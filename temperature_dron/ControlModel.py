# This Python file uses the following encoding: utf-8
import sys
import os
import shutil
from PySide6.QtWidgets import QApplication
from ViewControl import ViewControl
from DataModel import DatosControl, BoolData
import sqlite3
from PySide6.QtCore import QTimer
from TransformFotos import RGBToTemperatureScale, TemperaturaMax, FiltroFotos, CalibrateFoto, Segmentacion
from datetime import datetime
import numpy as np
from PySide6.QtCore import QRunnable, Slot, Signal, QObject, QThreadPool
import traceback
from camera import CameraIntrisicsValue
from jinja2 import Environment, FileSystemLoader
import pdfkit



class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        bool data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)

class threadRGbtemperatura(QRunnable):

    def __init__(self, foto_, step_sampling, fiting_model):
        QRunnable.__init__(self)
        self.signals = WorkerSignals()
        self.foto_ = foto_
        self.step_sampling = step_sampling
        self.fiting_model = fiting_model

    @Slot()
    def run(self):
        foto_temperatura = np.zeros((self.foto_.shape[0]//self.step_sampling,
                                     self.foto_.shape[1]//self.step_sampling, 1), dtype=float)
        try:
            for i in range(0,self.foto_.shape[0], self.step_sampling):
                for j in range(0, self.foto_.shape[1], self.step_sampling):
                    foto_temperatura[i//self.step_sampling, j//self.step_sampling ] = self.fiting_model.predict(np.array([self.foto_[i,j][0:2]]))
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(foto_temperatura)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done        


class threadMaxTemperatura(QRunnable, TemperaturaMax):

    def __init__(self, foto_temperatura, max_expected_temp):
        QRunnable.__init__(self)
        TemperaturaMax.__init__(self, max_expected_temp)
        self.signals = WorkerSignals()
        self.foto_temperatura = foto_temperatura

    @Slot()    
    def run(self):
        try:
           triger = self.is_max_trigger_foto(self.foto_temperatura)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(triger)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class ControlModel(ViewControl, 
                   DatosControl,
                   RGBToTemperatureScale,
                   Segmentacion,
                   CalibrateFoto):

    def __init__(self, *arg, **args):
        print("inicializando Controlador ")
        self.index = 0
        #variables y constantes
        self.CHECKERBOARD_SIZE = [5, 5]
        
        self.index = 0
        self.click_siguiente = 0
        self.index_fotos_calibracion = 0
        self.click_siguiente_chesspatern = 0
        # temperaturas utiles para la segmentacion y transformacion temperatura pixel
        self.temp_incendio = 50
        self.max_expected_temp = 90
        self.min_expected_temp = 30
        self.block_thread_finished = False
        self.threadpool = QThreadPool()

        # cargando app
        ViewControl.__init__(self)
        #datos
        DatosControl.__init__(self)
        RGBToTemperatureScale.__init__(self, self.max_expected_temp,
                                       self.min_expected_temp)
        Segmentacion.__init__(self,**{"distancia":3,
                                      "temp_incendio":self.temp_incendio})
        self.camera_instrisics_ = CameraIntrisicsValue(self.CHECKERBOARD_SIZE)
        self.conection = sqlite3.connect(self.go_to("data_dir") + 'Data_Incendio.db')
        ## Creating cursor object and namimg it as cursor
        self.cursor = self.conection.cursor()
        self.open_foto_analisis(False)
        self.open_foto_chesspattern(False)
        #control dron
        self.start_mision = BoolData(False, "start_mision")
        self.rtl = BoolData(False, "rtl")
        self.manual_automatico = BoolData(False, "manual_automatico")
        self.arm_disarm = BoolData(False, "arm_disarm")
        # creando timer recurrente leer data del dron
        self.timer = QTimer()
        self.timer.timeout.connect(self.cargar_datos_dron)
        self.timer.start(2)#segundos
        # creando timer recurrente leer y procesar fotos
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.nueva_mision_dron_app)
        self.timer2.start(60)#segundos
        #iniciando desde el indixe 0 en los datos
        self.static_index()
        # 2. Create a template Environment
        self.env = Environment(loader=FileSystemLoader("templates/"))
        # 3. Load the template from the Environment
        self.template = self.env.get_template("reporte.html")
        path_wkhtmltopdf = self.go_to("wkhtmltox_dir") + '\\bin\\wkhtmltopdf.exe'
        self.config_wkhtmltopdf = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        for filename in os.listdir(self.go_to("temp_dir")):
            file_path = os.path.join(self.go_to("temp_dir"), filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def GuardarCambios_observaciones_evento(self):
        estimacion_to_save  = self.get_text_estimacion()
        hora_to_save = self.get_hora_estimacion()
        fecha_to_save = self.get_fecha_estimacion()
        self.update_hora({"hora":hora_to_save})
        self.update_fecha({"fecha":fecha_to_save})
        self.update_estimacion({"text":estimacion_to_save})

    def CancelarCambios_observaciones_evento(self):
        self.update_estimacion_show(self.estimacion)
        self.update_fecha_show(self.fecha)
        self.update_hora_show(self.hora)

    def ArmDisarmButton_dron_evento(self):
        self.arm_disarm.setear(not(self.arm_disarm.bool_value)) 
        
    def StartMisionButton_dron_evento(self):
        self.start_mision.setear(not(self.start_mision.bool_value)) 

    def RTLButton_dron_evento(self):
        self.rtl.setear(not(self.rtl.bool_value)) 

    def ManualAutoButton_dron_evento(self):
        self.manual_automatico.setear(not(self.manual_automatico.bool_value)) 

    def GenerarReporteBotton_detalles_evento(self):
        self.save_foto(self.go_to("temp_dir"), "procesada_" + str(self.imagenes_procesamiento[self.index].ID_data) + "jpeg",
                       self.imagenes_procesamiento[self.index].foto_undistorted)
        self.save_foto(self.go_to("temp_dir"), "cortada_" + str(self.imagenes_procesamiento[self.index].ID_data) + "jpeg",
                       self.imagenes_procesamiento[self.index].foto_undistorted_segmentada)
        # 4. Render the template with variables
        current_datetime = datetime.now()
        html = self.template.render(hora_= str(current_datetime.strftime("%m-%d-%Y")),
                                    fecha_= str(current_datetime.strftime("%H:%M")), 
                                    original_path = self.go_to("foto_dir")  + str(self.imagenes_procesamiento[self.index].ID_data) + "jpeg",
                                    procesada_path = self.go_to("temp_dir") + "procesada_" + str(self.imagenes_procesamiento[self.index].ID_data) + "jpeg",
                                    seleccion_path = self.go_to("temp_dir") + "cortada_" + str(self.imagenes_procesamiento[self.index].ID_data) + "jpeg",
                                    ID_ = str(self.imagenes_procesamiento[self.index].ID_data),
                                    fecha_hora_ = self.fecha +", " + self.hora,
                                    categoria_ = str(self.categoria),
                                    coordenadas_ = self.coordenada_url_latitude + ", " + self.coordenada_url_longitud,
                                    area_= str(self.area),
                                    estimacion_ = str(self.estimacion))

        # 5. Write the template to an HTML file
        with open(self.go_to("temp_dir") + 'html_report_jinja.html', 'w') as f:
             f.write(html)
             
        pdfkit.from_file(self.go_to("temp_dir") + 'html_report_jinja.html',
                         self.go_to("reportes_dir") + str(self.imagenes_procesamiento[self.index].ID_data) + "pdf",
                         configuration = self.config_wkhtmltopdf,
                         options={"enable-local-file-access": True})
        

    def load_data_show(self, index):
        self.ID_actual_sql_management["id"] = self.imagenes_procesamiento[index].ID_data
        self.fecha = self.fecha_sql()
        self.hora = self.hora_sql()
        self.categoria = self.categoria_sql()
        self.area = self.area_sql()
        self.estimacion = self.estimacion_sql()
        self.altura = self.altura_sql()
        self.grados_latitude, self.minutos_latitude, self.segundos_latitude = self.latitude_sql()
        self.grados_longitud, self.minutos_longitud, self.segundos_longitud = self.longitude_sql()

    def update(self):
        self.search_cordenates_map(self.url_from_data)
        self.update_text(*[],
                         **{"fecha_hora_inicio": self.fecha +", " + self.hora,
                         "categoria":self.categoria, 
                         "cordenadas_origen": self.coordenada_url_latitude + ", " + self.coordenada_url_longitud,
                         "estado": self.estimacion,
                         "area":self.area
                         })
        self.CancelarCambios_observaciones_evento()
        self.Show_frames(self.imagenes_procesamiento[self.index].foto_camara,
                         "Foto_Camara")
        if isinstance(self.imagenes_procesamiento[self.index].foto_undistorted_segmentada, np.ndarray):
            self.Show_frames(self.imagenes_procesamiento[self.index].foto_undistorted_segmentada,
                             "ImagenProcesada")
            x, y, z = self.plot_3d(self.imagenes_procesamiento[self.index].segmentos_coordenadas,
                                                    self.imagenes_procesamiento[self.index].foto_word_coordinate)
            """self.show_plot_3d(x,
                              y,
                              z,
                              "local_3d_word_plot")"""
        

    def build_url(self):
        semi_url_domain = "https://www.google.com/maps/place/"
        self.coordenada_url_latitude = str(self.grados_latitude) + "°" + str(self.minutos_latitude) + "'" + str(self.segundos_latitude) + '"' + "N"
        self.coordenada_url_longitud = str(self.grados_longitud) + "°" + str(self.minutos_longitud) + "'" + str(self.segundos_longitud) + '"' + "W"
        self.url_from_data = semi_url_domain + self.coordenada_url_latitude  + "+" + self.coordenada_url_longitud

    def chage_index(func):
        def innner(self, *arg,**args):
            index = func(self, *arg,**args)
            if self.index <= (self.total_incendio - 1):
                self.load_data_show(index)
                if not(isinstance(self.imagenes_procesamiento[index].foto_fitro, np.ndarray)):
                    _filtro = FiltroFotos(self.imagenes_procesamiento[index].foto_camara)
                    self.imagenes_procesamiento[index].foto_fitro = _filtro.foto_bilate
                    
                if not(isinstance(self.imagenes_procesamiento[index].foto_undistorted_cut, np.ndarray)):
                    _undistorted, cut_undistorted, ROI = self.calibrate(self.imagenes_procesamiento[index].foto_fitro,
                                                                                 self.mtx,
                                                                                 self.dist)
                    self.imagenes_procesamiento[index].foto_undistorted_cut = cut_undistorted
                    self.imagenes_procesamiento[index].foto_undistorted = _undistorted
                    self.imagenes_procesamiento[index].ROI = ROI
                    if isinstance(self.altura, int):
                        word_object = self.get_foto_3d_from_2d(self.imagenes_procesamiento[index].foto_undistorted_cut,
                                                                        self.mtx,
                                                                        59)
                    else:
                        word_object = self.get_foto_3d_from_2d(self.imagenes_procesamiento[index].foto_undistorted_cut,
                                                                        self.mtx,
                                                                        59)
                    self.imagenes_procesamiento[index].foto_word_coordinate = word_object  
                if not(isinstance(self.imagenes_procesamiento[index].foto_temperatura_scaled, np.ndarray)  and not(self.block_index_updating)):
                    self.block_index_updating = True
                    self.from_RGB_to_temp(self.imagenes_procesamiento[index].foto_undistorted_cut, 1, True)
                self.build_url()
                self.update()
                self.anterior_index = index
        return innner
            
    @chage_index
    def siguiente(self):
        if self.index < (self.total_incendio - 1) and not(self.block_index_updating):
            self.index += 1
        return self.index

    @chage_index
    def anterior(self):
        if self.index > 0 and not(self.block_index_updating):
            self.index -= 1
        return self.index

    @chage_index
    def static_index(self):
        print ("cargando datos inicial")
        return self.index

    def cargar_datos_dron(self):
        self.read_actual_coordenates_dron()
        self.read_battery_dron()
        latitud = self.coordenadas_actual_dron.get("latitude")
        longitud = self.coordenadas_actual_dron.get("longitud")
        latitud_text = str(latitud[0]) + "°"  + str(latitud[1]) + "'" + str(latitud[2]) + '" N'
        longitud_text = str(longitud[0]) + "°"  + str(longitud[1]) + "'" + str(longitud[2]) + '" W'
        self.update_text_labels_dron(**{"coord_actual_dron":latitud_text + ", " + longitud_text,
                                        "porc_bat":self.bateria_dron_porc_value})

    def nueva_mision_dron_app(self):
        if(self.status_mision() and not(self.block_thread_finished)):
            self.foto_temp_spam = self.foto_spam()
            self.from_RGB_to_temp(self.foto_temp_spam, 2)
            self.block_thread_finished = True

    def chage_index_chesspatern(func):
        def innner(self, *arg,**args):
            index_fotos_calibracion = func(self, *arg,**args)
            if self.click_siguiente_chesspatern <= (self.total_fotos_chesspattern - 1):
                foto = self.imagenes_chesspattern[index_fotos_calibracion].foto
                self.Show_frames(foto,
                                 "Foto_calibracion_antes")
                self.Show_frames(self.camera_instrisics_.extracting_corners(foto),
                                 "Foto_calibracion_despues")
                self.click_siguiente_chesspatern +=1 
        return innner

    @chage_index_chesspatern
    def Siguiente_Calibracion_evento(self):
        if(self.index_fotos_calibracion<= (self.total_fotos_chesspattern -2 ) ):
            self.index_fotos_calibracion += 1
        return self.index_fotos_calibracion

    def Calcular_Calibracion_evento(self):
        if(self.index_fotos_calibracion>0):
            self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = self.camera_instrisics_.get_intrisic_parameters()
            self.save_instricic_camera()

    @chage_index_chesspatern
    def onChange(self,index): #changed!
        #si estamos en la pagina de calibracion
        if index==4:
            self.index_fotos_calibracion = 0
            self.click_siguiente_chesspatern = 0
            self.camera_instrisics_ = 0
            self.camera_instrisics_ = CameraIntrisicsValue(self.CHECKERBOARD_SIZE)
        return self.index_fotos_calibracion 
            
        
    """
    Hilos para procesamiento, resultados
    """
    def signal_error(self, error):
        self.block_thread_finished = False

    def is_max_trigger_foto_complete(self, triger):
        if triger:
            print("se detecto un incendio")
            current_datetime = datetime.now()
            hora = current_datetime.strftime("%H:%M")
            fecha = current_datetime.strftime("%m-%d-%Y")
            self.read_actual_coordenates_dron()
            latitud = self.coordenadas_actual_dron.get("latitude")
            longitud = self.coordenadas_actual_dron.get("longitud")
            altura = self.read_actual_altura_dron()
            self.guardar_nuevo_incendio_datos(**{"fecha":fecha,
                                                 "hora":hora,
                                                 "categoria":0,
                                                 "area":-1,
                                                 "estimacion":"n/a",
                                                 "latitude":latitud,
                                                 "longitud":longitud,
                                                 "foto_normal":self.foto_temp_spam,
                                                 "altura":altura})
            #terminamos y ponemos en false la variable
            self.write_status_mision(False)
            #update fotos list
            self.open_foto_analisis()
        self.block_thread_finished = False


    def from_RGB_to_temp_complete(self, foto_temperatura):
        self.is_max_trigger_foto(foto_temperatura)

    def from_RGB_to_temp_save(self, foto_temperatura):
        self.imagenes_procesamiento[self.index].foto_temperatura_scaled = foto_temperatura
        incendio, imagen = self.segmentacion(self.imagenes_procesamiento[self.index].foto_temperatura_scaled,
                                             self.imagenes_procesamiento[self.index].foto_undistorted,
                                             self.imagenes_procesamiento[self.index].ROI)
        self.imagenes_procesamiento[self.index].segmentos_coordenadas = incendio
        self.imagenes_procesamiento[self.index].foto_undistorted_segmentada = imagen
        self.Show_frames(self.imagenes_procesamiento[self.index].foto_undistorted_segmentada,
                         "ImagenProcesada")
        if self.area == -1:
            self.area = self.area_foto(incendio, 
                                       self.imagenes_procesamiento[self.index].foto_word_coordinate)
            print("Area: ", self.area)
            #self.update_area(self.area)
        self.block_index_updating = False
    
    def from_RGB_to_temp(self, foto_, step_sampling, foto_temp_save = False):
        thread = threadRGbtemperatura(foto_, step_sampling, self.regresion_model)
        if not(foto_temp_save):
            thread.signals.result.connect(self.from_RGB_to_temp_complete)
        else:
            thread.signals.result.connect(self.from_RGB_to_temp_save)
        thread.signals.error.connect(self.signal_error)
        self.threadpool.start(thread)
    
    def is_max_trigger_foto(self, foto_temperatura):
        thread = threadMaxTemperatura(foto_temperatura, self.max_expected_temp)
        thread.signals.result.connect(self.is_max_trigger_foto_complete)
        thread.signals.error.connect(self.signal_error)
        # Execute
        self.threadpool.start(thread)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ejecucion = ControlModel()
    ejecucion.show()
    sys.exit(app.exec_())

