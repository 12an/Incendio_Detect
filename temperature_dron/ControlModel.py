# This Python file uses the following encoding: utf-8
import os
import sys
from PySide6.QtWidgets import QApplication
from ViewControl import ViewControl
from DataModel import DatosControl, BoolData
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
        DatosControl.__init__(self)
        self.database_dir = self.current_dir.replace("temperature_dron", "data/")
        self.conection = sqlite3.connect(self.database_dir + 'Data_Incendio.db')
        ## Creating cursor object and namimg it as cursor
        self.cursor = self.conection.cursor()
        #control dron
        self.start_mision = BoolData(False, "start_mision")
        self.rtl = BoolData(False, "rtl")
        self.manual_automatico = BoolData(False, "manual_automatico")
        self.arm_disarm = BoolData(False, "arm_disarm")
        
        # creando timer recurrente leer data del dron
        self.timer = QTimer()
        self.timer.timeout.connect(self.cargar_datos_dron)
        self.timer.start(3/2)#segundos 

    def GuardarCambios_observaciones_evento(self):
        estimacion_to_save  = self.get_text_estimacion()
        hora_to_save = self.get_hora_estimacion()
        fecha_to_save = self.get_fecha_estimacion()
        self.cursor.execute('INSERT INTO INFORMACION(FECHA, HORA, ESTIMACION) VALUES(:text, :"hora", "fecha") WHERE ID == :id',
                           {"id":self.ID_data_show,
                            "text":estimacion_to_save,
                            "hora":hora_to_save,
                            "fecha":fecha_to_save})
        self.conection.commit()

    def CancelarCambios_observaciones_evento(self):
        data_row = self.cursor.execute('SELECT FECHA, HORA, ESTIMACION FROM INFORMACION WHERE ID == :id',
                                          {"id":self.ID_data_show})
        fecha, hora, estimacion = data_row.fetchone()
        
        self.update_estimacion_show(estimacion)
        self.update_fecha_show(fecha)
        self.update_hora_show(hora)

    def ArmDisarmButton_dron_evento(self):
        self.arm_disarm.value = not(self.arm_disarm.value)
        
    def StartMisionButton_dron_evento(self):
        self.start_mision.value = not(self.start_mision.value)

    def RTLButton_dron_evento(self):
        self.rtl.value = not(self.rtl.value)

    def ManualAutoButton_dron_evento(self):
        self.manual_automatico.value = not(self.manual_automatico.value)

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
