from PyQt5 import QtWidgets, QtGui, QtCore

from prueba import Ui_MainWindow  # importing our generated file

import sys

import Querys

import csv


class mywindow(QtWidgets.QMainWindow):


    def __init__(self):
        super(mywindow, self).__init__()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.ui.label.setFont(QtGui.QFont('SansSerif', 20))

        self.ui.label.setGeometry(QtCore.QRect(30, 5, 1000, 100))

        self.ui.comboBox.addItem("Salas ocupadas")  # add item

        self.ui.comboBox.addItem("Salas no ocupadas")

        self.ui.comboBox_2.addItem("Orientación")  # add item

        self.ui.comboBox_2.addItem("Norte")

        self.ui.comboBox_2.addItem("Sur")

        self.ui.comboBox_2.addItem("Este")

        self.ui.comboBox_2.addItem("Oeste")

        self.ui.comboBox_3.addItem("Medida")  # add item

        self.ui.comboBox_3.addItem("Temperatura")

        self.ui.comboBox_3.addItem("Consumo Agua")

        self.ui.comboBox_3.addItem("Nivel Humedad")

        self.ui.comboBox_3.addItem("Nivel Batería")

        self.ui.comboBox_4.addItem("Nivel")  # add item

        self.ui.comboBox_4.addItem("Mayor")

        self.ui.comboBox_4.addItem("Menor")

        self.ui.comboBox_4.addItem("Entre")

        self.ui.comboBox_4.addItem("Actual")

        self.ui.CancelOK.accepted.connect(self.accept)
        self.ui.CancelOK.rejected.connect(self.reject)
        print(self.ui.comboBox.itemText(0))

        text = str(self.ui.comboBox.currentText())



        #ocupadas=self.ui.comboBox.activated.connect(self.pass_Net_Adap)

        #orientacion=self.ui.comboBox_2.activated.connect(self.pass_Net_Adap)

    def accept(self):
         Ocupadas= str(self.ui.comboBox.currentText())
         Orientacion= str(self.ui.comboBox_2.currentText())
         Medida = str(self.ui.comboBox_3.currentText())
         Medicion=Medida
         Nivel= str(self.ui.comboBox_4.currentText())
         FirstLimit=str(self.ui.lineEdit.text())
         if FirstLimit!="":
            FirstLimit=int(FirstLimit)
         SecondLimit = str(self.ui.lineEdit_2.text())
         if SecondLimit!="":
            SecondLimit=int(SecondLimit)
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
         elif Medida=="Nivel Bateria":
             Medida="vbat"
         print(Ocupadas, Orientacion, Medida)
         Sensores, Salas= x.Query_Salas(Tipo_Sensor=Medida, orientacion=Orientacion, ocupada=Ocupadas)
         print(Salas)
         if Nivel=="Actual":
            resultados = x.Query_Niv_Actual(Sensores=Sensores, medida=Medida)
         elif Nivel=="Mayor" or Nivel=="Menor" or Nivel=="Entre":
            if Nivel=="Entre":
                resultados=x.Query_level(Sensores_Analizar=Sensores, medida=Medida, nivel=[FirstLimit, SecondLimit], condicion=Nivel)
            else:
                resultados = x.Query_level(Sensores_Analizar=Sensores, medida=Medida, nivel=[FirstLimit],
                                           condicion=Nivel)
         sensors = list(resultados.keys())
         i=0
         with open(NombreArchivo, mode='w') as archivo:
             archivo_writer = csv.writer(archivo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
             archivo_writer.writerow(['Salas', 'Sensor', Medicion])
             for r in Salas:
                if not resultados[sensors[i]]:
                    archivo_writer.writerow([r, sensors[i], 'Error'])
                    i+=1
                else:
                    pru = list(resultados[sensors[i]][0][0].keys())
                    archivo_writer.writerow([r, sensors[i], resultados[sensors[i]][0][0][pru[1]]])
                    i += 1
                print(i)
         Sensores.clear()
         Salas.clear()
         resultados.clear()
         sensors.clear()
         i=0



    def reject(self):
        text = str(self.ui.comboBox.currentText())

    def pass_Net_Adap(self):
        text = str(self.ui.comboBox.currentText())
        return text





app = QtWidgets.QApplication([])

application = mywindow()

application.show()

sys.exit(app.exec())


