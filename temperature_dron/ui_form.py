# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateEdit, QFrame, QGridLayout,
    QLabel, QPlainTextEdit, QPushButton, QSizePolicy,
    QTabWidget, QTimeEdit, QWidget)

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        if not MainWidget.objectName():
            MainWidget.setObjectName(u"MainWidget")
        MainWidget.resize(852, 600)
        icon = QIcon()
        iconThemeName = u"applications-engineering"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        MainWidget.setWindowIcon(icon)
        self.tabWidget = QTabWidget(MainWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(-4, 9, 861, 591))
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tabWidget.setElideMode(Qt.ElideMiddle)
        self.Dron = QWidget()
        self.Dron.setObjectName(u"Dron")
        self.PORC_BAT = QLabel(self.Dron)
        self.PORC_BAT.setObjectName(u"PORC_BAT")
        self.PORC_BAT.setGeometry(QRect(10, 30, 141, 16))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.PORC_BAT.setFont(font)
        self.porc_bat = QLabel(self.Dron)
        self.porc_bat.setObjectName(u"porc_bat")
        self.porc_bat.setGeometry(QRect(0, 50, 151, 20))
        self.porc_bat.setAlignment(Qt.AlignCenter)
        self.BAT_LINEA = QFrame(self.Dron)
        self.BAT_LINEA.setObjectName(u"BAT_LINEA")
        self.BAT_LINEA.setGeometry(QRect(10, 40, 131, 20))
        self.BAT_LINEA.setFrameShape(QFrame.HLine)
        self.BAT_LINEA.setFrameShadow(QFrame.Sunken)
        self.COORD_LINEA = QFrame(self.Dron)
        self.COORD_LINEA.setObjectName(u"COORD_LINEA")
        self.COORD_LINEA.setGeometry(QRect(700, 40, 141, 16))
        self.COORD_LINEA.setFrameShape(QFrame.HLine)
        self.COORD_LINEA.setFrameShadow(QFrame.Sunken)
        self.coord_actual_lb = QLabel(self.Dron)
        self.coord_actual_lb.setObjectName(u"coord_actual_lb")
        self.coord_actual_lb.setGeometry(QRect(698, 50, 141, 20))
        self.coord_actual_lb.setAlignment(Qt.AlignCenter)
        self.COORD_ACTUAL_LB = QLabel(self.Dron)
        self.COORD_ACTUAL_LB.setObjectName(u"COORD_ACTUAL_LB")
        self.COORD_ACTUAL_LB.setGeometry(QRect(700, 30, 151, 20))
        self.COORD_ACTUAL_LB.setFont(font)
        self.ArmDisarmButton_dron = QPushButton(self.Dron)
        self.ArmDisarmButton_dron.setObjectName(u"ArmDisarmButton_dron")
        self.ArmDisarmButton_dron.setGeometry(QRect(140, 320, 571, 41))
        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(True)
        self.ArmDisarmButton_dron.setFont(font1)
        self.StartMisionButton_dron = QPushButton(self.Dron)
        self.StartMisionButton_dron.setObjectName(u"StartMisionButton_dron")
        self.StartMisionButton_dron.setGeometry(QRect(140, 370, 161, 41))
        self.StartMisionButton_dron.setFont(font)
        self.RTLButton_dron = QPushButton(self.Dron)
        self.RTLButton_dron.setObjectName(u"RTLButton_dron")
        self.RTLButton_dron.setGeometry(QRect(340, 370, 181, 41))
        self.RTLButton_dron.setFont(font)
        self.ManualAutoButton_dron = QPushButton(self.Dron)
        self.ManualAutoButton_dron.setObjectName(u"ManualAutoButton_dron")
        self.ManualAutoButton_dron.setGeometry(QRect(550, 370, 161, 41))
        self.ManualAutoButton_dron.setFont(font)
        self.tabWidget.addTab(self.Dron, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.SiguienteCordenadaBotton_mapa = QPushButton(self.tab)
        self.SiguienteCordenadaBotton_mapa.setObjectName(u"SiguienteCordenadaBotton_mapa")
        self.SiguienteCordenadaBotton_mapa.setGeometry(QRect(660, 510, 191, 41))
        self.SiguienteCordenadaBotton_mapa.setFont(font1)
        self.AnteriorCordenadaBotton_mapa = QPushButton(self.tab)
        self.AnteriorCordenadaBotton_mapa.setObjectName(u"AnteriorCordenadaBotton_mapa")
        self.AnteriorCordenadaBotton_mapa.setGeometry(QRect(400, 510, 201, 41))
        self.AnteriorCordenadaBotton_mapa.setFont(font1)
        icon1 = QIcon()
        iconThemeName = u"video-x-generic"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.AnteriorCordenadaBotton_mapa.setIcon(icon1)
        self.gridLayoutWidget = QWidget(self.tab)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(400, 10, 451, 481))
        self.web_mapa = QGridLayout(self.gridLayoutWidget)
        self.web_mapa.setObjectName(u"web_mapa")
        self.web_mapa.setContentsMargins(0, 0, 0, 0)
        self.LINEA_DIVISORA = QFrame(self.tab)
        self.LINEA_DIVISORA.setObjectName(u"LINEA_DIVISORA")
        self.LINEA_DIVISORA.setGeometry(QRect(380, 0, 20, 571))
        self.LINEA_DIVISORA.setFrameShape(QFrame.VLine)
        self.LINEA_DIVISORA.setFrameShadow(QFrame.Sunken)
        self.gridLayoutWidget_4 = QWidget(self.tab)
        self.gridLayoutWidget_4.setObjectName(u"gridLayoutWidget_4")
        self.gridLayoutWidget_4.setGeometry(QRect(10, 10, 371, 271))
        self.mapa_2d = QGridLayout(self.gridLayoutWidget_4)
        self.mapa_2d.setObjectName(u"mapa_2d")
        self.mapa_2d.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutWidget_5 = QWidget(self.tab)
        self.gridLayoutWidget_5.setObjectName(u"gridLayoutWidget_5")
        self.gridLayoutWidget_5.setGeometry(QRect(10, 290, 371, 271))
        self.mapa_3d = QGridLayout(self.gridLayoutWidget_5)
        self.mapa_3d.setObjectName(u"mapa_3d")
        self.mapa_3d.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.tab, "")
        self.Editar = QWidget()
        self.Editar.setObjectName(u"Editar")
        self.textEdit = QPlainTextEdit(self.Editar)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(260, 190, 281, 211))
        self.horaEdit = QTimeEdit(self.Editar)
        self.horaEdit.setObjectName(u"horaEdit")
        self.horaEdit.setGeometry(QRect(300, 110, 81, 25))
        self.horaEdit.setAlignment(Qt.AlignCenter)
        self.fechaEdit = QDateEdit(self.Editar)
        self.fechaEdit.setObjectName(u"fechaEdit")
        self.fechaEdit.setGeometry(QRect(440, 110, 101, 25))
        self.fechaEdit.setAlignment(Qt.AlignCenter)
        self.fechaEdit.setMaximumDateTime(QDateTime(QDate(2026, 1, 1), QTime(23, 59, 59)))
        self.fechaEdit.setMinimumDateTime(QDateTime(QDate(2000, 9, 14), QTime(0, 0, 0)))
        self.GuardarCambios = QPushButton(self.Editar)
        self.GuardarCambios.setObjectName(u"GuardarCambios")
        self.GuardarCambios.setGeometry(QRect(220, 510, 191, 41))
        self.GuardarCambios.setFont(font1)
        self.GuardarCambios.setIcon(icon1)
        self.CancelarCambios = QPushButton(self.Editar)
        self.CancelarCambios.setObjectName(u"CancelarCambios")
        self.CancelarCambios.setGeometry(QRect(420, 510, 191, 41))
        self.CancelarCambios.setFont(font1)
        self.TITLEGUIDE = QLabel(self.Editar)
        self.TITLEGUIDE.setObjectName(u"TITLEGUIDE")
        self.TITLEGUIDE.setGeometry(QRect(220, 20, 351, 71))
        font2 = QFont()
        font2.setFamilies([u"Miriam CLM"])
        font2.setPointSize(15)
        font2.setBold(True)
        self.TITLEGUIDE.setFont(font2)
        self.TITLEGUIDE.setAlignment(Qt.AlignCenter)
        self.label_HORA_OBSERVACIONES = QLabel(self.Editar)
        self.label_HORA_OBSERVACIONES.setObjectName(u"label_HORA_OBSERVACIONES")
        self.label_HORA_OBSERVACIONES.setGeometry(QRect(260, 120, 31, 16))
        self.label_ESTIMACION_OBSERVACIONES = QLabel(self.Editar)
        self.label_ESTIMACION_OBSERVACIONES.setObjectName(u"label_ESTIMACION_OBSERVACIONES")
        self.label_ESTIMACION_OBSERVACIONES.setGeometry(QRect(360, 160, 71, 16))
        self.label_FECHA_OBSERVACIONES = QLabel(self.Editar)
        self.label_FECHA_OBSERVACIONES.setObjectName(u"label_FECHA_OBSERVACIONES")
        self.label_FECHA_OBSERVACIONES.setGeometry(QRect(400, 120, 41, 16))
        self.tabWidget.addTab(self.Editar, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.SiguienteCordenadaBotton_detalles = QPushButton(self.tab_3)
        self.SiguienteCordenadaBotton_detalles.setObjectName(u"SiguienteCordenadaBotton_detalles")
        self.SiguienteCordenadaBotton_detalles.setGeometry(QRect(640, 410, 191, 41))
        self.SiguienteCordenadaBotton_detalles.setFont(font1)
        self.AnteriorCordenadaBotton_detalles = QPushButton(self.tab_3)
        self.AnteriorCordenadaBotton_detalles.setObjectName(u"AnteriorCordenadaBotton_detalles")
        self.AnteriorCordenadaBotton_detalles.setGeometry(QRect(440, 410, 191, 41))
        self.AnteriorCordenadaBotton_detalles.setFont(font1)
        self.AnteriorCordenadaBotton_detalles.setIcon(icon1)
        self.gridLayoutWidget_3 = QWidget(self.tab_3)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(10, 10, 381, 241))
        self.Foto_Camara = QGridLayout(self.gridLayoutWidget_3)
        self.Foto_Camara.setObjectName(u"Foto_Camara")
        self.Foto_Camara.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.tab_3)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(460, 89, 351, 71))
        self.label.setFont(font2)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_CATEGORIA = QLabel(self.tab_3)
        self.label_CATEGORIA.setObjectName(u"label_CATEGORIA")
        self.label_CATEGORIA.setGeometry(QRect(460, 210, 61, 16))
        self.label_CORDENADAS_ORIGEN = QLabel(self.tab_3)
        self.label_CORDENADAS_ORIGEN.setObjectName(u"label_CORDENADAS_ORIGEN")
        self.label_CORDENADAS_ORIGEN.setGeometry(QRect(460, 240, 121, 16))
        self.label_FECHA_HORA = QLabel(self.tab_3)
        self.label_FECHA_HORA.setObjectName(u"label_FECHA_HORA")
        self.label_FECHA_HORA.setGeometry(QRect(460, 180, 71, 16))
        self.label_ESTADO = QLabel(self.tab_3)
        self.label_ESTADO.setObjectName(u"label_ESTADO")
        self.label_ESTADO.setGeometry(QRect(460, 300, 71, 16))
        self.label_AREA = QLabel(self.tab_3)
        self.label_AREA.setObjectName(u"label_AREA")
        self.label_AREA.setGeometry(QRect(460, 270, 121, 16))
        self.label_categoria = QLabel(self.tab_3)
        self.label_categoria.setObjectName(u"label_categoria")
        self.label_categoria.setGeometry(QRect(630, 210, 181, 20))
        self.label_categoria.setAlignment(Qt.AlignCenter)
        self.label_cordenadas_origen = QLabel(self.tab_3)
        self.label_cordenadas_origen.setObjectName(u"label_cordenadas_origen")
        self.label_cordenadas_origen.setGeometry(QRect(630, 240, 181, 20))
        self.label_cordenadas_origen.setAlignment(Qt.AlignCenter)
        self.label_estado = QLabel(self.tab_3)
        self.label_estado.setObjectName(u"label_estado")
        self.label_estado.setGeometry(QRect(630, 300, 181, 20))
        self.label_estado.setAlignment(Qt.AlignCenter)
        self.label_fecha_inicio = QLabel(self.tab_3)
        self.label_fecha_inicio.setObjectName(u"label_fecha_inicio")
        self.label_fecha_inicio.setGeometry(QRect(630, 180, 181, 20))
        self.label_fecha_inicio.setAlignment(Qt.AlignCenter)
        self.label_area = QLabel(self.tab_3)
        self.label_area.setObjectName(u"label_area")
        self.label_area.setGeometry(QRect(630, 270, 181, 20))
        self.label_area.setAlignment(Qt.AlignCenter)
        self.gridLayoutWidget_6 = QWidget(self.tab_3)
        self.gridLayoutWidget_6.setObjectName(u"gridLayoutWidget_6")
        self.gridLayoutWidget_6.setGeometry(QRect(10, 270, 381, 241))
        self.ImagenProcesada = QGridLayout(self.gridLayoutWidget_6)
        self.ImagenProcesada.setObjectName(u"ImagenProcesada")
        self.ImagenProcesada.setContentsMargins(0, 0, 0, 0)
        self.LINEA_DIVISORA_2 = QFrame(self.tab_3)
        self.LINEA_DIVISORA_2.setObjectName(u"LINEA_DIVISORA_2")
        self.LINEA_DIVISORA_2.setGeometry(QRect(390, 0, 20, 531))
        self.LINEA_DIVISORA_2.setFrameShape(QFrame.VLine)
        self.LINEA_DIVISORA_2.setFrameShadow(QFrame.Sunken)
        self.GenerarReporteBotton_detalles = QPushButton(self.tab_3)
        self.GenerarReporteBotton_detalles.setObjectName(u"GenerarReporteBotton_detalles")
        self.GenerarReporteBotton_detalles.setGeometry(QRect(0, 520, 861, 41))
        self.GenerarReporteBotton_detalles.setFont(font1)
        self.GenerarReporteBotton_detalles.setIcon(icon1)
        self.tabWidget.addTab(self.tab_3, "")

        self.retranslateUi(MainWidget)

        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWidget)
    # setupUi

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(QCoreApplication.translate("MainWidget", u"Incendio Mision", None))
        self.PORC_BAT.setText(QCoreApplication.translate("MainWidget", u"Porcentage Bateria", None))
        self.porc_bat.setText(QCoreApplication.translate("MainWidget", u"%NaN", None))
        self.coord_actual_lb.setText(QCoreApplication.translate("MainWidget", u"X,Y", None))
        self.COORD_ACTUAL_LB.setText(QCoreApplication.translate("MainWidget", u"Coordenadas Actual", None))
        self.ArmDisarmButton_dron.setText(QCoreApplication.translate("MainWidget", u"Arm/Disarm", None))
        self.StartMisionButton_dron.setText(QCoreApplication.translate("MainWidget", u"Start Mision", None))
        self.RTLButton_dron.setText(QCoreApplication.translate("MainWidget", u"RTL", None))
        self.ManualAutoButton_dron.setText(QCoreApplication.translate("MainWidget", u"Manual/Auto", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Dron), QCoreApplication.translate("MainWidget", u"Dron Status", None))
        self.SiguienteCordenadaBotton_mapa.setText(QCoreApplication.translate("MainWidget", u"Siguiente Cordenada", None))
        self.AnteriorCordenadaBotton_mapa.setText(QCoreApplication.translate("MainWidget", u"Anterior Cordenada", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWidget", u"Mapa", None))
        self.fechaEdit.setDisplayFormat(QCoreApplication.translate("MainWidget", u"M-d-yyyy", None))
        self.GuardarCambios.setText(QCoreApplication.translate("MainWidget", u"Guardar Cambios", None))
        self.CancelarCambios.setText(QCoreApplication.translate("MainWidget", u"Cancelar Cambios", None))
        self.TITLEGUIDE.setText(QCoreApplication.translate("MainWidget", u"Observaciones Generadas", None))
        self.label_HORA_OBSERVACIONES.setText(QCoreApplication.translate("MainWidget", u"Hora:", None))
        self.label_ESTIMACION_OBSERVACIONES.setText(QCoreApplication.translate("MainWidget", u"Estimacion", None))
        self.label_FECHA_OBSERVACIONES.setText(QCoreApplication.translate("MainWidget", u"Fecha:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Editar), QCoreApplication.translate("MainWidget", u"Observaciones", None))
        self.SiguienteCordenadaBotton_detalles.setText(QCoreApplication.translate("MainWidget", u"Siguiente Cordenada", None))
        self.AnteriorCordenadaBotton_detalles.setText(QCoreApplication.translate("MainWidget", u"Anterior Cordenada", None))
        self.label.setText(QCoreApplication.translate("MainWidget", u"Detalles Incendio", None))
        self.label_CATEGORIA.setText(QCoreApplication.translate("MainWidget", u"Categoria:", None))
        self.label_CORDENADAS_ORIGEN.setText(QCoreApplication.translate("MainWidget", u"Coordenadas Origen:", None))
        self.label_FECHA_HORA.setText(QCoreApplication.translate("MainWidget", u"Fecha/Hora:", None))
        self.label_ESTADO.setText(QCoreApplication.translate("MainWidget", u"Estimacion", None))
        self.label_AREA.setText(QCoreApplication.translate("MainWidget", u"Area", None))
        self.label_categoria.setText(QCoreApplication.translate("MainWidget", u"Cat 5", None))
        self.label_cordenadas_origen.setText(QCoreApplication.translate("MainWidget", u"18.539573, -69.911945", None))
        self.label_estado.setText(QCoreApplication.translate("MainWidget", u"Activo", None))
        self.label_fecha_inicio.setText(QCoreApplication.translate("MainWidget", u"8/5/2022", None))
        self.label_area.setText(QCoreApplication.translate("MainWidget", u"5 M2", None))
        self.GenerarReporteBotton_detalles.setText(QCoreApplication.translate("MainWidget", u"Generar Reporte Resumen", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWidget", u"Detalles Fuego", None))
    # retranslateUi

