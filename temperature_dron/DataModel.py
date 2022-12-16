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



class DatosControl():

    def __init__(self, path,
                 carpeta_fotos_analisis,
                 carpeta_fotos_chesspattern,
                 carpeta_gui,
                 instriscic_pkl,
                 carpeta_data
                  ):
        print("inicializando DatosControl ")
        self.path_directory = path

        self.carpeta_fotos_analisis = carpeta_fotos_analisis
        self.carpeta_fotos_chesspattern = carpeta_fotos_chesspattern
        self.instriscic_pkl = instriscic_pkl
        self.carpeta_data = carpeta_data
        self.carpeta_gui = carpeta_gui
        self.imagenes_chesspattern = list()
        self.imagenes_procesamiento = list()
        self.camera_instriscic = list()
        self.read_instricic_camera()
        self.total_incendio = 0
        self.total_fotos_chesspattern = 0
        
    def save_(func):
        def inner(self, *arg,**args):
            imwrite(func(self, *arg,**args))
        return inner


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
            path = self.path_directory
            return path.replace(self.carpeta_gui, self.carpeta_fotos_analisis), 1
        else:
            return path, 1

    @open_
    def open_foto_chesspattern(self, path = False):
        if isinstance(path, bool):
            path = self.path_directory
            return path.replace(self.carpeta_gui, self.carpeta_fotos_chesspattern), 2
        else:
            return path, 2

    def get_registed_camera_instricic(self, path = False):
        pass
    def save_registed_camera_instricic(self, ):
        pass

    #guarda foto con path nombre, altura y carpeta en especifico
    @save_
    def save_fotos_name(self, foto, altura, name, carpeta, path = False):
        if isinstance(path, bool):
            return os.path.join(self.path_directory, self.carpeta, name + "_" + str(altura) + ".png"), foto
        else:
            return os.path.join(path, self.carpeta, name + "_" + str(altura) + ".png"), foto

    def save_instricic_camera(self):
        with open(self.path_directory.replace(self.carpeta_gui, self.carpeta_data) + self.instriscic_pkl , "wb") as saving:
            pickle.dump([self.ret, self.mtx, self.dist, self.rvecs, self.tvecs], saving)

    def read_instricic_camera(self):
        with open(self.path_directory.replace(self.carpeta_gui, self.carpeta_data) + self.instriscic_pkl , "rb") as reading:
            try:
                self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = pickle.load(reading)
            except EOFError as nothing_in_file:
                print("there is nothing in the file, of data:")
                print(nothing_in_file)
