# -*- coding: utf-8 -*-
import wx
from numpy import array, linspace
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas 
from matplotlib.cm import  jet 
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

class Spec(wx.MDIChildFrame):
    def __init__(self,parent):
        wx.MDIChildFrame.__init__(self,parent,-1,title="Spectrum")
        topSplitter = wx.SplitterWindow(self)
        hSplitter = wx.SplitterWindow(topSplitter)

        self.panelAbFreq = MyListCtrlAbFreq(hSplitter)
        self.panelQuery = MyListCtrlQuery(hSplitter)
        hSplitter.SplitHorizontally(self.panelAbFreq, self.panelQuery)
        hSplitter.SetSashGravity(0.35)

        self.panelFigure = PanelSpec(topSplitter)
        topSplitter.SplitVertically(self.panelFigure, hSplitter)
        topSplitter.SetSashGravity(0.8)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(topSplitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        
class MyListCtrlAbFreq(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
        self.InsertColumn(0, u'序号')
        self.InsertColumn(1, u'异常频点频率(MHz)')
        self.InsertColumn(2, u'异常频点功率(dB)')
        self.SetColumnWidth(0, 50)
        self.SetColumnWidth(1, 120)
        self.SetColumnWidth(2, 130)
        for i in range(1,11):
            self.InsertStringItem(i-1,str(i))

class MyListCtrlQuery(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
        self.InsertColumn(0, u"帧类型")
        self.InsertColumn(1, u'参数类型')
        self.InsertColumn(2, u'参数值')
        self.SetColumnWidth(0, 100)
        self.SetColumnWidth(1, 100)
        self.SetColumnWidth(2, 100)
        for i in range(1,5301):
            self.InsertStringItem(i-1,str(i))

    
class PanelSpec(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        self.CreatePanel()
        self.setSpLabel()
    def CreatePanel(self):
        self.Figure = matplotlib.figure.Figure()
        self.axes=self.Figure.add_axes([0.05,0.05,0.93,0.93])
        self.FigureCanvas = FigureCanvas(self,-1,self.Figure)
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.FigureCanvas,1,wx.EXPAND)
        self.SetSizer(sizer)
    def setSpLabel(self, begin_X=0, end_X=50e6,begin_Y=-150,end_Y=0): 
        if(begin_Y==-150 and end_Y==0):
            self.yticks=range(-150,1,10)
            self.ylabel('dBFS')
        else:
            begin_Y=begin_Y/10*10
            end_Y=end_Y/10*10
            interval = 10
            yLabelNum=(end_Y-begin_Y)/interval
            self.yticks = [begin_Y+i*interval for i in range(yLabelNum+1)]

        yticklabels = [str(int(i*10)/10.0) for i in self.yticks]
        self.ylim(begin_Y,end_Y)
        self.xlim(begin_X,end_X)


        if( begin_X==0 and end_X==50e6):
            self.xticks=range(int(0),int(50e6+1),int(5e6))
            self.xlabel('MHz')
        else:
            xLabelNum = 10
            interval = (end_X - begin_X)/xLabelNum
            self.xticks = [begin_X+i*interval for i in range(xLabelNum+1)]

        xticklabels = [str(int(100*i/1e6)/100.0) for i in self.xticks]
        self.axes.set_xticks(self.xticks)
        self.axes.set_xticklabels(xticklabels,rotation=0)
        self.axes.set_yticks(self.yticks)
        self.axes.set_yticklabels(yticklabels,rotation=0)
        self.axes.grid(True)

    def PowerSpectrum(self, y):
        if self.btnStopFlg == 0:
            self.yData = y
            '''
            self.LineSpec.set_ydata(array(self.yData))
            self.FigureCanvas.restore_region(self.background)
            self.axes.draw_artist(self.LineSpec)
            self.FigureCanvas.blit(self.axes.bbox)
            '''
            self.LineSpec.set_ydata(array(self.yData))
            self.FigureCanvas.draw()
            

    def xlim(self,x_min,x_max):  
        self.axes.set_xlim(x_min,x_max)  
  
  
    def ylim(self,y_min,y_max):  
        self.axes.set_ylim(y_min,y_max)

    def xlabel(self,XabelString="X"):   
        self.axes.set_xlabel(XabelString)  
  
  
    def ylabel(self,YabelString="Y"):  
        self.axes.set_ylabel(YabelString)
            
