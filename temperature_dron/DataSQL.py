# This Python file uses the following encoding: utf-8
import os
import glob
from cv2 import imwrite, imread, cvtColor, COLOR_RGB2BGR
import sqlite3


class DataSQL():
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.conection = sqlite3.connect(self.data_dir + 'Data_Incendio.db')
        ## Creating cursor object and namimg it as cursor
        self.cursor = self.conection.cursor()
        self.current_id = 0
        self.all_ids = self.get_all_ids()

    def get_max_id(self):
        data_row = self.cursor.execute('SELECT max(ID) FROM INFORMACION')
        return data_row.fetchone()[0]

    def get_all_ids(self):
        data_row = self.cursor.execute('SELECT ID FROM INFORMACION')
        return data_row.fetchone()
         
    def nuevo_incendio_datos(self,
                             fecha,
                             hora,
                             categoria,
                             area,
                             estimacion,
                             latitude,
                             longitud,
                             foto_normal,
                             altura,
                             **args):
        informacion_row = (fecha, hora, categoria, area, estimacion, altura)
        self.cursor.execute("INSERT INTO INFORMACION(FECHA, HORA, CATEGORIA, AREA, ESTIMACION, ALTURA) VALUES(?,?,?,?,?, ?)", informacion_row)
        self.conection.commit()
        new_id = str(int(self.get_max_id()) + 1)
        data_latitude_row = (new_id,
                             latitude[0],
                             latitude[1],
                             latitude[2])
        data_longitud_row = (new_id,
                             longitud[0],
                             longitud[1],
                             longitud[2])
        self.cursor.execute("INSERT INTO COORDENADA_LATITUDE(ID, GRADOS, MINUTOS, SEGUNDOS) VALUES(?,?,?,?)",data_latitude_row)
        self.conection.commit()
        self.cursor.execute("INSERT INTO COORDENADAS_LONGITUD(ID, GRADOS, MINUTOS, SEGUNDOS) VALUES(?,?,?,?)",data_longitud_row)
        self.conection.commit()
        self.all_ids.append(new_id)
        return new_id

    def update(func):
        def inner(self, *arg, **args):
            query, data = func(self, *arg, **args)
            data.update({"id":self.current_id})
            self.cursor.execute(query, data)
            self.conection.commit()
        return inner

    def leer(func):
        def inner(self, *arg, **args):
            query, expected_variable = func(self, *arg, **args)
            data_cursor = self.cursor.execute(query, {"id":self.current_id})
            if expected_variable==1:
                return data_cursor.fetchone()[0]
            else:
                return data_cursor.fetchone()
        return inner

    @update
    def update_hora(self, value):
        return 'UPDATE  INFORMACION SET HORA=:hora WHERE ID == :id', value

    @update
    def update_fecha(self, value):
        return 'UPDATE INFORMACION SET FECHA=:fecha WHERE ID == :id', value

    @update
    def update_latitude(self, value):
        return 'UPDATE COORDENADA_LATITUDE SET GRADOS=:grados, MINUTOS=:minutos, SEGUNDOS=:segundos WHERE ID == :id', value

    @update
    def update_longitude(self, value):
        return 'UPDATE COORDENADAS_LONGITUD SET GRADOS=:grados, MINUTOS=:minutos, SEGUNDOS=:segundos WHERE ID == :id', value

    @update
    def update_categoria(self, value):
        return 'UPDATE INFORMACION SET CATEGORIA=:cateoria WHERE ID == :id', value

    @update
    def update_area(self, value):
        return 'UPDATE INFORMACION SET AREA=:area WHERE ID == :id', value

    @update
    def update_estimacion(self, value):
        return 'UPDATE INFORMACION SET ESTIMACION=:text WHERE ID == :id', value

    @leer
    def hora_sql(self):
        return 'SELECT HORA FROM INFORMACION WHERE ID == :id', 1

    @leer
    def fecha_sql(self):
        return 'SELECT FECHA FROM INFORMACION WHERE ID == :id', 1

    @leer
    def latitude_sql(self):
        return 'SELECT GRADOS, MINUTOS, SEGUNDOS FROM COORDENADA_LATITUDE WHERE ID == :id', 3

    @leer
    def longitude_sql(self):
        return 'SELECT GRADOS, MINUTOS, SEGUNDOS FROM COORDENADAs_LONGITUD WHERE ID == :id', 3

    @leer
    def categoria_sql(self):
        return 'SELECT CATEGORIA FROM INFORMACION WHERE ID == :id', 1

    @leer
    def area_sql(self):
        return 'SELECT AREA FROM INFORMACION WHERE ID == :id', 1

    @leer
    def estimacion_sql(self):
        return 'SELECT ESTIMACION FROM INFORMACION WHERE ID == :id', 1
    
    @leer
    def altura_sql(self):
        return 'SELECT ALTURA FROM INFORMACION WHERE ID == :id', 1