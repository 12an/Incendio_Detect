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

class PuntosIncendioReferenciaDron:
    def __init__(self, cordenada_dron, incendio_seleccion_ij):
        self.cordenada_dron = cordenada_dron
        self.altura = altura
        self.incendio_seleccion_ij = incendio_seleccion_ij
    def get3d_2d(self):
        # z es constante a la altura de la imagen
        for i,j,temp in zip(self.incendio_seleccion_ij):
            vector_pixel_2d_posicion = np.matrix([[i], [j], [self.altura]])
            foto_3d_from_2d = np.linalg.solv(self.newcameramtx, vector_pixel_2d_posicion)
            self.foto_3d_from_2d[i][j][0] = foto_3d_from_2d[0]
            self.foto_3d_from_2d[i][j][1] = foto_3d_from_2d[1]
            self.foto_3d_from_2d[i][j][2] = foto_3d_from_2d[2]

class OrigenReferenciaGlobal(PuntosIncendioReferenciaDron):
    def __init__(self, cordenada_referencia_global):
        self.cordenada_referencia_global = cordenada_referencia_global


class IncendioProyeccionOrigen(OrigenReferenciaGlobal):
    def __init__(self):
        pass


class IncendioData(IncendioProyeccionOrigen):
    def __init__(self,foto_referencia,
                 cordenada_origen_incendio,
                 categoria,
                 fecha_deteccion,
                 ultima_actualizacion,
                 observaciones,
                 intensidad,
                 *arg,
                 **args):
        self.foto_referencia = foto_referencia
        self.cordenada_origen = cordenada_origen_incendio
        self.categoria = categoria
        self.fecha_deteccion = fecha_deteccion
        self.ultima_actualizacion = ultima_actualizacion
        self.observaciones = observaciones
        self.intensidad = intensidad


class CameraData:
    def __init__(self,
                 ret,
                 mtx,
                 dist,
                 rvecs,
                 tvecs):
        self.ret = ret
        self.mtx = mtx
        self.dist = dist
        self.rvecs = rvecs
        self.tvecs = tvecs


class FotoChesspatternData():
    total_fotos = 0
    def __init__(self, id_foto, foto):
        self.id_foto = id_foto
        self.agregada = False
        self.foto = foto
        self.__class__.total_fotos += 1

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
        self.imagenes_chesspattern = list()
        self.carpeta_fotos_analisis = carpeta_fotos_analisis
        self.carpeta_fotos_chesspattern = carpeta_fotos_chesspattern
        self.instriscic_pkl = instriscic_pkl
        self.carpeta_data = carpeta_data
        self.carpeta_gui = carpeta_gui
        self.camera_instriscic = list()
        self.read_instricic_camera()
    def save_(func):
        def inner(self, *arg,**args):
            imwrite(func(self, *arg,**args))
        return inner

    def open_(func):
        def inner(self, *arg,**args):

            # charging images
            path, tipo_imagen = func(self, *arg,**args)
            for path_name_foto in glob.iglob(path + "\*.jpg"):
                name_foto = path_name_foto[len(path) + 1 : ]
                imagen = cvtColor(imread(path_name_foto), COLOR_RGB2BGR)
                id_imagen = name_foto[0:name_foto.find("_")]
                if(tipo_imagen==1):
                    altura_imagen = int(name_foto[name_foto.find("_") + 1: name_foto.find("-")])
                    coordenada_mix = name_foto[name_foto.find("-") + 1: name_foto.find(".")]
                    coordenada_imagen = {"x":coordenada_mix[coordenada_mix.find("x") + 1 :coordenada_mix.find("y")],
                                         "y":coordenada_mix[coordenada_mix.find("x") + 1 :coordenada_mix.find("y")]}
                if(tipo_imagen==2):
                    self.imagenes_chesspattern.append(
                        FotoChesspatternData(id_imagen, imagen)
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
