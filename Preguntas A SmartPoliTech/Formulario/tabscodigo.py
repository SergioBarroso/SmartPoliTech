from PyQt5 import QtWidgets, QtGui, QtCore

from tabs import Ui_MainWindow  # importing our generated file

import sys

import Querys

import csv
import datetime


class mywindow(QtWidgets.QMainWindow):


    def __init__(self):
        super(mywindow, self).__init__()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.ui.label_Pregunta.setFont(QtGui.QFont('SansSerif', 16))

        self.ui.label_Pregunta.setGeometry(QtCore.QRect(30, 5, 1000, 100))

        self.ui.comboBox_Ocu.addItem("Salas ocupadas")  # add item

        self.ui.comboBox_Ocu.addItem("Salas no ocupadas")

        self.ui.comboBox_Ori.addItem("Orientación")  # add item

        self.ui.comboBox_Ori.addItem("Norte")

        self.ui.comboBox_Ori.addItem("Sur")

        self.ui.comboBox_Ori.addItem("Este")

        self.ui.comboBox_Ori.addItem("Oeste")

        self.ui.comboBox_Med.addItem("Medida")  # add item

        self.ui.comboBox_Med.addItem("Temperatura")

        self.ui.comboBox_Med.addItem("Consumo Agua")

        self.ui.comboBox_Med.addItem("Nivel Humedad")

        self.ui.comboBox_Med.addItem("Nivel Batería")

        self.ui.comboBox_Ocu_3.addItem("Salas ocupadas")  # add item

        self.ui.comboBox_Ocu_3.addItem("Salas no ocupadas")

        self.ui.comboBox_Ori_3.addItem("Orientación")  # add item

        self.ui.comboBox_Ori_3.addItem("Norte")

        self.ui.comboBox_Ori_3.addItem("Sur")

        self.ui.comboBox_Ori_3.addItem("Este")

        self.ui.comboBox_Ori_3.addItem("Oeste")

        self.ui.comboBox_Med_3.addItem("Medida")  # add item

        self.ui.comboBox_Med_3.addItem("Temperatura")

        self.ui.comboBox_Med_3.addItem("Consumo Agua")

        self.ui.comboBox_Med_3.addItem("Nivel Humedad")

        self.ui.comboBox_Med_3.addItem("Nivel Batería")


        self.ui.CancelOK_tab2.accepted.connect(self.accept_tab2)
        self.ui.CancelOK_tab2.rejected.connect(self.reject)
        self.ui.CancelOK_tab1.accepted.connect(self.accept)
        self.ui.CancelOK_tab1.rejected.connect(self.reject)
        self.ui.CancelOK_tab3_1.accepted.connect(self.accept_tab3)
        self.ui.CancelOK_tab3_1.rejected.connect(self.reject)
        self.ui.CancelOK_tab4.accepted.connect(self.accept_tab4)
        self.ui.CancelOK_tab4.rejected.connect(self.reject)
        self.ui.CancelOK_estacion.accepted.connect(self.accept_tab5)
        self.ui.CancelOK_estacion.rejected.connect(self.reject)



        #print(self.ui.comboBox.itemText(0))

        #text = str(self.ui.comboBox.currentText())



        #ocupadas=self.ui.comboBox.activated.connect(self.pass_Net_Adap)

        #orientacion=self.ui.comboBox_2.activated.connect(self.pass_Net_Adap)

    def accept_tab2(self):
         x = Querys.Consultas()
         Ocupadas= str(self.ui.comboBox_Ocu_3.currentText())
         Orientacion= str(self.ui.comboBox_Ori_3.currentText())
         Medida = str(self.ui.comboBox_Med_3.currentText())
         Medicion=Medida
         Nivel= str(self.ui.comboBox_Nivel.currentText())
         FirstLimit=str(self.ui.lineEdit_Lim1.text())
         SecondLimit = str(self.ui.lineEdit_Lim2.text())
         NombreArchivo= str(self.ui.lineEdit_Arch2.text())+".csv"
         if FirstLimit!="":
            FirstLimit=int(FirstLimit)
         if SecondLimit!="":
            SecondLimit=int(SecondLimit)
         if Ocupadas=="Salas no ocupadas":
             Ocupadas=False
         else:
             Ocupadas=True
         if Orientacion=="Orientación":
             Orientacion=False
         else:
             Orientacion=Orientacion
         if Medida=="Medida":
             print('Error')# De momento hasta que se definan mas preguntas
         elif Medida=="Temperatura":
             Medida="temp"
         elif Medida=="Consumo Agua":
             Medida="agua"
         elif Medida=="Nivel Humedad":
             Medida="hum"
         elif Medida=="Nivel Batería":
             Medida="vbat"
         Sensores, Salas, Orientar= x.Query_Salas(Tipo_Sensor=Medida, orientacion=Orientacion, ocupada=Ocupadas)
         if Nivel=="Mayor" or Nivel=="Menor" or Nivel=="Entre":
            if Nivel=="Entre":
                resultados=x.Query_level(Sensores_Analizar=Sensores, medida=Medida, nivel=[FirstLimit, SecondLimit], condicion=Nivel)
            else:
                resultados = x.Query_level(Sensores_Analizar=Sensores, medida=Medida, nivel=[FirstLimit],
                                           condicion=Nivel)

         sensors = list(resultados.keys())
         print(resultados[sensors[1]])
         i=0
         with open(NombreArchivo, mode='w') as archivo:
             archivo_writer = csv.writer(archivo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
             archivo_writer.writerow(['Salas', 'Sensor', Medicion, "Orientación"])
             for r in Salas:
                if not resultados[sensors[i]]:
                    print("pasa")
                    i+=1
                else:
                    pru = list(resultados[sensors[i]][0][0].keys())
                    archivo_writer.writerow([r, sensors[i], resultados[sensors[i]][0][0][pru[1]], Orientar[i] ])
                    i += 1
         Sensores.clear()
         Salas.clear()
         resultados.clear()
         sensors.clear()
         i=0
    def accept(self):
         x=Querys.Consultas()
         Ocupadas= str(self.ui.comboBox_Ocu.currentText())
         Orientacion= str(self.ui.comboBox_Ori.currentText())
         Medida = str(self.ui.comboBox_Med.currentText())
         Medicion=Medida
         NombreArchivo= str(self.ui.lineEdit_1.text())+".csv"
         if Ocupadas=="Salas no ocupadas":
             Ocupadas=False
         else:
             Ocupadas=True
         if Orientacion=="Orientación":
             Orientacion=False
         else:
             Orientacion=Orientacion
         if Medida=="Medida":
             print('Error')# De momento hasta que se definan mas preguntas
         elif Medida=="Temperatura":
             Medida="temp"
         elif Medida=="Consumo Agua":
             Medida="agua"
         elif Medida=="Nivel Humedad":
             Medida="hum"
         elif Medida=="Nivel Batería":
             Medida="vbat"

         Sensores, Salas, Orientar= x.Query_Salas(Tipo_Sensor=Medida, orientacion=Orientacion, ocupada=Ocupadas)
         resultados = x.Query_Niv_Actual(Sensores=Sensores, medida=Medida)

         sensors = list(resultados.keys())
         i=0
         with open(NombreArchivo, mode='w') as archivo:
             archivo_writer = csv.writer(archivo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
             archivo_writer.writerow(['Salas', 'Sensor', Medicion, "Orientacion"])
             for r in Salas:
                if not resultados[sensors[i]]:
                    i+=1
                else:
                    pru = list(resultados[sensors[i]][0][0].keys())
                    archivo_writer.writerow([r, sensors[i], resultados[sensors[i]][0][0][pru[1]],Orientar[i]] )
                    i += 1
         Sensores.clear()
         Salas.clear()
         resultados.clear()
         sensors.clear()
         i=0

    def accept_tab3(self):
        Orientacion = str(self.ui.comboBox_Ori_4.currentText())
        TipoSala = str(self.ui.comboBox_Sala_1.currentText())
        NombreArchivo = str(self.ui.lineEdit_Arch2_2.text()) + ".csv"
        x = Querys.Consultas()
        if TipoSala == "Sala":
            TipoSala = False
        if Orientacion == "Orientacion":
            print("ERROR")
        Nombre, Orientacion = x.Query_Orientacion(Tipo_Sala=TipoSala, orientacion=Orientacion)
        i = 0
        with open(NombreArchivo, mode='w') as archivo:
            archivo_writer = csv.writer(archivo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            archivo_writer.writerow(['Salas', "Orientacion"])
            for r in Nombre:
                archivo_writer.writerow([r, Orientacion[i]])
                i += 1
        Nombre.clear()
        Orientacion.clear()
        i = 0

    def accept_tab4(self):
         Ocupadas= str(self.ui.comboBox.currentText())
         Orientacion= str(self.ui.comboBox_2.currentText())
         Medida = str(self.ui.comboBox_3.currentText())
         Medicion=Medida
         Fecha_ini=self.ui.dateTimeEdit.dateTime()
         Fecha_ini = Fecha_ini.toPyDateTime()
         Fecha_ini=Fecha_ini.strftime("%d-%m-%YT%H:%M:%SZ")
         Fecha_fin = self.ui.dateTimeEdit_2.dateTime()
         Fecha_fin = Fecha_fin.toPyDateTime()
         Fecha_fin = Fecha_fin.strftime("%d-%m-%YT%H:%M:%SZ")
         Hora_Ini=str(self.ui.comboBox_5.currentText())
         Hora_Fin = str(self.ui.comboBox_6.currentText())
         if Fecha_ini=="01-01-2000T00:00:00Z":
             Fecha_ini=False
         else:
             Fecha_ini = datetime.datetime.strptime(Fecha_ini, "%d-%m-%YT%H:%M:%SZ")
         if Fecha_fin=="01-01-2000T00:00:00Z":
             Fecha_fin=False
         else:
            Fecha_fin = datetime.datetime.strptime(Fecha_fin, "%d-%m-%YT%H:%M:%SZ")
         if Hora_Ini!="Hora Inicio":
            Hora_Inicio=int(Hora_Ini)
         else:
             Hora_Inicio=False
         if Hora_Fin!="Hora Final":
            Hora_Final=int(Hora_Fin)
         else:
             Hora_Final=False
         NombreArchivo= str(self.ui.lineEdit_3.text())+".csv"
         x=Querys.Consultas()
         if Ocupadas=="Salas no ocupadas":
             Ocupadas=False
         else:
             Ocupadas=True
         if Orientacion=="Orientación":
             Orientacion=False
         else:
             Orientacion=Orientacion
         if Medida=="Medida":
             print('Error')# De momento hasta que se definan mas preguntas
         elif Medida=="Temperatura":
             Medida="temp"
         elif Medida=="Consumo Agua":
             Medida="agua"
         elif Medida=="Nivel Humedad":
             Medida="hum"
         elif Medida=="Nivel Batería":
             Medida="vbat"
         Sensores, Salas, Orientar= x.Query_Salas(Tipo_Sensor=Medida, orientacion=Orientacion, ocupada=Ocupadas)
         resultados=x.Query_Media_Medida(medida=Medida,
                           operacion="mean",
                           Sensores_Analizar=Sensores, fecha=Fecha_ini, fecha_fin=Fecha_fin, primera_hora=Hora_Inicio,
                           segunda_hora=Hora_Final)
         sensors = list(resultados.keys())
         i=0
         v=0
         if Hora_Ini=="Hora Inicio" and Hora_Fin=="Hora Final":
             with open(NombreArchivo, mode='w') as archivo:
                 archivo_writer = csv.writer(archivo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                 archivo_writer.writerow(['Salas', 'Sensor', Medicion, "Orientación"])
                 for r in Salas:
                    if not resultados[sensors[i]]:
                        i+=1
                    else:
                        pru = list(resultados[sensors[i]][0][0].keys())
                        archivo_writer.writerow([r, sensors[i], resultados[sensors[i]][0][0][pru[1]], Orientar[i] ])
                        i += 1
         else:
             with open(NombreArchivo, mode='w') as archivo:
                 archivo_writer = csv.writer(archivo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                 archivo_writer.writerow(['Sala', 'Sensor',"Fecha", Medicion])
                 for r in Salas:
                    if not resultados[sensors[i]]:
                        i+=1
                    else:
                        for m in resultados[sensors[0]][0]:
                            pru = list(resultados[sensors[i]][0][0].keys())
                            archivo_writer.writerow([r, sensors[i], m['time'],  m['mean']])
                        i += 1
         Sensores.clear()
         Salas.clear()
         resultados.clear()
         sensors.clear()
         i=0
    def accept_tab5(self):
         Ocupadas= str(self.ui.comboBox_14.currentText())
         year=str(self.ui.comboBox_16.currentText())
         Orientacion= str(self.ui.comboBox_13.currentText())
         Medida = str(self.ui.comboBox_4.currentText())
         Medicion=Medida
         Nivel= str(self.ui.comboBox_Nivel_3.currentText())
         FirstLimit=str(self.ui.lineEdit_Lim1_3.text())
         Estacion=str(self.ui.comboBox_15.currentText())
         if FirstLimit!="":
            FirstLimit=int(FirstLimit)
         SecondLimit = str(self.ui.lineEdit_Lim2_3.text())
         if SecondLimit!="":
            SecondLimit=int(SecondLimit)
         NombreArchivo= str(self.ui.lineEdit_Arch2_5.text())+".csv"
         x=Querys.Consultas()
         if Ocupadas=="Salas no ocupadas":
             Ocupadas=False
         else:
             Ocupadas=True
         if Orientacion=="Orientación":
             Orientacion=False
         else:
             Orientacion=Orientacion
         if Medida=="Medida":
             print('Error')# De momento hasta que se definan mas preguntas
         elif Medida=="Temperatura":
             Medida="temp"
         elif Medida=="Consumo Agua":
             Medida="agua"
         elif Medida=="Nivel Humedad":
             Medida="hum"
         elif Medida=="Nivel Batería":
             Medida="vbat"
         Sensores, Salas, Orientar= x.Query_Salas(Tipo_Sensor=Medida, orientacion=Orientacion, ocupada=Ocupadas)
         if Nivel=="Mayor" or Nivel=="Menor" or Nivel=="Entre":
            if Nivel=="Entre":
                resultados=x.Query_Estaciones(Sensores_Analizar=Sensores, medida=Medida, estacion=Estacion, year=year, nivel=[FirstLimit, SecondLimit],
                                   condicion=Nivel)
            else:
                resultados = x.Query_Estaciones(Sensores_Analizar=Sensores, medida=Medida, estacion=Estacion, year=year, nivel=[FirstLimit],
                                   condicion=Nivel)

         sensors = list(resultados.keys())
         print(resultados[sensors[1]])
         i=0
         with open(NombreArchivo, mode='w') as archivo:
             archivo_writer = csv.writer(archivo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
             archivo_writer.writerow(['Salas', 'Sensor', Medicion, "Orientación"])
             for r in Salas:
                if not resultados[sensors[i]]:
                    print("pasa")
                    i+=1
                else:
                    pru = list(resultados[sensors[i]][0][0].keys())
                    archivo_writer.writerow([r, sensors[i], resultados[sensors[i]][0][0][pru[1]], Orientar[i] ])
                    i += 1
         Sensores.clear()
         Salas.clear()
         resultados.clear()
         sensors.clear()
         i=0
    def reject(self):
        text = str(self.ui.comboBox.currentText())
        print("CERRAR VENTANA")
"""
    def pass_Net_Adap(self):
        text = str(self.ui.comboBox.currentText())
        return text
"""




app = QtWidgets.QApplication([])

application = mywindow()

application.show()

sys.exit(app.exec())

