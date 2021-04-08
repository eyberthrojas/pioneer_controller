#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray
import utiles as ut
import numpy as np


def pioneerPosCallback(msg):
    posRobot.x = msg.linear.x
    posRobot.y = msg.linear.y
    posRobot.theta = msg.angular.z
    rospy.loginfo("Pos Robot: {} {} {}".format(posRobot.x, posRobot.y, posRobot.theta))

def simTimeCallback(msg):
    tiempo.actualizarTiempo(msg.data)
    t.fps = tiempo.fps
    t.dt = tiempo.dt
    rospy.loginfo("FPS: {}".format(t.fps))

def pioneer_controller():
    rate = rospy.Rate(100) # 10hz
    while not rospy.is_shutdown():  
        vel.data[0] = 1
        vel.data[1] = 1
        motorsVelPub.publish(vel)
        rate.sleep()
        
        
if __name__ == '__main__':
    try:
        rospy.init_node('pioneer_controller', anonymous=True)
        rospy.loginfo("Nodo Iniciado")
        rospy.Subscriber('/pioneerPosition', Twist, pioneerPosCallback)
        rospy.Subscriber('/simulationTime', Float32, simTimeCallback)
        motorsVelPub = rospy.Publisher('/motorsVel', Float32MultiArray, queue_size=10)
        vel = Float32MultiArray()
        vel.data = np.empty(2)
        posRobot = ut.PosRobot()
        tiempo = ut.tiempo(0.0) 
        t = ut.FPS()
        pioneer_controller()          
    except rospy.ROSInterruptException:
        pass


