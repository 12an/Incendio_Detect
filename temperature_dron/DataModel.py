# This Python file uses the following encoding: utf-8
import os
import glob
from cv2 import imwrite, imread, cvtColor, COLOR_RGB2BGR
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import pdfkit
import traceback
from DirGestion import Path, IncendioFolder, DumpPumpVariable
from DataSQL import DataSQL


class BoolData(Path, DumpPumpVariable):
    def __init__(self, value, variable_name):
        Path.__init__(self)
        self.variable_name = variable_name
        self.bool_value = value

    def setear(self, value):
        self.bool_value = value
        self.dump(self.go_to("data_dir"), self.variable_name, self.bool_value )


class IncendioData():
    def __init__(self,foto_raw,
                 temperatura_foto,
                 **args):
        self.foto_camara = foto_raw #foto original
        self.foto_fitro = None # foto con algunos filtros
        self.foto_undistorted = None # sin los efectos distorcion del lente
        self.foto_undistorted_cut = None # quitada toda la parte innecesaria para procesamiento
        self.foto_word_coordinate= None # donde se localizan cada pixel en el mundo real
        self.foto_undistorted_segmentada = None  # imagen a color del area del incendio      
        self.foto_temperatura = temperatura_foto #foto con pixeles transformado a su respectiva temperatura
        self.foto_temperatura_undistorted = None
        self.foto_temperatura_undistorted_cut = None
        self.segmentos_coordenadas = {}  #dictionario, parte de interes del fuego, calcular area
        self.ROI = None #recortes de interes de la imagen undistorted


class FotoChesspatternData():
    def __init__(self, id_foto, foto):
        self.id_foto = id_foto
        self.agregada = False
        self.foto = foto


class CameraIntrics():
    def __init__(self):
        self.ret = None
        self.mtx = None
        self.dist = None
        self.rvecs = None
        self.tvecs = None


class DatosControl(Path,
                   DumpPumpVariable,
                   CameraIntrics,
                   DataSQL):
    def __init__(self):
        Path.__init__(self)
        CameraIntrics.__init__(self)
        DataSQL.__init__(self, self.go_to("data_dir"))
        print("inicializando DatosControl")
        self.imagenes_chesspattern = list()
        self.imagenes_procesamiento = dict()
        self.folders_incendios = dict()
        self.read_instricic_camera()
        self.total_fotos_chesspattern = 0
        self.bateria_dron_porc_value = 0
        self.coordenadas_actual_dron = {}
        self.current_id = 0
        self.cargar_datos()
        #para los reportes
        #Create a template Environment
        self.env = Environment(loader=FileSystemLoader("templates/"))
        #Load the template from the Environment
        self.template = self.env.get_template("reporte.html")
        self.config_wkhtmltopdf = pdfkit.configuration(wkhtmltopdf=self.go_to("wkhtmltox_dir") + "wkhtmltopdf.exe")
        self.open_foto_chesspattern()

    def get_time(self):
        current_datetime = datetime.now()
        hora = current_datetime.strftime("%H:%M")
        fecha = current_datetime.strftime("%m-%d-%Y")
        return hora, fecha

    def cargar_datos(self):
        for id_ in self.all_ids:
            folder = IncendioFolder(id_, self.go_to("incendios_dir"))
            self.folders_incendios[id_] = folder
            self.imagenes_procesamiento[id_] = (IncendioData(**{"foto_raw": folder.get_raw_foto(),
                                                            "temperatura_foto": folder.get_temp_foto()
                                                             }))

    def open_foto_chesspattern(self):
        path = self.go_to("chess_dir")
        for path_name_foto in glob.iglob(path + "\*.jpeg"):
            #al path le quitamos el nombre del archiv0
            name_foto = path_name_foto[len(path) : ]               
            ID_data = name_foto[:-4]
            imagen = imread(path_name_foto)
            self.total_fotos_chesspattern += 1
            self.imagenes_chesspattern.append(FotoChesspatternData(ID_data, imagen))

    def guardar_nuevo_incendio(self):
        hora, fecha = self.get_time()
        self.read_actual_coordenates_dron()
        latitud = self.coordenadas_actual_dron.get("latitude")
        longitud = self.coordenadas_actual_dron.get("longitud")
        altura = self.read_actual_altura_dron()
        id_ = self.nuevo_incendio_datos(**{"fecha":fecha,
                                           "hora":hora,
                                           "categoria":0,
                                           "area":-1,
                                           "estimacion":"n/a",
                                           "latitude":latitud,
                                           "longitud":longitud,
                                           "altura":altura})
        folder = IncendioFolder(id_, new_folder = True)
        folder.save_temp_foto(self.foto_temp_spam)
        folder.save_raw_foto(self.foto_raw_spam)
        self.folders_incendios[id_] = folder
        self.total_incendio += 1
        self.imagenes_procesamiento[id_] = (IncendioData(**{"foto_raw": folder.get_raw_foto(),
                                                           "temperatura_foto": folder.get_temp_foto(),
                                                           "ID_data": id_
                                                            }))
    def save_instricic_camera(self):
        self.dump(self.go_to("data_dir"),
                  "registed_data_instricic",
                  [self.ret, self.mtx, self.dist, self.rvecs, self.tvecs])

    def read_instricic_camera(self):
        packet = self.pump(self.go_to("data_dir"), "registed_data_instricic")
        try:
            self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = packet
        except ValueError as nothing_in_file:
            print("parece que no se ha guardado")
            print(nothing_in_file)

    def read_battery_dron(self):
        self.bateria_dron_porc_value = self.pump(self.go_to("data_dir"), "bateria_data_dron")
        return self.bateria_dron_porc_value

    def read_actual_coordenates_dron(self):
        self.coordenadas_actual_dron = self.pump(self.go_to("data_dir"), "coordenadas_dron")
        return self.coordenadas_actual_dron
    
    def read_actual_altura_dron(self):
        self.altura_actual_dron = self.pump(self.go_to("data_dir"), "altura_dron")
        return self.altura_actual_dron

    def status_mision(self):
        self.mision_status = self.pump(self.go_to("data_dir"), "mision_status")
        return self.mision_status

    def write_status_mision(self, value):
        self.dump(self.go_to("data_dir"),
                  "mision_status",
                  value)

    def foto_spam(self):
        return imread(self.go_to("fotos_spam_dir") + "spam.jpeg")
    
    def save_foto(self, path, name, foto):
        imwrite(path + name, foto)

    def load_data(self):
        self.fecha = self.fecha_sql()
        self.hora = self.hora_sql()
        self.categoria = self.categoria_sql()
        self.area = self.area_sql()
        self.estimacion = self.estimacion_sql()
        self.altura = self.altura_sql()
        self.grados_latitude, self.minutos_latitude, self.segundos_latitude = self.latitude_sql()
        self.grados_longitud, self.minutos_longitud, self.segundos_longitud = self.longitude_sql()

    def generar_reporte(self, coordenada_url_latitude, coordenada_url_longitud):
        self.folders_incendios.get(self.current_id).save_foto_temporal_dir(self.imagenes_procesamiento.get(self.current_id).foto_undistorted_segmentada,
                                                                           "cortada")
        self.folders_incendios.get(self.current_id).save_foto_temporal_dir(self.imagenes_procesamiento.get(self.current_id).foto_undistorted,
                                                                           "procesada")
        # Render the template with variables
        hora, fecha = self.get_time()
        file_html = self.template.render(hora_ = hora,
                                    fecha_ = fecha,
                                    original_path = self.folders_incendios.get(self.current_id).path_root + "\\raw\\raw.jpeg",
                                    procesada_path = self.folders_incendios.get(self.current_id).path_temporal_folder + "procesada.jpeg",
                                    seleccion_path = self.folders_incendios.get(self.current_id).path_temporal_folder + "cortada.jpeg",
                                    ID_ = self.current_id,
                                    fecha_hora_ = self.fecha +", " + self.hora,
                                    categoria_ = str(self.categoria),
                                    coordenadas_ = coordenada_url_latitude + ", " + coordenada_url_longitud,
                                    area_= str(self.area),
                                    estimacion_ = str(self.estimacion))

        # Write the template to an HTML file
        with open(self.folders_incendios.get(self.current_id).path_temporal_folder + 'html_report.html', 'w') as f:
             f.write(file_html)
        pdfkit.from_file(self.folders_incendios.get(self.current_id).path_temporal_folder + 'html_report.html',
                         self.folders_incendios.get(self.current_id).path_save_reporte(),
                         configuration = self.config_wkhtmltopdf,
                         options={"enable-local-file-access": True})
