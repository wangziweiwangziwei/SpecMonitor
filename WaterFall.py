# -*- coding: utf-8 -*-
import wx
from numpy import array, linspace
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas 
from matplotlib.cm import  jet 

class Water(wx.MDIChildFrame):
    def __init__(self,parent):
        wx.MDIChildFrame.__init__(self,parent,-1,title="WaterFall ")
        self.waterFirst=1
        self.col=800
        self.row=500
        self.CreatePanel()
        self.setWfLabel()
        

    def CreatePanel(self):
        self.Figure = matplotlib.figure.Figure(figsize=(1,1))
        self.axes=self.Figure.add_axes([0.05,0.05,0.93,0.93])
        self.FigureCanvas = FigureCanvas(self,-1,self.Figure)
              

    def WaterFall(self,yData):        
        if(self.waterFirst):
            min_data=int(min(yData))
            max_data=int(max(yData))
            min_data=min_data/10*10
            max_data=max_data/10*10
            self.matrixFull = [[min_data for i in range(self.col)] for i in range(self.row)]
            norm = matplotlib.colors.Normalize(vmin=min_data, vmax=max_data)
            self.image = self.axes.imshow(array(self.matrixFull),origin='lower',cmap=jet,norm=norm,interpolation='nearest')
            cbar=self.Figure.colorbar(self.image)
            ticks=linspace(min_data,max_data,10)
            cbar.set_ticks(ticks)
            tick_labels=[str(int(i)) for i in ticks]
            cbar.set_ticklabels(tick_labels)
            self.waterFirst=0
        else:
            while(self.draw5water%6):
                yTmp=[]
                for j in range(self.col):
                    ySum=max(yData[j*self.samplIntv:(j+1)*self.samplIntv])
                    yTmp.append(ySum)          
                del self.matrixFull[self.row-self.rowCpy:self.row]
        
                for i in range(self.rowCpy):
                    self.matrixFull.insert(0,yTmp)
                self.image.set_data(array(self.matrixFull))
                self.FigureCanvas.draw()
                self.draw5water=self.draw5water+1
            self.draw5water=1

    def setWfLabel(self):
        self.ylabel('Frame Number')
        self.xlabel('MHz')
        xLabelNum = 10
        intervalX = self.col/xLabelNum
        xticks = range(0, self.col, intervalX)
        xticklabels = [str(i) for i in range(0,51,5)]
        self.axes.set_xticks(xticks)
        self.axes.set_xticklabels(xticklabels,rotation=0)

        intervalY = self.row/xLabelNum
        yticks = range(0, self.row+1, intervalY)
        yticklabels = [str(i) for i in yticks]
        self.axes.set_yticks(yticks)
        self.axes.set_yticklabels(yticklabels,rotation=0)        
        
          

    def xlim(self,x_min,x_max):  
        self.axes.set_xlim(x_min,x_max)  
  
  
    def ylim(self,y_min,y_max):  
        self.axes.set_ylim(y_min,y_max)

    def xlabel(self,XabelString="X"):   
        self.axes.set_xlabel(XabelString)  
  
  
    def ylabel(self,YabelString="Y"):  
        self.axes.set_ylabel(YabelString)
