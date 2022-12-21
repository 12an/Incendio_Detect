# This Python file uses the following encoding: utf-8
import os
import glob
from cv2 import imwrite, imread, cvtColor, COLOR_RGB2BGR
import pickle
from  TransformFotos import LuminosidadFotos, FiltroFotos, CalibrateFoto, Segmentacion
from widget import MplCanvas
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class DumpPumpVariable():
    def dump(self, directorio, variable_name, variable):
        with open(directorio + variable_name + ".pkl" , "wb") as saving:
            pickle.dump(variable, saving)
    def pump(self, directorio, variable_name):
        with open(directorio + variable_name + ".pkl", "rb") as reading:
            variable_leida = 0
            try:
                variable_leida = pickle.load(reading)
            except EOFError as nothing_in_file:
                print("there is nothing in the file, of data:")
                print(nothing_in_file)
            return variable_leida

class Path():
    def __init__(self):
        self.origen_dir = os.path.abspath(os.path.dirname( __file__ ))
        self.current_dir = self.origen_dir
        self.carpetas_dir = {"data_dir" : "data",
                             "foto_dir" : "fotos_analisis",
                             "dron_dir" : "code_dron",
                             "chess_dir" : "fotos_chess_pattern",
                             "main_dir" : "temperature_dron"}
        self.get_actual_dir()
    """
    optener data con una key relacionada al diccionario
        self.carpetas_dir = {"data_dir" : "data",
                             "foto_dir" : "fotos_analisis",
                             "dron_dir" : "code_dron",
                             "chess_dir" : "fotos_chess_pattern",
                             "main_dir" : "temperature_dron"}
    """
    def go_to(self, key):
        self.current_dir = self.current_dir.replace(self.name_actual_carpet,
                                                    self.carpetas_dir.get(key))
        self.name_actual_carpet = self.carpetas_dir.get(key)
        return self.current_dir + "/"
        
    def get_actual_dir(self):
        for key, value in self.carpetas_dir:
            if value in self.current_dir:
                self.name_actual_carpet = value


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class IncendioData():
    def __init__(self,foto_camara,
                 ID_data,
                 *arg,
                 **args):
        self.ID_data = ID_data
        self.foto_camara = foto_camara

class FotoChesspatternData():
    def __init__(self, id_foto, foto):
        self.id_foto = id_foto
        self.agregada = False
        self.foto = foto



class DatosControl(Path, DumpPumpVariable):

    def __init__(self):
        Path.__init__(self)
        print("inicializando DatosControl ")
        self.imagenes_chesspattern = list()
        self.imagenes_procesamiento = list()
        self.camera_instriscic = list()
        self.read_instricic_camera()
        self.total_incendio = 0
        self.total_fotos_chesspattern = 0
        self.bateria_dron_porc_value = 0
        self.coordenadas_actual_dron = {}

    def open_(func):
        def inner(self, *arg,**args):
            # charging images
            path, tipo_imagen = func(self, *arg,**args)
            for path_name_foto in glob.iglob(path + "\*.jpg"):
                #al path le quitamos el nombre del archiv0
                name_foto = path_name_foto[len(path) + 1 : ]
                ID_data = name_foto[0:name_foto.find("_")]
                imagen = cvtColor(imread(path_name_foto), COLOR_RGB2BGR)
                if(tipo_imagen==1):
                    self.total_incendio += 1
                    self.imagenes_procesamiento.append(IncendioData(*[],
                                                                    **{"foto_camara":imagen,
                                                                       "ID_data": ID_data
                                                                       }))
                if(tipo_imagen==2):
                    self.total_fotos_chesspattern += 1
                    self.imagenes_chesspattern.append(
                                                      FotoChesspatternData(ID_data, imagen)
                                                      )
        return inner

    @open_
    def open_foto_analisis(self, path = False):
        if isinstance(path, bool):
            return self.go_to("foto_dir"), 1
        else:
            return path, 1

    @open_
    def open_foto_chesspattern(self, path = False):
        if isinstance(path, bool):
            path = self.path_directory
            return self.go_to("chess_dir"), 2
        else:
            return path, 2

    def get_registed_camera_instricic(self, path = False):
        pass
    def save_registed_camera_instricic(self, ):
        pass

    def save_instricic_camera(self):
        self.dump(self.go_to("data_dir"),
                  "instricic_camera",
                  [self.ret, self.mtx, self.dist, self.rvecs, self.tvecs])

    def read_instricic_camera(self):
        packet = self.pump(self.go_to("data_dir"), "instricic_camera")
        try:
            self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = packet
        except ValueError as nothing_in_file:
            print("parece que no se ha guardado")
            print(nothing_in_file)
    def read_battery_dron(self):
        self.bateria_dron_porc_value = self.pump(self.go_to("data_dir"), "bateria_data_dron")

    def read_actual_coordenates_dron(self):
        self.coordenadas_actual_dron = self.pump(self.go_to("data_dir"), "coordenadas_dron")
        