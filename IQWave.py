# -*- coding: cp936 -*-
import wx


import matplotlib
#matplotlib.use("WXAgg")    
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from math import sqrt, log10, pi, cos, sin, atan


class WaveIQ(wx.MDIChildFrame):
    def __init__(self,parent,name):
        wx.MDIChildFrame.__init__(self,parent,-1,title=name)
        self.Fs=5e6
        self.CreatePanel()  
        self.setWaveLabel()
        

    def CreatePanel(self):
        self.Figure = matplotlib.figure.Figure(figsize=(1,1))
        self.axes=self.Figure.add_axes([0.05,0.05,0.93,0.93])
        self.FigureCanvas = FigureCanvas(self,-1,self.Figure)
       

    def setWaveLabel(self,begin_X=0,end_X=9.81,begin_Y=-1.3,end_Y=1.3):   
        if(begin_X<0):begin_X=0
        if(end_Y>1.3):
            end_Y=1.3 
            begin_Y=-1.3 

        yLabelNum=8
        self.axes.set_xlim(begin_X,end_X)
        self.axes.set_ylim(begin_Y,end_Y)
        interval=float(end_Y-begin_Y)/ yLabelNum
        yticks=[(begin_Y+interval*i) for i in range(yLabelNum+1)]
        yticklabels = [str(int(n*100)/100.00) for n in yticks]
        self.axes.set_ylabel('V',rotation=1)
        
        xLabelNum = 9
        interval = (end_X-begin_X)/xLabelNum
        xticks = [begin_X+interval*i for i in range(xLabelNum+1)]
        xticklabels = [str('%0.2f'%i) for i in xticks]
        if(self.Fs==5e6):
            self.axes.set_xlabel('ms')
        if(self.Fs==40000):
            self.axes.set_xlabel('s')
        self.axes.set_xticks(xticks)
        self.axes.set_xticklabels(xticklabels,rotation=0)
        self.axes.set_yticks(yticks)
        self.axes.set_yticklabels(yticklabels,rotation=0)
        self.axes.grid(True)


    def Wave(self,fs,chData):
        pass
    

        
        
            
        


        



        
