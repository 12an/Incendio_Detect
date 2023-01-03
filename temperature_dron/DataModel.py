# This Python file uses the following encoding: utf-8
import os
import glob
from cv2 import imwrite, imread, cvtColor, COLOR_RGB2BGR
import pickle


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


class Path():
    def __init__(self):
        self.origen_dir = os.path.abspath(os.path.dirname( __name__ ))
        self.current_dir = self.origen_dir
        self.carpetas_dir = {"data_dir" : "data",
                             "foto_dir" : "fotos_analisis",
                             "dron_dir" : "code_dron",
                             "chess_dir" : "fotos_chess_pattern",
                             "main_dir" : "temperature_dron",
                             "fotos_spam_dir" : "fotos_analisis\\fotos_spam",}
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
        self.current_dir = self.current_dir.replace(self.name_actual_carpet + "\\",
                                                    self.carpetas_dir.get(key))
        self.name_actual_carpet = self.carpetas_dir.get(key)
        return self.current_dir + "\\"
        
    def get_actual_dir(self):
        for key, value in self.carpetas_dir.items():
            if value in self.current_dir:
                self.name_actual_carpet = value


class Quantity:
    def __init__(self, managed_attribute_name):
        print(f'managing attribute {managed_attribute_name}')
        self._managed_attribute_name = managed_attribute_name

    def __get__(self, instance, owner):
        print(f'{self._managed_attribute_name} get')
        return instance.__dict__[self._managed_attribute_name]

    def __set__(self, instance, value):
        print(f'{self._managed_attribute_name} set {value}')
        if value > 0:
            instance.__dict__[self._managed_attribute_name] = value


class BoolData(Path, DumpPumpVariable):
    def __init__(self, value, variable_name):
        Path.__init__(self)
        self.variable_name = variable_name
        self.bool_value = value

    def setear(self, value):
        self.bool_value = value
        self.dump(self.go_to("data_dir"), self.variable_name, self.bool_value )


class IncendioData():
    def __init__(self,foto_camara,
                 ID_data,
                 *arg,
                 **args):
        self.ID_data = ID_data
        self.foto_camara = foto_camara
        self.foto_fitro = None
        self.foto_undistorted = None
        self.matrix_foto = None
        self.foto_temperatura_scaled = None


class Data_SQL(Path):
    def __init__(self):
        Path.__init__(self)
        self.conection = sqlite3.connect(self.go_to("data_dir") + 'Data_Incendio.db')
        ## Creating cursor object and namimg it as cursor
        self.cursor = self.conection.cursor()
        self.ID_actual_sql_management = 0

    def get_max_id(self):
        self.data_row = self.cursor.execute('SELECT max(ID) FROM INFORMACION')
        return max_id self.data_row.fetchone()[0]
         
    def guardar_nuevo_incendio_datos(self,
                                     fecha,
                                     hora,
                                     categoria,
                                     area,
                                     estimacion,
                                     latitude,
                                     longitud,
                                     foto_normal,
                                     **{}):
        informacion_row = (fecha, hora, categoria, area, estimacion)
        self.cursor.execute("INSERT INTO INFORMACION(FECHA, HORA, CATEGORIA, AREA, ESTIMACION) VALUES(?,?,?,?,?)", informacion_row)
        self.conection.commit()
        max_id = self.get_max_id()
        data_latitude_row = (max_id,
                             latitude.get("grados"),
                             latitude.get("minutos"),
                             latitude.get("segundos"))
        data_longitud_row = (max_id,
                             longitud.get("grados"),
                             longitud.get("minutos"),
                             longitud.get("segundos"))
        self.cursor.execute("INSERT INTO COORDENADA_LATITUDE(ID, GRADOS, MINUTOS, SEGUNDOS) VALUES(?,?,?,?)",data_latitudetable)
        self.conection.commit()
        self.cursor.execute("INSERT INTO COORDENADAS_LONGITUD(ID, GRADOS, MINUTOS, SEGUNDOS) VALUES(?,?,?,?)",data_longitudtable)
        self.conection.commit()
        #GUARDANDO FOTO
        imwrite(self.go_to("foto_dir") + str(max_id) + ".png", foto_normal)

    def update(func):
        def inner(self, *arg, **args):
            query, data = func(self, *arg, **args)
            self.cursor.execute(query, data)
            self.conection.commit()
        return inner

    def leer():
        def inner(self, *arg, **args):
            query = func(self, *arg, **args)
            data_cursor = self.cursor.execute(query, {"id":self.ID_data_show})
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
    def hora(self):
        return 'SELECT HORA FROM INFORMACION WHERE ID == :id'

        @leer
    def fecha(self):
        return 'SELECT FECHA FROM INFORMACION WHERE ID == :id'

        @leer
    def latitude(self):
        return 'SELECT GRADOS, MINUTOS, SEGUNDOS FROM COORDENADA_LATITUDE WHERE ID == :id'

        @leer
    def longitude(self):
        return 'SELECT GRADOS, MINUTOS, SEGUNDOS FROM COORDENADAs_LONGITUD WHERE ID == :id'

        @leer
    def categoria(self):
        return 'SELECT CATEGORIA FROM INFORMACION WHERE ID == :id'

        @leer
    def area(self):
        return 'SELECT AREA FROM INFORMACION WHERE ID == :id'

        @leer
    def estimacion(self):
        return 'SELECT ESTIMACION FROM INFORMACION WHERE ID == :id'


class FotoChesspatternData():
    def __init__(self, id_foto, foto):
        self.id_foto = id_foto
        self.agregada = False
        self.foto = foto


class CameraIntrics():
    def __init__(self):
        self.ret = None
        self.mtx = None
        self.dist = None
        self.rvecs = None
        self.tvecs = None


class DatosControl(Path,
                   DumpPumpVariable,
                   CameraIntrics,
                   Data_SQL):
    def __init__(self):
        Path.__init__(self)
        CameraIntrics.__init__(self)
        Data_SQL.__init__(self)
        print("inicializando DatosControl ")
        self.imagenes_chesspattern = list()
        self.imagenes_procesamiento = list()
        self.read_instricic_camera()
        self.total_incendio = 0
        self.total_fotos_chesspattern = 0
        self.bateria_dron_porc_value = 0
        self.coordenadas_actual_dron = {}

    def open_(func):
        def inner(self, *arg,**args):
            # charging images
            path, tipo_imagen = func(self, *arg,**args)
            for path_name_foto in glob.iglob(path + "\*.jpg"):
                #al path le quitamos el nombre del archiv0
                name_foto = path_name_foto[len(path) : ]               
                ID_data = name_foto[:-4]
                imagen = cvtColor(imread(path_name_foto), COLOR_RGB2BGR)
                if(tipo_imagen==1):
                    self.total_incendio += 1
                    self.imagenes_procesamiento.append(IncendioData(*[],
                                                                    **{"foto_camara":imagen,
                                                                       "ID_data": ID_data
                                                                       }))
                if(tipo_imagen==2):
                    self.total_fotos_chesspattern += 1
                    self.imagenes_chesspattern.append(
                                                      FotoChesspatternData(ID_data, imagen)
                                                      )
        return inner

    @open_
    def open_foto_analisis(self, path = False):
        if isinstance(path, bool):
            return self.go_to("foto_dir"), 1
        else:
            return path, 1

    @open_
    def open_foto_chesspattern(self, path = False):
        if isinstance(path, bool):
            path = self.path_directory
            return self.go_to("chess_dir"), 2
        else:
            return path, 2

    def get_registed_camera_instricic(self, path = False):
        pass

    def save_registed_camera_instricic(self, ):
        pass

    def save_instricic_camera(self):
        self.dump(self.go_to("data_dir"),
                  "registed_data_instricic",
                  [self.ret, self.mtx, self.dist, self.rvecs, self.tvecs])

    def read_instricic_camera(self):
        packet = self.pump(self.go_to("data_dir"), "registed_data_instricic")
        try:
            self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = packet
        except ValueError as nothing_in_file:
            print("parece que no se ha guardado")
            print(nothing_in_file)

    def read_battery_dron(self):
        self.bateria_dron_porc_value = self.pump(self.go_to("data_dir"), "bateria_data_dron")
        return self.bateria_dron_porc_value

    def read_actual_coordenates_dron(self):
        self.coordenadas_actual_dron = self.pump(self.go_to("data_dir"), "coordenadas_dron")
        return self.coordenadas_actual_dron

    def status_mision(self):
        self.mision_status = self.pump(self.go_to("data_dir"), "mision_status")
        return self.mision_status

    def foto_spam(self):
        return cvtColor(imread(self.go_to("fotos_spam_dir") + "spam.png"), COLOR_RGB2BGR)