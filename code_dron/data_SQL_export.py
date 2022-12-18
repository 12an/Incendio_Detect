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

class Data_Incendio():
    def __init__(self, foto):
        current_datetime = datetime.now()
        self.hora = current_datetime.strftime("%H:%M:%S")
        self.fecha = current_datetime.strftime("%m/%d/%Y")
        self.categoria = 0
        self.area = 0
        self.estimacion = "n/a"
        self.latitude = {"grados":0, "minutos":0, "segundos":0}
        self.longitud = {"grados":0, "minutos":0, "segundos":0}
        self.foto = foto
        self.ID = 0
        

class Data_SQL():
    def __init__(self):
        self.current_dir = os.path.abspath(os.path.dirname( __file__ ))
        self.data_dir = self.current_dir.replace("code_dron", "data/")
        self.foto_dir = self.current_dir.replace("code_dron", "fotos_analisis/")
        self.conection = sqlite3.connect(self.data_dir + 'Data_Incendio.db')
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

#para pruebas
if __name__ == "__main__":  
    current_dir = os.path.abspath(os.path.dirname( __file__ ))
    data_dir = current_dir.replace("code_dron", "data/")
    foto_dir = current_dir.replace("code_dron", "fotos_analisis/")
    conection = sqlite3.connect(data_dir + 'Data_Incendio.db')
    cursor = conection.cursor()
    data_row = cursor.execute('SELECT FECHA, HORA FROM INFORMACION WHERE ID == :id',{"id":1})
    max_id = data_row.fetchone()

        