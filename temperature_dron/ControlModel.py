# This Python file uses the following encoding: utf-8
import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
import numpy as np
from PySide6.QtCore import QRunnable, Slot, Signal, QObject, QThreadPool
from camera import CameraIntrisicsValue
from TransformFotos import FiltroFotos, CalibrateFoto, Segmentacion
from DataModel import DatosControl, BoolData
from ViewControl import ViewControl
from Trheads import threadMaxTemperatura

class ControlModel(ViewControl, 
                   DatosControl,
                   Segmentacion,
                   CalibrateFoto,
                   threadMaxTemperatura):

    def __init__(self, *arg, **args):
        print("inicializando Controlador ")
        self.index = 0
        #variables y constantes
        self.CHECKERBOARD_SIZE = [5, 5]
        self.index = 0
        self.click_siguiente = 0
        self.index_fotos_calibracion = 0
        self.click_siguiente_chesspatern = 0
        # temperaturas utiles para la segmentacion
        self.temp_incendio = 50
        self.block_thread_finished = False
        self.threadpool = QThreadPool()
        # cargando app
        ViewControl.__init__(self)
        #datos
        DatosControl.__init__(self)
        Segmentacion.__init__(self,**{"distancia":3,
                                      "temp_incendio":self.temp_incendio})
        self.camera_instrisics_ = CameraIntrisicsValue(self.CHECKERBOARD_SIZE)
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
        self.generar_reporte(self.coordenada_url_latitude, self.coordenada_url_longitud)

    def update(self, id_):
        self.search_cordenates_map(self.build_url())
        self.update_text(*[],
                         **{"fecha_hora_inicio": self.fecha +", " + self.hora,
                         "categoria":self.categoria, 
                         "cordenadas_origen": self.coordenada_url_latitude + ", " + self.coordenada_url_longitud,
                         "estado": self.estimacion,
                         "area":self.area
                         })
        self.CancelarCambios_observaciones_evento()
        self.Show_frames(self.imagenes_procesamiento.get(id_).foto_camara,
                         "Foto_Camara")
        self.Show_frames(self.imagenes_procesamiento.get(id_).foto_undistorted_segmentada,
                         "ImagenProcesada")
        x, y, z = self.plot_3d(self.imagenes_procesamiento.get(id_).segmentos_coordenadas,
                               self.imagenes_procesamiento.get(id_).foto_word_coordinate)      

    def build_url(self):
        semi_url_domain = "https://www.google.com/maps/place/"
        self.coordenada_url_latitude = str(self.grados_latitude) + "°" + str(self.minutos_latitude) + "'" + str(self.segundos_latitude) + '"' + "N"
        self.coordenada_url_longitud = str(self.grados_longitud) + "°" + str(self.minutos_longitud) + "'" + str(self.segundos_longitud) + '"' + "W"
        url_from_data = semi_url_domain + self.coordenada_url_latitude  + "+" + self.coordenada_url_longitud
        return url_from_data 

    def chage_index(func):
        def innner(self, *arg,**args):
            index = func(self, *arg,**args)
            self.current_id  = self.all_ids[index]
            self.load_data(self.current_id)
            if not(isinstance(self.imagenes_procesamiento.get(self.current_id).foto_fitro, np.ndarray)):
                _filtro = FiltroFotos(self.imagenes_procesamiento.get(self.current_id).foto_camara)
                self.imagenes_procesamiento.get(self.current_id).foto_fitro = _filtro.foto_bilate
                if not(isinstance(self.imagenes_procesamiento.get(self.current_id).foto_undistorted_cut, np.ndarray)):
                    _undistorted, cut_undistorted, ROI = self.calibrate(self.imagenes_procesamiento[index].foto_fitro,
                                                                                 self.mtx,
                                                                                 self.dist)
                    self.imagenes_procesamiento.get(self.current_id).foto_undistorted_cut = cut_undistorted
                    self.imagenes_procesamiento.get(self.current_id).foto_undistorted = _undistorted
                    self.imagenes_procesamiento.get(self.current_id).ROI = ROI
                    if isinstance(self.altura, int):
                        word_image = self.get_foto_3d_from_2d(self.imagenes_procesamiento.get(self.current_id).foto_undistorted_cut,
                                                                        self.mtx,
                                                                        self.altura)
                    else:
                        word_image = self.get_foto_3d_from_2d(self.imagenes_procesamiento.get(self.current_id).foto_undistorted_cut,
                                                                        self.mtx,
                                                                        59)
                    self.imagenes_procesamiento.get(self.current_id).foto_word_coordinate = word_image  
                if not(isinstance(self.imagenes_procesamiento.get(self.current_id).foto_undistorted_segmentada , np.ndarray)):
                    self.imagen_segmentacion(self.imagenes_procesamiento.get(self.current_id).foto_temperatura)
                self.update(self.current_id)
                self.anterior_index = index
        return innner
            
    @chage_index
    def siguiente(self):
        if self.index < (len(self.all_ids)- 1):
            self.index += 1
        return self.index

    @chage_index
    def anterior(self):
        if self.index > 0:
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
            self.guardar_nuevo_incendio()
            #terminamos y ponemos en false la variable
            self.write_status_mision(False)
        self.block_thread_finished = False

    def imagen_segmentacion(self, foto_temperatura):
        incendio, imagen = self.segmentacion(self.imagenes_procesamiento[self.index].foto_temperatura_scaled,
                                             self.imagenes_procesamiento[self.index].foto_undistorted,
                                             self.imagenes_procesamiento[self.index].ROI)
        self.imagenes_procesamiento[self.index].segmentos_coordenadas = incendio
        self.imagenes_procesamiento[self.index].foto_undistorted_segmentada = imagen
        if self.area == -1:
            self.area = self.area_foto(incendio, 
                                       self.imagenes_procesamiento[self.index].foto_word_coordinate)
            print("Area: ", self.area)
            #self.update_area(self.area)
       
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