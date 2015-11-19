# -*- coding: cp936 -*-
import wx
import numpy as np

import matplotlib
#matplotlib.use("WXAgg")    
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
    
import scipy.signal as signal
from math import sqrt, log10, pi, cos, sin, atan


class CCDF(wx.MDIChildFrame):
    def __init__(self,parent):
        wx.MDIChildFrame.__init__(self,parent,-1,title=" CCDF ")
        self.CreatePanel()  
    def CreatePanel(self):
        self.Figure = matplotlib.figure.Figure(figsize=(1,1))
        self.axes=self.Figure.add_axes([0.05,0.05,0.9,0.9])
        self.FigureCanvas = FigureCanvas(self,-1,self.Figure)
        self.axes.set_xlabel('dB')
        self.axes.set_ylabel('Ratio')
        self.axes.set_xlim(0,10)
        self.axes.set_ylim(10e-5, 1)
        self.axes.grid(True)
        self.LineCCDF,=self.axes.semilogy([],[],'r')
    def CCDF(self,chData):
        pass
        '''
        IData = [i.real for i in chData]
        nPoints = len(IData)
        power = [(i**2) for i in IData]
        meanPower = sum(power)/float(nPoints)
        dataRatio = [-0.1]*nPoints
        for i in xrange(nPoints):
            if (power[i] >= 0.1*meanPower):
                dataRatio[i] = 10*log10(power[i]/meanPower)

        maxDataRatio = max(dataRatio)
       
        num = 50
        realNum = 20
        X_Axis = [i*maxDataRatio/num for i in range(num)]
        X_AxisReal = [0]*realNum
        for i in xrange(10):
            X_AxisReal[i] = X_Axis[4*i]
            X_AxisReal[10+i] = X_Axis[40+i]
            
        y = [0]*realNum
        for i in range(realNum):
            for j in dataRatio:
                if j >= X_AxisReal[i]:
                    y[i] += 1
        y = [i/float(nPoints) for i in y]
        y.append(1.0/float(nPoints))
        X_AxisReal.append(maxDataRatio)
        self.LineCCDF.set_xdata(X_AxisReal)
        self.LineCCDF.set_ydata(y)
        self.FigureCanvas.draw()
        '''
