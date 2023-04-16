# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 08:24:28 2023

@author: 2233a
"""
from SendSocket import SendSocket
from ReceiveSocket import MyTCPHandler
from socketserver  import TCPServer
import lepton_control
import numpy as np
import threading
import time

class CamaraStreaming(SendSocket):
    def __init__(self, HOST, PORT):
        SendSocket.__init__(self, HOST, PORT)
        try:
            self.camera = lepton_control.Lepton()
        except:
            print("Revisa la coneccion de la camera")

    def send_imagen(self):
        try:
            # get lepton image (raw) and convert it to temperature (temp)
            raw_img, temp_img = self.camera.update_frame()
        except:
            raw_img = np.asarray((160,120))
            temp_img = np.asarray((160,120))
        # tone mapping and highlight in Red
        print("ejecutando camera streaming")
        gray = np.interp(temp_img, (20.0, 40.0), (0, 255)).astype('uint8')
        dict_data = {"pic":self.list_wraping(raw_img),
                     "temp":self.list_wraping(gray)}
        self.send_data(dict_data)

    def list_wraping(self, data_array):
        array = list()
        for i in range(data_array.shape[0]):
            row = list()
            for j in range(data_array.shape[1]):
                row.append(int(data_array[i, j]))
            array.append(row)
        return array

class InfoStraming(SendSocket):
    def __init__(self, HOST, PORT):
        SendSocket.__init__(self, HOST, PORT)

    def send_data(self,
                  coordenadas,
                  porcentage_bateria, 
                  altura):
        print("ejecutando info streaming")
        dict_data = {"coordenadas":coordenadas,
                     "porcentage_bateria":porcentage_bateria,
                     "altura":porcentage_bateria}
        self.send_data(dict_data)

class ComandosHandler(MyTCPHandler):
    def comandos_update(self):
        arm_disarm = self.data_recieved.get("arm_disarm")
        start_mision = self.data_recieved.get("start_mision")
        rtl = self.data_recieved.get("rtl")
        manual_auto = self.data_recieved.get("manual_auto")
        print("ejecutando ComandosHandler")
        print(arm_disarm,start_mision,rtl,manual_auto)

if __name__ == "__main__":
    camera_host = "localhost"#"192.168.100.2"
    camera_port = 1046
    comand_host = "localhost"
    comand_port = camera_port + 1
    info_host = camera_host
    info_port = camera_port + 2
    camara_streaming = False
    infostreaming = False
    server = TCPServer((comand_host, comand_port),
                       ComandosHandler)
    def camera_thread():
        global camara_streaming, camera_host, camera_port
        if isinstance(camara_streaming, bool()):
            try:
                camara_streaming = CamaraStreaming(camera_host, camera_port)
            except:
                camara_streaming = False
                print("coneccion no establecida con el servidor de camara streaming")
        else:
            camara_streaming.send_imagen()
        time.sleep(1)

    def comandos_thread():
        server.handle_request()

    def info_thread():
        """
        este hilo necesita actualizar las variables
        """
        altura = 0
        bateria_porcentage = 78
        coordenadas = {"latitude": [18,30,58], "longitud": [69,53,47]}
        global infostreaming, info_host, info_port
        if isinstance(infostreaming, bool()):
            try:
                infostreaming = InfoStraming(info_host, info_port)
            except:
                infostreaming = False
                print("coneccion no establecida con el servidor de camara streaming")
        else:      
            infostreaming.send_data(coordenadas,
                                bateria_porcentage, 
                                altura)

    camaraThread = threading.Thread(target=camera_thread)
    comandosThread = threading.Thread(target=camera_thread)
    infoThread = threading.Thread(target=camera_thread)
    camaraThread.start()
    comandosThread.start()
    infoThread.start()
    camaraThread.join()
    infoThread.join()
    comandosThread.join()
    
    
