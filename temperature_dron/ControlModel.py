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
        # cargando app
        ViewControl.__init__(self)
        #datos
        DatosControl.__init__(self)
        self.conection = sqlite3.connect(self.go_to("data_dir") + 'Data_Incendio.db')
        ## Creating cursor object and namimg it as cursor
        self.cursor = self.conection.cursor()
        self.open_foto_analisis(False)
        #control dron
        self.start_mision = BoolData(False, "start_mision")
        self.rtl = BoolData(False, "rtl")
        self.manual_automatico = BoolData(False, "manual_automatico")
        self.arm_disarm = BoolData(False, "arm_disarm")
        # creando timer recurrente leer data del dron
        self.timer = QTimer()
        self.timer.timeout.connect(self.cargar_datos_dron)
        self.timer.start(3/2)#segundos
        # creando timer recurrente leer y procesar fotos
        self.timer = QTimer()
        self.timer.timeout.connect(self.nueva_mision_dron_app)
        self.timer.start(0.25)#segundos
        #iniciando desde el indixe 0 en los datos
        self.static_index()

    def GuardarCambios_observaciones_evento(self):
        estimacion_to_save  = self.get_text_estimacion()
        hora_to_save = self.get_hora_estimacion()
        fecha_to_save = self.get_fecha_estimacion()
        self.cursor.execute('UPDATE INFORMACION SET FECHA=:fecha, HORA=:hora, ESTIMACION=:text WHERE ID == :id',
                           {"id":self.ID_data_show,
                            "text":estimacion_to_save,
                            "hora":hora_to_save,
                            "fecha":fecha_to_save})
        self.conection.commit()

    def CancelarCambios_observaciones_evento(self):
        self.update_estimacion_show(self.estimacion)
        self.update_fecha_show(self.fecha)
        self.update_hora_show(self.hora)

    def ArmDisarmButton_dron_evento(self):
        self.arm_disarm.setear(not(self.arm_disarm.bool_value)) 
        
    def StartMisionButton_dron_evento(self):
        self.start_mision.setear(not(self.start_mision.bool_value)) 

    def RTLButton_dron_evento(self):
        self.rtl.setear(not(self.rtl.bool_value)) 

    def ManualAutoButton_dron_evento(self):
        self.manual_automatico.setear(not(self.manual_automatico.bool_value)) 

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
        print(self.url_from_data)
        self.search_cordenates_map(self.url_from_data)
        self.update_text(*[],
                         **{"fecha_hora_inicio": self.fecha +", " + self.hora,
                         "categoria":self.categoria, 
                         "cordenadas_origen": self.coordenada_url_latitude + ", " + self.coordenada_url_longitud,
                         "estado": self.estimacion,
                         "area":self.area
                         })
        self.CancelarCambios_observaciones_evento()
        
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
        return innner
            
    @chage_index
    def siguiente(self):
        if self.index < (self.total_incendio - 1):
            self.index += 1
        return self.index
    @chage_index
    def anterior(self):
        if self.index > 0:
            self.index -= 1
        return self.index

    @chage_index
    def static_index(self):
        print ("cargando datos inicial")
        return self.index
         
    def cargar_datos_dron(self):
        self.read_actual_coordenates_dron()
        self.read_battery_dron()
        latitud = self.coordenadas_actual_dron.get("latitude")
        longitud = self.coordenadas_actual_dron.get("longitud")
        latitud_text = str(latitud[0]) + "°"  + str(latitud[1]) + "'" + str(latitud[2]) + '" N'
        longitud_text = str(longitud[0]) + "°"  + str(longitud[1]) + "'" + str(longitud[2]) + '" W'
        self.update_text_labels_dron(**{"coord_actual_dron":latitud_text + ", " + longitud_text,
                                        "porc_bat":self.bateria_dron_porc_value})

    def nueva_mision_dron_app(self):
        pass
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ejecucion = ControlModel()
    ejecucion.show()
    sys.exit(app.exec_())
