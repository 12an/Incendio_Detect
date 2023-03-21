# This Python file uses the following encoding: utf-8
import cv2
import numpy as np
from sklearn.cluster import DBSCAN, OPTICS
from sklearn.linear_model import LinearRegression
import math as mt


class FiltroFotos:
    def __init__(self, foto):
        self.foto_= foto
        self.bilateral_filtro()
        self.histograma_bilateral()

    def bilateral_filtro(self):
        self.foto_bilate = cv2.bilateralFilter(self.foto_,26,80,80)

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


class CalibrateFoto():
    def calibrate(self, foto, mtx, dist):
        cameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx,
                                                          dist,
                                                          (foto.shape[1], foto.shape[0] ),
                                                          1,
                                                          (foto.shape[1] , foto.shape[0]))
        mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, cameramtx, (foto.shape[1], foto.shape[0]), 5)
        foto_calibrada = cv2.remap(foto, mapx, mapy, cv2.INTER_LINEAR)
        foto_calibrada_cuadrado = np.copy(foto_calibrada, order = "K", subok = True)
        # crop the image
        x, y, w, h = roi
        foto_calibrada_recortada = np.copy(foto_calibrada[y:y+h, x:x+w], order = "K", subok = True)
        # dibujando cuadrado en la imagen calibrada del area de interes
        for j in range(x, x + w):
            for doble_linea in range(0, 1):
                foto_calibrada_cuadrado[y + doble_linea, j] = [239,184,16]
                foto_calibrada_cuadrado[y + h + doble_linea, j] = [239,184,16]
        for i in range(y, y + h):
            for doble_linea in range(0, 1):
                foto_calibrada_cuadrado[i, x + doble_linea] = [239,184,16]
                foto_calibrada_cuadrado[i, x + w + doble_linea] = [239,184,16]
        return foto_calibrada, foto_calibrada_recortada, roi

    def get_foto_3d_from_2d(self, ft, cameramtx, altura):
        # z es constante a la altura de la imagen
        Zw = altura
        foto = np.zeros_like(ft, dtype = None, order = "K", subok = True)
        foto = foto.astype('float64')
        cameramtrix = np.copy(cameramtx, order = "K", subok = True)
        cameramtrix = cameramtrix
        fx = cameramtrix[0,0]
        fy = cameramtrix[1,1]
        cx = cameramtrix[2,0]
        cy = cameramtrix[2,1]
        for i in range(0,ft.shape[0]):
            for j in range(0,ft.shape[1]):
                xw = ((i - cx)/fx)*Zw
                yw = ((j - cy)/fy)*Zw
                foto[i, j] =[xw, yw, Zw]
        return foto

    def area_foto(self, puntos_interes,
                  foto_word_view):
        area = 0
        foto_3d_view = np.copy(foto_word_view, order = "K", subok = True)
        foto_3d_view = foto_3d_view.astype('float64')
        #se medira desde izquierda derecha, arriba abajo, 
        #cuadrado abcd
        #area basada en trangulos abc y adc (por si las distancias son irregulares)
        for punto in puntos_interes:
            #punto a es el punto generado de la lista
            #punto b es punto correspondiente al i + 1
            #punto c es el punto j - 1
            #punto d es i + 1, j - 1
            a = foto_3d_view[punto[0], punto[1]]
            b = foto_3d_view[punto[0] + 1, punto[1]]
            c = foto_3d_view[punto[0], punto[1] - 1]
            d = foto_3d_view[punto[0] + 1, punto[1] - 1]
            distancia_ab = self.distancia(a, b)
            distancia_bc = self.distancia(b, c)
            distancia_ac = self.distancia(a, c)
            distancia_bd = self.distancia(b, d)
            distancia_dc = self.distancia(d, c)
            area_abc = self.area_heron_triangulo(distancia_ab,
                                         distancia_bc,
                                         distancia_ac)
            area_bdc = self.area_heron_triangulo(distancia_bd,
                                         distancia_dc,
                                         distancia_ac)             
            area +=  area_abc + area_bdc
        return area / 1.95

    def distancia(self, a, b):
        return mt.sqrt(mt.pow((a[0] - b[0]), 2) + mt.pow((a[1] - b[1]), 2))

    def area_heron_triangulo(self, a, b, c):
        #calculo area en base formula heron
        s = (a + b + c)/2
        return mt.sqrt(mt.fabs((s * (s - a) * (s - b) * (s - c))))

    def plot_3d(self, puntos_interes, foto_word_view):
        foto_3d_view = np.copy(foto_word_view, order = "K", subok = True)         
        for punto in puntos_interes:
            x = foto_3d_view[punto[0], punto[1]][0]
            y = foto_3d_view[punto[0], punto[1]][1]
            z = foto_3d_view[punto[0], punto[1]][2]
        return x, y, z 

class Segmentacion():
    def __init__(self,
                distancia,
                temp_incendio,
                **args):
        self.distancia_puntos = distancia
        self.temp_incendio = temp_incendio

    def segmentacion(self,
                     foto_temperatura_scalada,
                     foto_undistorted,
                     ROI):
        x, y, w, h = ROI
        foto_undistorted_c = np.zeros_like(foto_undistorted, order = "K", subok = True)        
        incendio = []
        #redrwing picture
        for i in range(0, foto_temperatura_scalada.shape[0]):
            for j in range(0, foto_temperatura_scalada.shape[1]):
                if foto_temperatura_scalada[i,j]>= (self.temp_incendio):
                    incendio.append([i, j])
                    foto_undistorted_c[y + i, j + x] = foto_undistorted[y + i, j + x]
        return incendio, foto_undistorted_c



                
