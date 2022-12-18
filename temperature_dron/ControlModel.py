# This Python file uses the following encoding: utf-8
import os
import sys
from PySide6.QtWidgets import QApplication
from ViewControl import ViewControl
from PIL import Image as im
from DataModel import DatosControl
import sqlite3

class ControlModel(ViewControl, DatosControl):

    def __init__(self, *arg, **args):
        print("inicializando Controlador ")
        self.index = 0
        self.current_dir = os.path.abspath(os.path.dirname( __file__ ))
        # cargando app
        ViewControl.__init__(self)
        self.search_cordenates_map()
        #datos
        DatosControl.__init__(self,*[],
                                      **{"path" : self.current_dir,
                                         "carpeta_fotos_analisis" : "fotos_analisis",
                                         "carpeta_fotos_chesspattern" : "fotos_chess_pattern",
                                         "carpeta_gui" : "temperature_dron",
                                         "carpeta_data" : "data",
                                         "instriscic_pkl" : r"\registed_data_instricic.pkl"
                                         }
                             )
        self.database_dir = self.current_dir.replace("temperature_dron", "data/")
        self.conection = sqlite3.connect(self.database_dir + 'Data_Incendio.db')
        ## Creating cursor object and namimg it as cursor
        self.cursor = self.conection.cursor()


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
    def load_data_show(self, index):
        ID_data_show  = self.imagenes_procesamiento[index].ID_data
        data_cursor = self.cursor.execute('SELECT FECHA, HORA, CATEGORIA, AREA, ESTIMACION FROM INFORMACION WHERE ID == :id',
                                         {"id":ID_data_show})
        self.fecha, self.hora, self.categoria, self.area, self.estimacion = data_cursor.fetchone()
        data_cursor = self.cursor.execute('SELECT GRADOS, MINUTOS, SEGUNDOS FROM COORDENADA_LATITUDE WHERE ID == :id',
                                         {"id":ID_data_show})
        self.grados_latitude, self.minutos_latitude, self.segundos_latitude = data_cursor.fetchone()
        data_cursor = self.cursor.execute('SELECT GRADOS, MINUTOS, SEGUNDOS FROM COORDENADAs_LONGITUD WHERE ID == :id',
                                         {"id":ID_data_show})
        self.grados_longitud, self.minutos_longitud, self.segundos_longitud = data_cursor.fetchone()

    def update(self):
        self.search_cordenates_map(self.url_from_data)
        self.update_text_labels(*[],
                                **{"fecha_hora_inicio": self.fecha +"/" + self.hora,
                                  "categoria":self.categoria, 
                                  "cordenadas_origen": self.coordenada_url_latitude + ", " + self.coordenada_url_longitud,
                                  "estado": self.estimacion,
                                  "coord_actual_dron": self.coordenada_url_latitude + ", " + self.coordenada_url_longitud,
                                  "porc_bat":45,
                                  "area":self.area
                                  })
    def build_url(self):
        semi_url_domain = "https://www.google.com/maps/place/"
        self.coordenada_url_latitude = str(self.grados_latitude) + "°" + str(self.minutos_latitude) + "'" + str(self.segundos_latitude) + '"' + "N"
        self.coordenada_url_longitud = str(self.grados_longitud) + "°" + str(self.minutos_longitud) + "'" + str(self.segundos_longitud) + '"' + "W"
        self.url_from_data = semi_url_domain + self.coordenada_url_latitude  + "+" + self.coordenada_url_longitud

    def chage_index(func):
        def innner(self, *arg,**args):
            index = func(self, *arg,**args)
            self.load_data_show(index)
            self.build_url()
            self.update()
            
    @chage_index
    def siguiente(self):
        if self.index < self.total_incendio:
            self.index += 1
        return self.index
    @chage_index
    def anterior(self):
        if self.index >= 0:
            self.index -= 1
        return self.index            
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ejecucion = ControlModel()
    ejecucion.show()
    sys.exit(app.exec_())
