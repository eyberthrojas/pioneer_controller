#!/usr/bin/env python3
import numpy as np
class tiempo():
    def __init__(self, t):
        self.t_ant = 0.0
        self.t = float(t)
    def actualizarTiempo(self, t):
        self.t_ant = self.t
        self.t = float(t)
        self.dt = self.t - self.t_ant
        self.fps = 1/self.dt

class PosRobot():
    x = float()
    y = float()
    theta = float()
    
class FPS():
    fps = float()
    dt = float()
    
class Banderas():
    posFlag = bool()
    timeFlag = bool()
    scannerFlag = bool()

class scannerData():
    dim = int()
    dist = []
    alpha = []

class worldScannerData():
    dim = int()
    x = []
    y = []
    
def figRobot(pos, r):
    theta = np.linspace(0,2*np.pi,100)
    x = r*np.cos(theta) + pos.x
    y = r*np.sin(theta) + pos.y
    dirx = [pos.x, pos.x + r*np.cos(pos.theta)]
    diry = [pos.y, pos.y + r*np.sin(pos.theta)]
    return x,y,dirx,diry    