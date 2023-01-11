# This Python file uses the following encoding: utf-8
import cv2
import numpy as np
from sklearn.cluster import DBSCAN, OPTICS
from sklearn.linear_model import LinearRegression


class FiltroFotos:
    def __init__(self, foto):
        self.foto_= foto
        self.bilateral_filtro()
        self.histograma_bilateral()

    def bilateral_filtro(self):
        self.foto_bilate = cv2.bilateralFilter(self.foto_,10,80,80)

    def histograma_bilateral(self):
        self.histo_bilater = np.zeros(256, int)
        for i in range(0, self.foto_.shape[0]):
            for j in range(0, self.foto_.shape[1]):
                self.histo_bilater[self.foto_[i,j]] = self.histo_bilater[self.foto_[i,j]] + 1


class TemperaturaMax:
    def __init__(self, temp_trigger):
        self.temp_trigger = temp_trigger

    def is_max_trigger_foto(self, foto):
        max_ = 0
        for i in range(0, foto.shape[0]):
            for j in range(0, foto.shape[1]):
                if foto[i,j] > max_:
                    max_ = foto[i,j]
        if max_>=self.temp_trigger:
            return True
        else:
            return False

class RGBToTemperatureScale:
    def __init__(self):
        self.puntos_temp_RGB = {"60.0":[251,249,249],
                                "60.00":[252,250,250],
                                "60":[252,249,249],
                                "15.30":[1,1,1],
                                "15.300":[6,2,2],
                                "15.3":[9,0,0],
                                
                                "50.0":[252,251,251],
                                "50.01":[250,250,250],
                                "50":[253,248,248],
                                "14.8":[2,1,1],
                                "14.800":[2,0,0],
                                "14.80":[1,2,2],
                                
                                "57.4":[253,252,252],
                                "57.40":[249,250,250],
                                "57.400":[250,249,249],
                                "9.300":[0,1,1],
                                "9.30":[2,1,1],
                                "9.3":[9,0,0]                               
                                }
        Y_matrix = list()
        X_matrix = list()
        for key, values in self.puntos_temp_RGB.items():
            Y_matrix.append(float(key))
            X_matrix.append(values)
        Y_matrix = np.array(Y_matrix)
        X_matrix = np.array(X_matrix)
        self.regresion_model = LinearRegression().fit(X_matrix, Y_matrix)


class CalibrateFoto():
    def calibrate(self, foto, mtx, dist):
        self.cameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx,
                                                          dist,
                                                          (foto.shape[1], foto.shape[0] ),
                                                          1,
                                                          (foto.shape[1] , foto.shape[0]))
        mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, self.cameramtx, (foto.shape[1], foto.shape[0]), 5)
        foto_calibrada = cv2.remap(foto, mapx, mapy, cv2.INTER_LINEAR)
        # crop the image
        x, y, w, h = roi
        foto_calibrada_recortada = foto_calibrada[y:y+h, x:x+w]
        # dibujando cuadrado en la imagen calibrada del area de interes
        for j in range(x, x + w):
            for doble_linea in range(0, 2):
                foto_calibrada[y + doble_linea, j] = [239,184,16]
                foto_calibrada[y + h + doble_linea, j] = [239,184,16]
        for i in range(y, y + h):
            for doble_linea in range(0, 2):
                foto_calibrada[i, x + doble_linea] = [239,184,16]
                foto_calibrada[i, x + w + doble_linea] = [239,184,16]
        return foto_calibrada, foto_calibrada_recortada 
        
    def get_foto_3d_from_2d(self,foto, altura, cameramtx):
        # z es constante a la altura de la imagen
        u_v = 
        for i in range(0, foto.shape[0]):
            for j in range(0,foto.shape[1]):
                vector_pixel_2d_posicion = np.matrix([[i], [j], [altura]])
                foto_3d_from_2d = np.linalg.solv(self.cameramtx, vector_pixel_2d_posicion)
                self.foto_3d_from_2d[i][j][0] = foto_3d_from_2d[0]
                self.foto_3d_from_2d[i][j][1] = foto_3d_from_2d[1]
                self.foto_3d_from_2d[i][j][2] = foto_3d_from_2d[2]

class Segmentacion():
    def __init__(self, foto_calibrada,
                distancia,
                min_group_pixel_size,
                *arg,
                **args):

        #reshaping foto from 3 dimensions to 2 dimensions
        self.foto_reshaped = self.foto_calibrada_recortada_segmentada.reshape((-1,3))
        #converting to float
        self.foto_reshaped = np.float32(self.foto_reshaped)
        self.distancia = distancia
        self.min_group_pixel_size = min_group_pixel_size
        self.colores_dictionario_labels = {}

    def segmentacion(self):
        self.clustering = DBSCAN(eps = self.distancia, min_samples = self.min_group_pixel_size, p = 3)
        self.clustering.fit(self.foto_reshaped)
        self.reshaped_result = self.clustering.labels_.reshape((self.foto_calibrada_recortada_segmentada.shape[0], self.foto_calibrada_recortada_segmentada.shape[1]))
        #redrwing picture
        for i in range(0, self.foto_calibrada_recortada_segmentada.shape[0]):
            for j in range(0, self.foto_calibrada_recortada_segmentada.shape[1]):
                if self.colores_dictionario_labels.get(self.reshaped_result[i, j]) is None:
                    self.colores_dictionario_labels[self.reshaped_result[i, j]] = self.foto_calibrada_recortada_segmentada[i, j]
                else:
                    #self.colores_dictionario_labels[self.reshaped_result[i, j]] = (self.colores_dictionario_labels.get(self.reshaped_result[i, j]) + self.foto__[i, j])/2
                    self.foto_calibrada_recortada_segmentada[i, j] = self.colores_dictionario_labels.get(self.reshaped_result[i, j])
        cv2.imshow("segmentacion", self.foto_calibrada_recortada_segmentada)
