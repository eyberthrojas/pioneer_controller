#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
import utiles as ut
import numpy as np
import sys
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import threading
class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App,self).__init__()
        self.title = 'Visualizacion robot'
        self.width = 1080
        self.height = 1080
        self.left = 10
        self.top = 10 
        self.contador = 0 
        self.f_timer = False 
        self.dt = 200  
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.actualiza)
        # Widgets
        # Título 
        titulo = QtWidgets.QLabel(self)
        titulo.setAlignment(QtCore.Qt.AlignCenter)
        titulo.setStyleSheet('border: gray; border-style:solid; border-width: 1px; color: black; font: 20pt Arial')
        titulo.setText("GUI ROBOT")
        # Grafica 
        self.canvas = Canvas(self, width = 8, height = 4)
        self.canvas.setStyleSheet('border: gray; border-style:solid; border-width: 1px')
        # Boton Inicio
        self.boton_inicio = QtWidgets.QPushButton(self)
        self.boton_inicio.setText("Iniciar")
        self.boton_inicio.clicked.connect(self.mostrar_contador)
        # Visualización
        self.visualizacion = QtWidgets.QLabel(self)
        self.visualizacion.setAlignment(QtCore.Qt.AlignCenter)
        self.visualizacion.setStyleSheet('border: gray; border-style:solid; border-width: 1px')
        
        # Layouts
        self.controles = QtWidgets.QHBoxLayout(self)
        self.controles.addWidget(self.boton_inicio)
        self.controles.addWidget(self.visualizacion)
        # Crea layoud raiz
        self.raiz = QtWidgets.QVBoxLayout(self)
        self.raiz.addWidget(titulo,5)
        self.raiz.addWidget(self.canvas,70)
        self.raiz.addLayout(self.controles,15)
        # main
        self.main = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main)
        self.centralWidget().setLayout(self.raiz)
        self.show()
    def mostrar_contador(self):
        if self.f_timer == False:
            self.f_timer = True
            self.timer.start(self.dt)
            self.boton_inicio.setText("Detener")
        else:
            self.f_timer = False
            self.timer.stop()
            self.boton_inicio.setText("Iniciar")
        
    def actualiza(self):
        #if self.f_timer == True:
        x,y,dirx,diry = ut.figRobot(posRobot, 0.25)
        self.canvas.plot(x,y,dirx,diry)
        self.visualizacion.setText("dt: "+str(t.dt*1000)+" ms")
        print("Pos robot ",posRobot.x," ",posRobot.x)

class Canvas(FigureCanvas):
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
    def plot(self, x, y, dirx, diry):
        self.axes.cla()
        self.axes.plot(x,y,'r',dirx,diry,'b')
        self.axes.axis([-5, 5, -5, 5])
        self.axes.grid(True)
        self.draw()

def robotPosCallback(msg):
    posRobot.x = msg.linear.x
    posRobot.y = msg.linear.y
    posRobot.theta = msg.angular.z
def simTimeCallback(msg):
    tiempo.actualizarTiempo(msg.data)
    t.fps = tiempo.fps
    t.dt = tiempo.dt
def hilo_ROS():
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        rate.sleep()       
if __name__ == '__main__':
    try:
        rospy.init_node('gui', anonymous=True)
        rospy.loginfo("Nodo Iniciado")
        rospy.Subscriber('/pioneerPosition', Twist, robotPosCallback)
        rospy.Subscriber('/simulationTime', Float32, simTimeCallback)
        posRobot = ut.PosRobot()
        tiempo = ut.tiempo(0.0) 
        t = ut.FPS()  
        hilo1 = threading.Thread(target = hilo_ROS)  
        hilo1.daemon = True
        hilo1.start() 
        app = QtWidgets.QApplication(sys.argv)
        ex = App()
        sys.exit(app.exec_())     
    except rospy.ROSInterruptException:
        pass
    