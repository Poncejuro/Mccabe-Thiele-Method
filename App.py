import sys
from PyQt5 import uic
#from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from Modulo_Destilacion import c1a as UnaEntrada
from Modulo_Destilacion import c2a as DosEntardas


#Estructura para llamar la GUI
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI.ui",self)
        
        #Desactivar las casillas
        self.labelF.setEnabled(False)
        self.valF2.setEnabled(False)
        self.labelf.setEnabled(False)
        self.valf2.setEnabled(False)
        self.labelT.setEnabled(False)     
        self.labelE.setEnabled(False)
        self.labelE2.setEnabled(False)
        self.labelD.setEnabled(False)
        self.labelB.setEnabled(False)
        self.valMF.setEnabled(False)
        self.valMF2.setEnabled(False)
        self.valMD.setEnabled(False)
        self.valMB.setEnabled(False)
        
        #armando el ComboBox
        self.Tipo_Entrada.currentIndexChanged.connect(self.activar_casilla)
        
        #armando del botón calcular
        self.boton_calcular.clicked.connect(self.calculos)
    
        
    def activar_casilla(self):    
        item=self.Tipo_Entrada.currentText()
        if item == "Una alimentación":
            self.labelF.setEnabled(False)
            self.valF2.setEnabled(False)
            self.labelf.setEnabled(False)
            self.valf2.setEnabled(False)
            self.labelT.setEnabled(False)     
            self.labelE.setEnabled(False)
            self.labelE2.setEnabled(False)
            self.labelD.setEnabled(False)
            self.labelB.setEnabled(False)
            self.valMF.setEnabled(False)
            self.valMF2.setEnabled(False)
            self.valMD.setEnabled(False)
            self.valMB.setEnabled(False)
        else:
             self.labelF.setEnabled(True)
             self.valF2.setEnabled(True)
             self.labelf.setEnabled(True)
             self.valf2.setEnabled(True)
             self.labelT.setEnabled(True)     
             self.labelE.setEnabled(True)
             self.labelE2.setEnabled(True)
             self.labelD.setEnabled(True)
             self.labelB.setEnabled(True)
             self.valMF.setEnabled(True)
             self.valMF2.setEnabled(True)
             self.valMD.setEnabled(True)
             self.valMB.setEnabled(True)
        return
   
    def calculos(self):
        item=self.Tipo_Entrada.currentText()
        if item == "Una alimentación":
            D=float(self.valD.toPlainText())
            B=float(self.valB.toPlainText())
            F=float(self.valF.toPlainText())
            R=float(self.valR.toPlainText())
            f=float(self.valf.toPlainText())
            NP=UnaEntrada(D,B,F,R,f) 
            self.label_NP.setText("Se calcularon " + str(NP) + " platos")
            self.label_NP.setFont(QFont('Arial', 12))           
        else:
            D=float(self.valD.toPlainText())
            B=float(self.valB.toPlainText())
            F=float(self.valF.toPlainText())
            R=float(self.valR.toPlainText())
            f=float(self.valf.toPlainText())
            f2=float(self.valf2.toPlainText())
            F2=float(self.valF2.toPlainText())
            FM1=float(self.valMF.toPlainText())
            FM2=float(self.valMF2.toPlainText())
            Dm=float(self.valMD.toPlainText())
            Bm=float(self.valMB.toPlainText())
            #Balances de masa
            L=R*Dm
            LT=L+FM1*(1-f)
            LTT=LT+FM2*(1-f2)
            VTT=LTT-Bm
            VT=VTT+FM2*f2
            V=VT+FM1*f
            m1=L/V
            m2=LT/VT
            m3=LTT/VTT  
            NP=DosEntardas(D,B,F,R,f,f2,F2,m1,m2,m3)
            self.label_NP.setText("Se calcularon " + str(NP) + " platos")
            self.label_NP.setFont(QFont('Arial', 12))
        return
           
#Iniciar y cerrar la aplicación
if __name__ == "__main__":
    app =  QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())