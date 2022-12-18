# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QUrl
from PySide6 import QtGui
from PySide6.QtWebEngineWidgets import *
from PySide6.QtWebEngineCore import *
from widget import Widget


class ImagenLabel:
    def __init__(self, name):
        self.name = name
        self.qlabel = QLabel()


class ViewControl(Widget):
    def __init__(self):
        Widget.__init__(self)
        # eventos
        self.ui.ArmDisarmButton_dron.clicked.connect(self.ArmDisarmButton_dron_evento)
        self.ui.StartMisionButton_dron.clicked.connect(self.StartMisionButton_dron_evento)
        self.ui.RTLButton_dron.clicked.connect(self.RTLButton_dron_evento)
        self.ui.ManualAutoButton_dron.clicked.connect(self.ManualAutoButton_dron_evento)
        self.ui.AnteriorCordenadaBotton_mapa.clicked.connect(self.anterior)
        self.ui.SiguienteCordenadaBotton_mapa.clicked.connect(self.siguiente)
        self.ui.GenerarReporteBotton_detalles.clicked.connect(self.GenerarReporteBotton_detalles_evento)
        self.ui.SiguienteCordenadaBotton_detalles.clicked.connect(self.siguiente)
        self.ui.AnteriorCordenadaBotton_detalles.clicked.connect(self.anterior)
        # imagen 3d
        self.plot_layout = list()
        self.plot_layout.append(self.ui.mapa_3d)
        self.plot_layout.append(self.ui.mapa_2d)
        # imagen tab 3 detalles
        self.imagenes_detalles = {"0":ImagenLabel("Foto_Camara"),
                                  "1":ImagenLabel("ImagenProcesada")}
        self.ui.Foto_Camara.addWidget(self.imagenes_detalles.get("0").qlabel,
                                  1,
                                  1)
        self.ui.ImagenProcesada.addWidget(self.imagenes_detalles.get("1").qlabel,
                                  1,
                                  1)
        #mapa
        self.web_view = QWebEngineView()
        self.web_view.settings()
        self.ui.web_mapa.addWidget(self.web_view,
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
        self.web_view.load(QUrl(cordenada))
        self.web_view.show()
    def update_text_labels(self,
                           fecha_hora_inicio,
                           categoria,
                           cordenadas_origen,
                           area,
                           estado,
                           coord_actual_dron,
                           porc_bat,
                           *arg, 
                           **args):
        #detalles fuego
        self.ui.label_fecha_inicio.setText(str(fecha_hora_inicio))
        self.ui.label_categoria.setText(str(categoria))
        self.ui.label_cordenadas_origen.setText(str(cordenadas_origen))
        self.ui.label_estado.setText(str(estado))
        self.ui.label_area.setText(str(area))
        #data dron
        self.ui.coord_actual_lb.setText(str(coord_actual_dron))
        self.ui.porc_bat.setText(str(porc_bat))

    def show_plot(self, canvas_plot, index_layout):
        self.plot_layout[index_layout].addWidget(canvas_plot,
                                                 1,
                                                 1)

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
    widget = Widget(8)
    widget.show()
    sys.exit(app.exec())


