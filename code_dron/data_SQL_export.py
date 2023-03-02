# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 20:05:04 2022
agregar claves a una base de datos existente
@author: 2233a

"""
from datetime import datetime
import sqlite3
import os
#from cv2 import imwrite
import pickle

class Path():
    def __init__(self):
        self.origen_dir = os.path.abspath(os.path.dirname( __name__ ))
        self.current_dir = self.origen_dir
        self.carpetas_dir = {"data_dir" : "data",
                             "foto_dir" : "fotos_analisis",
                             "dron_dir" : "code_dron",
                             "chess_dir" : "fotos_chess_pattern",
                             "main_dir" : "temperature_dron",
                             "fotos_spam_dir" : "fotos_analisis/fotos_spam",}
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
        return self.current_dir + "/"
        
    def get_actual_dir(self):
        for key, value in self.carpetas_dir.items():
            if value in self.current_dir:
                self.name_actual_carpet = value


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


#para pruebas
if __name__ == "__main__":
    text_path = Path()
    bateria_porcentage = 78
    coordenadas = {"latitude": [18,30,58], "longitud": [69,53,47]}
    mision_status = True
    FOTO = "aqui va la foto"
    #imwrite(text_path.go_to("fotos_spam_dir") + "spam" + ".jpeg", FOTO)

    DumpPumpVariable().dump(text_path.go_to("data_dir"), "mision_status", mision_status)
    DumpPumpVariable().dump(text_path.go_to("data_dir"), "bateria_data_dron", bateria_porcentage)
    DumpPumpVariable().dump(text_path.go_to("data_dir"), "coordenadas_dron", coordenadas)    
    
       