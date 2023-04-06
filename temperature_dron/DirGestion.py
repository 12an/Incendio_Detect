# This Python file uses the following encoding: utf-8
import os
import glob
from cv2 import imwrite, imread
import pickle
import shutil

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
            except FileNotFoundError:
                print("archivo no existe")
            return variable_leida


class IncendioFolder():
    main_dir = ""
    def __init__(self, ID_, main_dir = None, new_folder = False):
        self.name_incendio_folder = "incendio_" + str(ID_)
        self.ID_ = ID_
        self.name_analisis_folder = "analisis"
        self.name_reporte_folder = "reportes"
        self.name_raw_folder = "raw"
        self.name_temporal_folder = "temporal"
        
        if isinstance(main_dir, str):
            IncendioFolder.main_dir = main_dir 
        #creando directorios
        if new_folder:
            self.create_folders()
            pass
        self.path_root = IncendioFolder.main_dir + self.name_incendio_folder + "\\"
        self.path_temporal_folder = self.path_root + self.name_temporal_folder + "\\"
        #borrar todos los archivos temporales
        for filename in os.listdir(self.path_temporal_folder):
            file_path = os.path.join(self.path_temporal_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def create_folders(self):
        os.makedirs(IncendioFolder.main_dir + self.name_incendio_folder)
        os.makedirs(self.path_root + self.name_analisis_folder)
        os.makedirs(self.path_root + self.name_reporte_folder)
        os.makedirs(self.path_root + self.name_raw_folder)
        os.makedirs(self.path_root + self.name_temporal_folder)
        

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
        return foto, self.name_incendio_folder + "\\" + self.name_raw_folder + "\\", "raw.jpeg"

    def save_temp_foto(self, foto):
        path = IncendioFolder.main_dir + self.name_incendio_folder + "\\" + self.name_raw_folder + "\\"
        DumpPumpVariable.dump(path, "temp", foto)

    @save_foto
    def save_foto_temporal_dir(self, foto, name):
        return foto, self.name_incendio_folder + "\\" + self.name_temporal_folder + "\\", name + ".jpeg"

    @save_foto
    def save_analisis_foto(self, foto):
        return foto, self.name_incendio_folder + "\\" + self.name_analisis_folder + "\\", "procesada.jpeg"

    def path_save_reporte(self):
        return IncendioFolder.main_dir + self.name_incendio_folder + "\\" + self.name_reporte_folder + "\\" + self.name_incendio_folder + ".pdf"

    @open_foto
    def get_raw_foto(self):
        return self.name_incendio_folder + "\\" + self.name_raw_folder + "\\", "raw.jpeg"

    def get_temp_foto(self):
        #optenemos un array que representa la temperatura
        path = IncendioFolder.main_dir + self.name_incendio_folder + "\\" + self.name_raw_folder + "\\"
        return DumpPumpVariable.pump(self, path, "temp")

    @open_foto
    def open_foto_temporal_dir(self, name):
        return self.name_incendio_folder + "\\" + self.name_temporal_folder + "\\", name + ".jpeg"
