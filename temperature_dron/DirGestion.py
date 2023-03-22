# This Python file uses the following encoding: utf-8
import os
import glob
from cv2 import imwrite, imread


class Path():
    def __init__(self):
        self.origen_dir = os.path.abspath(os.path.dirname( __name__ ))
        self.current_dir = self.origen_dir
        self.carpetas_dir = {"data_dir" : "data",
                             "foto_dir" : "fotos_analisis",
                             "dron_dir" : "code_dron",
                             "chess_dir" : "fotos_chess_pattern",
                             "main_dir" : "temperature_dron",
                             "fotos_spam_dir" : "fotos_analisis\\fotos_spam",
                             "reportes_dir":"reportes",
                             "wkhtmltox_dir":"wkhtmltox\\bin",
                             "temp_dir":"cache",
                             "incendios_dir":"Incendios_Detectados"
                             }
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
        return self.current_dir + '\\'
        
    def get_actual_dir(self):
        for key, value in self.carpetas_dir.items():
            if value in self.current_dir:
                self.name_actual_carpet = value

class IncendioFolder():
    main_dir = ""
    def __init__(self, ID_, main_dir = None, new_folder = False):
        self.name_main_folder = "incendio_" + str(ID_)
        self.ID_ = ID_
        self.name_analisis_folder = "analisis"
        self.name_reporte_folder = "reporte"
        if not(isinstance(main_dir, str)):
            IncendioFolder.main_dir = main_dir 
        #creando directorios
        if new_folder:
            pass

    def save_foto(func):
        def inner(self, *arg,**args):
            # charging images
            foto, path, name = func(self, *arg,**args)
            imwrite(IncendioFolder.main_dir + path + name, foto)
        return inner

    def open_foto(func):
        def inner(self, *arg,**args):
            # charging images
            path, name = func(self, *arg,**args)
            return imread(IncendioFolder.main_dir + path + name)
        return inner

    @save_foto
    def save_raw_foto(self, foto):
        return foto, self.name_main_folder + "\\" + "raw" + "\\", "raw.jpeg"

    @save_foto
    def save_temp_foto(self, foto):
        return foto, self.name_main_folder + "\\" + "raw" + "\\", "temp.jpeg"

    @save_foto
    def save_analisis_foto(self, foto):
        return foto, self.name_main_folder + "\\" + "analisis" + "\\", "procesada.jpeg"

    def path_save_reporte(self):
        return IncendioFolder.main_dir + self.name_main_folder + "\\" + "reportes" + "\\" + self.name_main_folder + ".pdf"

    @open_foto
    def get_raw_foto(self):
        return self.name_main_folder + "\\" + "raw" + "\\", "raw.jpeg"

    @open_foto
    def get_temp_foto(self):
        pass

    @open_foto
    def get_analisis_foto(self):
        return self.name_main_folder + "\\" + "analisis" + "\\", "procesada.jpeg"
