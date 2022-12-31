# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 20:05:04 2022
agregar claves a una base de datos existente
@author: 2233a

"""
from datetime import datetime
import sqlite3
import os
from cv2 import imwrite
import pickle

class Path():
    def __init__(self):
        self.origen_dir = os.path.abspath(os.path.dirname( __name__ ))
        self.current_dir = self.origen_dir
        self.carpetas_dir = {"data_dir" : "data",
                             "foto_dir" : "fotos_analisis",
                             "dron_dir" : "code_dron",
                             "chess_dir" : "fotos_chess_pattern",
                             "main_dir" : "temperature_dron"}
        self.get_actual_dir()
    """
    optener data con una key relacionada al diccionario
        self.carpetas_dir = {"data_dir" : "data",
                             "foto_dir" : "fotos_analisis",
                             "dron_dir" : "code_dron",
                             "chess_dir" : "fotos_chess_pattern",
                             "main_dir" : "temperature_dron"}
    """
    def go_to(self, key):
        self.current_dir = self.current_dir.replace(self.name_actual_carpet,
                                                    self.carpetas_dir.get(key))
        self.name_actual_carpet = self.carpetas_dir.get(key)
        return self.current_dir + "\\"
        
    def get_actual_dir(self):
        for key, value in self.carpetas_dir.items():
            if value in self.current_dir:
                self.name_actual_carpet = value

class Data_Incendio():
    def __init__(self, foto):
        current_datetime = datetime.now()
        self.hora = current_datetime.strftime("%H:%M")
        self.fecha = current_datetime.strftime("%m-%d-%Y")
        self.categoria = 0
        self.area = 0
        self.estimacion = "n/a"
        self.latitude = {"grados":0, "minutos":0, "segundos":0}
        self.longitud = {"grados":0, "minutos":0, "segundos":0}
        self.foto = foto
        self.ID = 0

class Data_SQL(Path):
    def __init__(self):
        Path.__init__(self)
        self.conection = sqlite3.connect(self.go_to("data_dir") + 'Data_Incendio.db')
        ## Creating cursor object and namimg it as cursor
        self.cursor = self.conection.cursor()
    def guardar_datos(self, instance_data_incendio):
        data_infotable = (instance_data_incendio.fecha,
                          instance_data_incendio.hora,
                          instance_data_incendio.categoria,
                          instance_data_incendio.area,
                          instance_data_incendio.area,
                          instance_data_incendio.estimacion)
        self.cursor.execute("INSERT INTO INFORMACION(FECHA, HORA, CATEGORIA, AREA, ESTIMACION) VALUES(?,?,?,?,?)", data_infotable)
        self.conection.commit()
        self.data_row = self.cursor.execute('SELECT max(ID) FROM INFORMACION')
        max_id = self.data_row.fetchone()[0]
        instance_data_incendio.ID = max_id
        data_latitudetable = (max_id,
                             instance_data_incendio.latitude.get("grados"),
                             instance_data_incendio.latitude.get("minutos"),
                             instance_data_incendio.latitude.get("segundos"))
        data_longitudtable = (max_id,
                             instance_data_incendio.longitud.get("grados"),
                             instance_data_incendio.longitud.get("minutos"),
                             instance_data_incendio.longitud.get("segundos"))
        self.cursor.execute("INSERT INTO COORDENADA_LATITUDE(ID, GRADOS, MINUTOS, SEGUNDOS) VALUES(?,?,?,?)",data_latitudetable)
        self.conection.commit()
        self.cursor.execute("INSERT INTO COORDENADAS_LONGITUD(ID, GRADOS, MINUTOS, SEGUNDOS) VALUES(?,?,?,?)",data_longitudtable)
        self.conection.commit()
        #GUARDANDO FOTO
        imwrite(self.foto_dir + str(max_id) + ".png", instance_data_incendio.foto)

class DumpPumpVariable():
    def dump(self, directorio, variable_name, variable):
        with open(directorio + variable_name + ".pkl" , "wb") as saving:
            pickle.dump(variable, saving)
    def pump(self, directorio, variable_name):
        with open(directorio + variable_name + ".pkl", "rb") as reading:
            variable_leida = 0
            try:
                variable_leida = pickle.load(reading)
            except EOFError as nothing_in_file:
                print("there is nothing in the file, of data:")
                print(nothing_in_file)
            return variable_leida
        
class coordenada_data(Path, DumpPumpVariable):
    def __init__(self):
        Path.__init__(self)
        self.value = {"latitude": [0,0,0], "longitud": [0,0,0]}
        self.variable_name = "coordenadas_dron"

    def __get__(self, obj, objtype):
        return self.value
        
    def __set__(self, obj, value):
        self.value = value
        self.dump(self.go_to("data_dir"), self.variable_name, self.value)

class integer_data(Path, DumpPumpVariable):
    def __init__(self):
        Path.__init__(self)
        self.value = 0
        self.variable_name = "bateria_data_dron"

    def __get__(self, obj, objtype):
        return self.value
        
    def __set__(self, obj, value):
        self.value = value
        
        self.dump(self.go_to("data_dir"), self.variable_name, self.value)

class bool_data(Path, DumpPumpVariable):
    def __init__(self):
        Path.__init__(self)
        self.value = False
        self.variable_name = "mision_status"

    def __get__(self, obj, objtype):
        return self.value
        
    def __set__(self, obj, value):
        self.value = value
        
        self.dump(self.go_to("data_dir"), self.variable_name, self.value)

class DronData():
    bateria_porcentage = integer_data() 
    coordenadas = coordenada_data()

#para pruebas
if __name__ == "__main__":
    text_path = Path()
    dron_variables = DronData()
    dron_variables.bateria_porcentage = 78
    dron_variables.coordenadas = {"latitude": [0,0,0], "longitud": [0,0,0]}
    datos_sql = Data_SQL()
    FOTO = "aqui va la foto"
    read_bool = DumpPumpVariable().pump(text_path.go_to("data_dir"), "start_mision")
    incendio1 = Data_Incendio(FOTO)
    #la hora y fecha se carga automatico al momento de crear el incendio
    # el ID no se modifica (se configura automaticamente al guardar el incendio)
    #solo se agrega la coordenada, el resto de la informacion se genera en la app
    incendio1.latitude = {"grados":0, "minutos":0, "segundos":0}
    incendio1.longitud = {"grados":0, "minutos":0, "segundos":0}
    # se agrega informacion a ese incendio
    datos_sql.guardar_datos(incendio1)
    
    
       