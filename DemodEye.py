# -*- coding: cp936 -*-
import wx
import numpy as np

import matplotlib
#matplotlib.use("WXAgg")    
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from matplotlib import cm
import scipy.signal as signal
from math import sqrt, log10, pi, cos, sin, atan
#import ClassDemod


class Eye(wx.MDIChildFrame):
    def __init__(self,parent):
        wx.MDIChildFrame.__init__(self,parent,-1,title=" EyeDiagram ")
        self.CreatePanel()  
    def CreatePanel(self):
        self.Figure = matplotlib.figure.Figure(figsize=(1,1))
        self.axes=self.Figure.add_axes([0.05,0.05,0.9,0.9])
        self.FigureCanvas = FigureCanvas(self,-1,self.Figure) 
    def eyePattern(self, fs,ch):
        pass
        '''
        self.axes.lines=[]
        self.chData=ch
        self.Fs=fs
        ch1 = ClassDemod.DoubleVector() 
        for i in self.chData:
            ch1.append(i.real)
            ch1.append(-i.imag)
        cons = ClassDemod.Demod(ch1, self.Fd, 16)
        cons.demodEye()
        sigI = cons.IeyeFinal
        nsample = int(self.Fs/self.Fd)
        self.axes.set_xlim(1,nsample)    
        for i in range(100):  
            yTmp = sigI[nsample*i:nsample*(i+1)]
            xTmp = [i+1 for i in range(nsample)]
            self.axes.plot(xTmp,yTmp,'r')  
        self.FigureCanvas.draw()
        del cons
        '''
