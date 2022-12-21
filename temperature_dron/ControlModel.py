# This Python file uses the following encoding: utf-8
import os
import sys
from PySide6.QtWidgets import QApplication
from ViewControl import ViewControl
from DataModel import DatosControl
import sqlite3
from PySide6.QtCore import QTimer

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
        
        # creando timer recurrente leer data del dron
        self.timer = QTimer()
        self.timer.timeout.connect(self.cargar_datos_dron)
        self.timer.start(3/2)#segundos 


    def ArmDisarmButton_dron_evento(self):
        pass

    def GuardarCambios_observaciones_evento(self):
        estimacion_to_save  = self.get_text_estimacion()
        self.cursor.execute('INSERT INTO INFORMACION(ESTIMACION) VALUES(:text) WHERE ID == :id',
                           {"id":self.ID_data_show, "text":estimacion_to_save})
        self.conection.commit()

    def CancelarCambios_observaciones_evento(self):
        text_mostrar = self.cursor.execute('SELECT ESTIMACION FROM INFORMACION WHERE ID == :id',
                                          {"id":self.ID_data_show})
        self.update_estimacion_show(text_mostrar)

    def StartMisionButton_dron_evento(self):
        pass

    def RTLButton_dron_evento(self):
        pass

    def ManualAutoButton_dron_evento(self):
        pass

    def GenerarReporteBotton_detalles_evento(self):
        pass
    def load_data_show(self, index):
        self.ID_data_show  = self.imagenes_procesamiento[index].ID_data
        data_cursor = self.cursor.execute('SELECT FECHA, HORA, CATEGORIA, AREA, ESTIMACION FROM INFORMACION WHERE ID == :id',
                                         {"id":self.ID_data_show})
        self.fecha, self.hora, self.categoria, self.area, self.estimacion = data_cursor.fetchone()
        data_cursor = self.cursor.execute('SELECT GRADOS, MINUTOS, SEGUNDOS FROM COORDENADA_LATITUDE WHERE ID == :id',
                                         {"id":self.ID_data_show})
        self.grados_latitude, self.minutos_latitude, self.segundos_latitude = data_cursor.fetchone()
        data_cursor = self.cursor.execute('SELECT GRADOS, MINUTOS, SEGUNDOS FROM COORDENADAs_LONGITUD WHERE ID == :id',
                                         {"id":self.ID_data_show})
        self.grados_longitud, self.minutos_longitud, self.segundos_longitud = data_cursor.fetchone()

    def update(self):
        self.search_cordenates_map(self.url_from_data)
        self.update_text_labels(*[],
                                **{"fecha_hora_inicio": self.fecha +"/" + self.hora,
                                  "categoria":self.categoria, 
                                  "cordenadas_origen": self.coordenada_url_latitude + ", " + self.coordenada_url_longitud,
                                  "estado": self.estimacion,
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
         
    def cargar_datos_dron(self):
        self.read_actual_coordenates_dron()
        self.read_battery_dron()
        self.update_text_labels_dron(**{"coord_actual_dron":self.coordenadas_actual_dron,
                                        "porc_bat":self.bateria_dron_porc_value})


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ejecucion = ControlModel()
    ejecucion.show()
    sys.exit(app.exec_())
