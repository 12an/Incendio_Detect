# This Python file uses the following encoding: utf-8
import os
import sys
from PySide6.QtWidgets import QApplication
from ViewControl import ViewControl
from PIL import Image as im

class ControlModel(ViewControl):

    def __init__(self, *arg, **args):
        print("inicializando Controlador ")
        self.current_dir = os.path.abspath(os.path.dirname( __file__ ))

        # cargando app
        ViewControl.__init__(self)
        self.search_cordenates_map()
        #datos


    def siguiente(self):
        pass
    def anterior(self):
        pass
    def ArmDisarmButton_dron_evento(self):
        pass

    def StartMisionButton_dron_evento(self):
        pass

    def RTLButton_dron_evento(self):
        pass

    def ManualAutoButton_dron_evento(self):
        pass

    def GenerarReporteBotton_detalles_evento(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ejecucion = ControlModel()
    ejecucion.show()
    sys.exit(app.exec_())
