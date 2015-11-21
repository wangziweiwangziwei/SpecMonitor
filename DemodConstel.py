# -*- coding: cp936 -*-
import wx
import numpy as np

import matplotlib
#matplotlib.use("WXAgg")    
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import scipy.signal as signal
from math import sqrt, log10, pi, cos, sin, atan
#import ClassClust
#import ClassDemod
    
class Constel(wx.MDIChildFrame):
    def __init__(self,parent):
        wx.MDIChildFrame.__init__(self,parent,-1,title="Constellation ")
        self.CreatePanel()  
        self.SUM_SNR=0
        self.NUM_SNR=0
        self.SUM_EVM=0
        self.NUM_EVM=0
        self.SUM_Delta_F=0
    def CreatePanel(self):
        self.Figure = matplotlib.figure.Figure(figsize=(1,1))
        self.axes=self.Figure.add_axes([0.05,0.05,0.9,0.9])
        self.FigureCanvas = FigureCanvas(self,-1,self.Figure)
        ticks=range(-4,5,1)
        ticklabel=[str(i) for i in ticks]
        self.axes.set_xlim(-4,4)
        self.axes.set_ylim(-4,4)
        self.axes.set_xticks(ticks)
        self.axes.set_yticks(ticks)
        self.axes.set_xticklabels(ticklabel)
        self.axes.set_yticklabels(ticklabel)
        self.axes.grid()
        self.LineConstel,=self.axes.plot([],[],'r',linestyle='',marker='o')
    def constellation(self, fs,chData):
        pass
        '''
        while(len(self.axes.texts)):
            self.axes.texts.pop()
        ch1 = ClassDemod.DoubleVector() 
        for i in chData:
            ch1.append(i.real)
            ch1.append(i.imag)
        cons = ClassDemod.Demod(ch1, self.Fd, 16)
        cons.demodCon()
        deltafq = cons.deltaFq
        delta_phy=cons.deltaP
        rad1 = 0.1
        points = cons.numFinalIQ
        extractN = 1
        demension = 2
        dataLen = (int)(points/extractN)
        dataI = ClassClust.DoubleVector()
        dataQ = ClassClust.DoubleVector()
        for i in range(dataLen):
            dataI.append((cons.IconFinal)[extractN*i])
            dataQ.append((cons.QconFinal)[extractN*i])
        clust = ClassClust.CSubclust(dataI, dataQ, extractN, dataLen, demension, 0.1)
        clust.SubclustCent()
        
        evm = clust.SubclustEVM()
        evm = evm*100
        strEVM = 'EVM: '+str('%0.2f'%evm)+'%'
        strdeltafq = 'deltaf: '+ str('%0.2f'%deltafq)+'hz'
        strdeltaphy = 'delta_phy: '+ str('%0.2f'%delta_phy)+'rad'
        self.SUM_EVM+=evm
        self.SUM_Delta_F+=deltafq
        self.NUM_EVM+=1
        AVG_EVM=self.SUM_EVM/self.NUM_EVM
        AVG_Delta_F=self.SUM_Delta_F/self.NUM_EVM
        
        str_AVG_EVM='AVG_EVM: '+str('%0.2f'%AVG_EVM)+'%'
        str_AVG_Delta_F='AVG_deltaf: '+str('%0.2f'%AVG_Delta_F)+'hz'

        I = cons.IconFinal
        Q = cons.QconFinal
      
        I=list(I)
        Q=list(Q)
        Imax=max(I)
        Imin=min(I)
        Qmax=max(Q)
        Qmin=min(Q)
        Idata=[(I[i]-Imin)/(Imax-Imin)*6+(-3) for i in range(len(I))]
        Qdata=[(Q[i]-Qmin)/(Qmax-Qmin)*6+(-3) for i in range(len(Q))]
      
        self.axes.text(-3.8,3.8, strEVM, fontsize=13,fontweight='heavy')
        self.axes.text(-3.8,3.5,str_AVG_EVM,fontsize=13,fontweight='heavy')
        self.axes.text(-3.8,3.2 ,strdeltafq, fontsize=13,fontweight='heavy')
        self.axes.text(-3.8,2.9,strdeltaphy,fontsize=13,fontweight='heavy')
        self.axes.text(-3.8,2.6,str_AVG_Delta_F,fontsize=13,fontweight='heavy')
        self.LineConstel.set_xdata(Idata)
        self.LineConstel.set_ydata(Qdata)
        self.FigureCanvas.draw()
        del cons
        del clust

        '''
