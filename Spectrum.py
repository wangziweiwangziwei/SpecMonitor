# -*- coding: utf-8 -*-
import wx
from numpy import array, linspace
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas 


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
        self.setSpLabel(intv=300e6)
    def CreatePanel(self):
        self.Figure = matplotlib.figure.Figure()
        self.axes=self.Figure.add_axes([0.05,0.05,0.93,0.93])
        self.FigureCanvas = FigureCanvas(self,-1,self.Figure)
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.FigureCanvas,1,wx.EXPAND)
        self.SetSizer(sizer)
        Array=linspace(70, 5995,238)
        xDataList=[]
        self.LineSpec=[]
        for i in xrange(237):
            xData=linspace(Array[i],Array[i+1],1024)
            xDataList.append(xData)
        
        ydata=[0]*1024
        for xData in xDataList:
            lineSpec,=self.axes.plot(xData*1e6,ydata,'y')
            self.LineSpec.append(lineSpec)
      
        self.LineSPecBack,=self.axes.plot([],[],'r')
    def setSpLabel(self, begin_X=70e6,intv=5e6, end_X=5995e6,begin_Y=-120,end_Y=60): 
        self.ylabel('dBm')
        self.xlabel('MHz')
        self.ylim(begin_Y,end_Y)
        self.xlim(begin_X,end_X)
        yticks=range(-120,60+1,10)
        yticklabels = [str(i) for i in yticks]  
        xticks=range(int(70e6),int(5995e6+1),int(intv))
        xticklabels = [str(int(100*i/1e6)/100.0) for i in xticks]
        self.axes.set_xticks(xticks)
        self.axes.set_xticklabels(xticklabels,rotation=0)
        self.axes.set_yticks(yticks)
        self.axes.set_yticklabels(yticklabels,rotation=0)
        self.axes.grid(True)

    def PowerSpectrum(self, y,funcPara,curSectionNo):
       
        if(funcPara==0x0D):
            self.LineSpec[curSectionNo-1].set_ydata(array(y))
        elif(funcPara==0x1D):
            pass
            #self.LineSPecBack.set_ydata(array(y))
        self.FigureCanvas.draw()
                
            

    def xlim(self,x_min,x_max):  
        self.axes.set_xlim(x_min,x_max)  
  
  
    def ylim(self,y_min,y_max):  
        self.axes.set_ylim(y_min,y_max)

    def xlabel(self,XabelString="X"):   
        self.axes.set_xlabel(XabelString)  
  
  
    def ylabel(self,YabelString="Y"):  
        self.axes.set_ylabel(YabelString)
            
