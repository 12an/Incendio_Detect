# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QUrl, QDate, QTime
from PySide6 import QtGui
from PySide6.QtWebEngineWidgets import *
from PySide6.QtWebEngineCore import *
from widget import Widget
from cv2 import cvtColor, COLOR_RGB2BGR
import matplotlib
# specify the use of PySide
matplotlib.use('QtAgg')


# import the figure canvas for interfacing with the backend
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

# import 3D plotting
from mpl_toolkits.mplot3d import Axes3D    # @UnusedImport
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111, projection='3d')
        self.axes.set_xlabel('X Label')
        self.axes.set_ylabel('Y Label')
        self.axes.set_zlabel('Z Label')
        super(MplCanvas, self).__init__(fig)


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
        self.ui.CancelarCambios.clicked.connect(self.CancelarCambios_observaciones_evento)
        self.ui.GuardarCambios.clicked.connect(self.GuardarCambios_observaciones_evento)
        self.ui.SiguienteCalibracion.clicked.connect(self.Siguiente_Calibracion_evento)
        self.ui.CalcularCalibracion.clicked.connect(self.Calcular_Calibracion_evento)
        self.ui.tabWidget.currentChanged.connect(self.onChange)
        self.ui.tabWidget.blockSignals(False) #now listen the currentChanged signal
        # imagen tab 3 detalles
        self.fotos = list()
        for obj in range(0,4):
            temp = QLabel()
            self.fotos.append(temp)
        self.ui.Foto_Camara.addWidget(self.fotos[0],
                                      1,
                                      1)
        self.ui.ImagenProcesada.addWidget(self.fotos[1],
                                          1,
                                          1)
        self.ui.Foto_calibracion_antes.addWidget(self.fotos[2],
                                          1,
                                          1)
        self.ui.Foto_calibracion_despues.addWidget(self.fotos[3],
                                          1,
                                          1)
        #mapa
        self.web_view = QWebEngineView()
        self.web_view.settings()
        self.ui.web_mapa.addWidget(self.web_view,
                                  1,
                                  1)
        self.size_imaenes_view = {"Foto_Camara":(self.fotos[0], [381, 248]), 
                                  "ImagenProcesada":(self.fotos[1], [381, 248]),
                                  "Foto_calibracion_antes":(self.fotos[2], [441, 501]),
                                  "Foto_calibracion_despues":(self.fotos[3], [441, 501])}
        #plot para 3d puntos
        '''self.local_3d_word_plot = MplCanvas(self, width=5, height=4, dpi=100)
        self.plot_size_view = {"local_3d_word_plot":self.local_3d_word_plot
            }
        self.ui.mapa_3d.addWidget(self.local_3d_word_plot,
                                  1,
                                  1)  '''     

    def Show_frames(self, frame, foto_name):
        """
        Parameters
        ----------
        frame : foto, nparray
        foto_name : str
            nombre de foto.

        Returns
        -------
        None.

        """
        frame = cvtColor(frame, COLOR_RGB2BGR)
        layout, foto_size = self.size_imaenes_view.get(foto_name)
        foto_ancho, foto_largo = foto_size
        try:
            bytesPerLine = frame.shape[1] * frame.shape[2]
            ima = QtGui.QImage(frame,
                               frame.shape[1],
                               frame.shape[0],
                               bytesPerLine,
                               QtGui.QImage.Format_RGB888)
            imagen = QtGui.QPixmap.fromImage(ima)
            imagen = imagen.scaled(foto_ancho, foto_largo, Qt.KeepAspectRatio)
            layout.setPixmap(imagen)
        except AttributeError as error_list:
            print(error_list)

    def search_cordenates_map(self, cordenada):
        self.web_view.load(QUrl(cordenada))
        self.web_view.show()
    def update_text(self,
                    fecha_hora_inicio,
                    categoria,
                    cordenadas_origen,
                    area,
                    estado, 
                    **args):
        #detalles fuego
        self.ui.label_fecha_inicio.setText(str(fecha_hora_inicio))
        self.ui.label_categoria.setText(str(categoria))
        self.ui.label_cordenadas_origen.setText(str(cordenadas_origen))
        self.ui.label_area.setText(str(area) + " M2")
        self.ui.textBrowser.setText(str(estado))

    def update_text_labels_dron(self,
                           coord_actual_dron,
                           porc_bat, 
                           **args):
        #data dron
        self.ui.coord_actual_lb.setText(str(coord_actual_dron))
        self.ui.porc_bat.setText(str(porc_bat) + "%")
        
    def update_hora_show(self, hora):
        qtime = QTime.fromString(hora, "HH:mm")
        self.ui.horaEdit.setTime(qtime)

    def get_hora_estimacion(self):
        curent_t = self.ui.horaEdit.time()
        #  HH:MM:SS  , eg 10:45:28
        return curent_t.toString("HH:mm")
        
    def update_fecha_show(self, fecha):
        qdate = QDate.fromString(fecha, "dd-MM-yyyy")
        self.ui.fechaEdit.setDate(qdate)

    def get_fecha_estimacion(self):
        curent_d = self.ui.fechaEdit.date()
        return curent_d.toString("dd-MM-yyyy")
    
    def update_estimacion_show(self, estimacion):
        self.ui.textEdit.setPlainText(estimacion)

    def get_text_estimacion(self):
        return self.ui.textEdit.toPlainText()

    def show_plot_3d(self, x, y, z, layout):
        '''plot_object = self.plot_size_view.get(layout)
        plot_object.axes.scatter(x, y, z)'''
        pass


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

    def GuardarCambios_observaciones_evento(self):
        pass

    def CancelarCambios_observaciones_evento(self):
        pass

    def Siguiente_Calibracion_evento(self):
        pass

    def Calcular_Calibracion_evento(self):
        pass

    def onChange(self,index): #changed!
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget(8)
    widget.show()
    sys.exit(app.exec())