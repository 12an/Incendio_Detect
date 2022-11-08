# This Python file uses the following encoding: utf-8
import sys
import matplotlib
matplotlib.use('Qt5Agg')
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from PySide6 import QtGui
from widget import Widget

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_main_qwidget

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class ViewControl(Widget):
    def __init__(self, cantidad_imagenes, parent=None):
        super().__init__(parent)
        self.ui = Ui_main_qwidget()
        self.ui.setupUi(self)
        # eventos
        self.ui.anterior_mapa_1.clicked.connect(self.event_anterior_mapa_1)
        self.ui.siguiente_mapa_1.clicked.connect(self.event_siguiente_mapa_1)
        self.ui.anterior_3dmapa_2.clicked.connect(self.event_anterior_3dmapa_2)
        self.ui.siguiente_3dmapa_2.clicked.connect(self.event_siguiente_3dmapa_2)
        self.ui.anterior_detalles_3.clicked.connect(self.event_anterior_detalles_3)
        self.ui.siguiente_detalles_3.clicked.connect(self.event_siguiente_detalles_3)
        # imagenes para los layout
        self.label_image = list()
        self.label_image.append(QLabel())
        self.plot_layout = list()
        self.plot_layout.append(self.ui.mapa_3d)
        self.ui.antes_calibracion_layout.addWidget(self.label_image[0],
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

    def show_plot(self, canvas_plot, index_layout):
        self.plot_layout[index_layout].addWidget(canvas_plot,
                                                 1,
                                                 1)

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
    widget = Widget(8)
    widget.show()
    sys.exit(app.exec())


