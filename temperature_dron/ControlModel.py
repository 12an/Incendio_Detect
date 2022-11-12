# This Python file uses the following encoding: utf-8
import os
import sys
from PySide6.QtWidgets import QApplication
from DataModel import DatosControl
from ViewControl import ViewControl
import cv2
from PIL import Image as im

class ControlModel(DatosControl, ViewControl):

    def __init__(self, *arg, **args):
        print("inicializando Controlador ")
        self.index_tag1 = 0
        self.index_tag2 = 0
        self.index_tag3 = 0
        self.index_tag4 = 0
        self.index_tag5 = 0

        self.current_dir = os.path.abspath(os.path.dirname( __file__ ))
        self.sensor_size = [3.55,5.88]
        self.resolucion = [1920, 1080]
        # cargando app
        Widget.__init__(self,
                        *[],
                        **{"cantidad_imagenes":11})
        self.parametros_calibracion = {"numero_cameras" : 1,
                                  "sensor_size" : self.sensor_size,
                                  "camera_id" : 0,
                                  "CHECKERBOARD" : (6,9)
                                  }
        self.camera_instrisics_ = CameraIntrisicsValue(*[],
                                                       **self.parametros_calibracion
                                                       )

        #datos
        DatosControl.__init__(self,*[],
                                      **{"path" : self.current_dir,
                                         "carpeta_fotos_analisis" : "fotos_analisis",
                                         "carpeta_fotos_chesspattern" : "fotos_chess_pattern",
                                         "carpeta_gui" : "GUI_QT",
                                         "carpeta_data" : "data",
                                         "instriscic_pkl" : r"\registed_data_instricic.pkl"
                                         }
                             )
        # configurando inicio
        self.open_foto_analisis(False)
        self.open_foto_chesspattern(False)


    def event_anterior_mapa_1(self):
        pass


    def event_siguiente_mapa_1(self):
        pass

    def event_anterior_3dmapa_2(self):
        pass

    def event_siguiente_3dmapa_2(self):
        pass

    def event_anterior_detalles_3(self):
        pass

    def event_siguiente_detalles_3(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ejecucion = ControlModel()
    ejecucion.show()
    sys.exit(app.exec_())
