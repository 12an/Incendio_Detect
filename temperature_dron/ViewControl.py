# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from PySide6 import QtGui
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebKitWidgets import QWebView
from widget import Widget

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_main_qwidget


class ImagenLabel:
    def __init__(self, name):
        self.name = name
        self.imagen_qlabel = QLabel()


class ViewControl(Widget):
    def __init__(self, cantidad_imagenes, parent=None):
        super().__init__(parent)
        self.ui = Ui_main_qwidget()
        self.ui.setupUi(self)
        # eventos
        self.ui.ArmDisarmButton_dron.clicked.connect(self.ArmDisarmButton_dron_evento)
        self.ui.StartMisionButton_dron.clicked.connect(self.StartMisionButton_dron_evento)
        self.ui.RTLButton_dron.clicked.connect(self.RTLButton_dron_evento)
        self.ui.ManualAutoButton_dron.clicked.connect(self.ManualAutoButton_dron_evento)
        self.ui.AnteriorCordenadaBotton_mapa.clicked.connect(self.AnteriorCordenadaBotton_mapa_evento)
        self.ui.SiguienteCordenadaBotton_mapa.clicked.connect(self.SiguienteCordenadaBotton_mapa_evento)
        self.ui.GenerarReporteBotton_detalles.clicked.connect(self.GenerarReporteBotton_detalles_evento)
        self.ui.SiguienteCordenadaBotton_detalles.clicked.connect(self.SiguienteCordenadaBotton_detalles_evento)
        self.ui.AnteriorCordenadaBotton_detalles.clicked.connect(self.AnteriorCordenadaBotton_detalles_evento)
        # imagen 3d
        self.plot_layout = list()
        self.plot_layout.append(self.ui.mapa_3d)
        self.plot_layout.append(self.ui.mapa_2d)
        # imagen tab 3 detalles
        self.imagenes_detalles = {"0":ImagenLabel("Foto_Camara"),
                                  "1":ImagenLabel("ImagenProcesada")}
        self.ui.Foto_Camara.addWidget(self.imagenes_detalles.get("0"),
                                  1,
                                  1)
        self.ui.ImagenProcesada.addWidget(self.imagenes_detalles.get("1"),
                                  1,
                                  1)
        #mapa
        self.web = QWebView()
        self.web.settings().setAttribute(QWebSettings.JavascriptEnabled, True)
        self.ui.web_mapa.addWidget(self.web,
                                  1,
                                  1)


    def Show_frames(self, frame, index_layout, scalar = True, bit_image=False):
        try:
            bytesPerLine = frame.shape[1] * frame.shape[2]
        except AttributeError as error_list:
            print(error_list)
        else:
            if not(bit_image):
                ima = QtGui.QImage(frame,
                                   frame.shape[1],
                                   frame.shape[0],
                                   bytesPerLine,
                                   QtGui.QImage.Format_RGB888)
            else:
                ima = QtGui.QImage(frame,
                                   frame.shape[1],
                                   frame.shape[0],
                                   bytesPerLine,
                                   QtGui.QImage.Format_RGB32)
            imagen = QtGui.QPixmap.fromImage(ima)
            if scalar:
                imagen = imagen.scaled(469, 469, Qt.KeepAspectRatio)

            self.label_image[index_layout].setPixmap(imagen)
    def search_cordenates_map(self, cordenada):
        web.load(QUrl(tempPath))
        web.show()
        pass

    def show_plot(self, canvas_plot, index_layout):
        self.plot_layout[index_layout].addWidget(canvas_plot,
                                                 1,
                                                 1)

    def ArmDisarmButton_dron_evento(self):
        pass

    def StartMisionButton_dron_evento(self):
        pass

    def RTLButton_dron_evento(self):
        pass

    def ManualAutoButton_dron_evento(self):
        pass

    def AnteriorCordenadaBotton_mapa_evento(self):
        pass

    def SiguienteCordenadaBotton_mapa_evento(self):
        pass


    def GenerarReporteBotton_detalles_evento(self):
        pass

    def SiguienteCordenadaBotton_detalles_evento(self):
        pass

    def AnteriorCordenadaBotton_detalles_evento(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget(8)
    widget.show()
    sys.exit(app.exec())


