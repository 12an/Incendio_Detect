# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import math
import lepton_control
import params
import os
import glob
from cv2 import imwrite, imread
from datetime import datetime
import pickle


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.master.bind("<f>", self.run_ffc)
        #self.capturar = ttk.Button(container, text, command)

        # MainPanel を 全体に配置し、右クリックをpopup menu に対応付け
        self.lmain = tk.Label(root)
        self.lmain.pack()
        self.lmain.bind("<Button-3>", self.right_button_clicked)

        # Menu 作成
        self.m = tk.Menu(root, tearoff=0)
        self.m.add_command(label="ここの温度を表示", command=self.start_show_temp)
        self.m.add_command(label="温度非表示", command=self.stop_show_temp)
        self.m.add_separator()
        self.m.add_command(label="フラットフィールド補正(F)", command=self.run_ffc)
        self.m.add_command(label="設定", command=self.show_param_dlg)
        self.origen_dir = os.path.abspath(os.path.dirname( __name__ ))

        # lepton カメラの読み込み
        try:
            self.camera = lepton_control.Lepton()
        except:
            root.destroy()
            messagebox.showwarning("Lepton Viewer", "カメラが見つかりません\nカメラを差し直してください")
            exit()
        self.popup_point = self.point = (params.W_SIZE[0] // 2, params.W_SIZE[1] // 2)
        self.is_bell = False

    def right_button_clicked(self, event):
        current_datetime = datetime.now()
        fecha = current_datetime.strftime("%m-%d-%Y")
        hora = current_datetime.strftime("%H:%M:%S")
        imwrite(self.origen_di + "\\capture\\" + fecha + hora + ".jpeg", self.image_raw)
        with open( fecha + hora + ".pkl",'wb') as file:
            pickle.dump(self.image_temp, file)
        
    def stop_show_temp(self):
        global SHOW_TEMP_AT_POINT
        SHOW_TEMP_AT_POINT = False
        self.point = (params.W_SIZE[0] // 2, params.W_SIZE[1] // 2)

    def start_show_temp(self):
        global SHOW_TEMP_AT_POINT
        SHOW_TEMP_AT_POINT = True
        self.point = self.popup_point

    def run_ffc(self, event=None):
        self.camera.run_ffc()

    def show_lepton_frame(self):
        # get lepton image (raw) and convert it to temperature (temp)
        raw_img, temp_img = self.camera.update_frame(params.ROTATE, params.FLIP, params.COEFFICIENT, params.OFFSET)
        print(raw_img)
        # tone mapping and highlight in Red
        gray = np.interp(temp_img, (params.TONE_MIN, params.TONE_MAX), (0, 255)).astype('uint8')
        gray = np.dstack([gray, gray, gray])
        self.image_raw = raw_img
        self.image_temp = temp_img


        # resize image
        width = params.W_SIZE[0] if params.ROTATE % 2 == 0 else params.W_SIZE[1]
        height = params.W_SIZE[1] if params.ROTATE % 2 == 0 else params.W_SIZE[0]
        res = cv2.resize(gray, (width, height), interpolation=cv2.INTER_LANCZOS4)

        # get max temper in params.ROI_RECT
        scale = raw_img.shape[1] / width
        rx = np.clip(int(params.ROI_RECT[0] * scale), 0, width - 2)
        ry = np.clip(int(params.ROI_RECT[1] * scale), 0, height - 2)
        rw = np.clip(int(params.ROI_RECT[2] * scale), 1, width)
        rh = np.clip(int(params.ROI_RECT[3] * scale), 1, height)
        temp_max = np.max(temp_img[ry: ry + rh, rx: rx + rw])
        

        # draw rect
        rect = params.ROI_RECT
        if temp_max >= params.THRESHOLD:
            res = cv2.rectangle(res, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 32, 32), 3)
        else:
            res = cv2.rectangle(res, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (32, 223, 32), 3)

        # set bell
        if temp_max >= params.THRESHOLD and not self.is_bell:
            self.is_bell = True

        elif temp_max < params.THRESHOLD and self.is_bell:
            self.is_bell = False

        if params.SHOW_MAXTEMP:
            text = "MAX in ROI: {:.2f}".format(temp_max)
            res = cv2.putText(res, text, (10, 25), cv2.FONT_HERSHEY_PLAIN, 1.25, (0, 0, 0), 5, cv2.LINE_AA)
            res = cv2.putText(res, text, (10, 25), cv2.FONT_HERSHEY_PLAIN, 1.25, (255, 255, 255), 1, cv2.LINE_AA)

        if params.SHOW_CAMTEMP:
            camera_temp = self.camera.camera_temp()
            text = "CAM: {:.2f}".format(camera_temp)
            res = cv2.putText(res, text, (250, 25), cv2.FONT_HERSHEY_PLAIN, 1.25, (0, 0, 0), 5, cv2.LINE_AA)
            res = cv2.putText(res, text, (250, 25), cv2.FONT_HERSHEY_PLAIN, 1.25, (255, 255, 255), 1, cv2.LINE_AA)

        if SHOW_TEMP_AT_POINT:
            # note self.point represent the point in the displayed image (not in temp_img)
            # r_p (point*scale) is the point in temp_img (or raw image)
            scale = raw_img.shape[1] / width
            r_p = (int(self.point[0] * scale), int(self.point[1] * scale))
            shift = int(10 * scale + 1)
            point_temp = np.mean(temp_img[r_p[1]-shift: r_p[1]+shift, r_p[0]-shift: r_p[0]+shift])
            text = "{:.2f}".format(point_temp)

            pt = (self.point[0] - 28, self.point[1] - 20)
            res = cv2.putText(res, text, pt, cv2.FONT_HERSHEY_PLAIN, 1.25, (255, 255, 255), 4, cv2.LINE_AA)
            res = cv2.putText(res, text, pt, cv2.FONT_HERSHEY_PLAIN, 1.25, (32, 32, 255), 1, cv2.LINE_AA)
            b1 = (self.point[0] + 10, self.point[1] + 10)
            b2 = (self.point[0] - 10, self.point[1] - 10)
            res = cv2.rectangle(res, b1, b2, (255, 255, 255), 2, cv2.LINE_AA, 0)
            res = cv2.rectangle(res, b1, b2, (32, 32, 255), 1, cv2.LINE_AA, 0)

        
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(res))
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.lmain.after(66, self.show_lepton_frame)

    def show_param_dlg(self):
        params.SettingDlg(self.camera.tlinear)

    def on_closing(self):
        self.camera.stop_streaming()
        root.destroy()


def lut_overheat(x):
    rgb = np.array([255, round(math.pow(1.005, -x) * 128), 32], np.uint8)
    return rgb


SHOW_TEMP_AT_POINT = False


if __name__ == "__main__":
    params.init()

    root = tk.Tk()
    app = Application(master=root)
    root.title("Lepton Viewer")
    root.iconbitmap('./logo.ico')
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    app.show_lepton_frame()
    app.mainloop()
