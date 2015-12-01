# -*- coding: utf-8 -*-
import threading
import wx
from Package import *
import time
import Queue

dictFreqPlan={1:u"固定",2:u"移动",3:u"无线电定位",4:u"卫星固定",5:u"空间研究",6:u"卫星地球探测",
              7:u"射电天文",8:u"广播",9:u"移动(航空移动除外)",10:u"无线电导航",11:u"航空无线电导航",
              12:u"水上移动",13:u"卫星移动",14:u"卫星间",15:u"卫星无线电导航",16:u"业余",17:u"卫星气象",18:u"标准频率和时间信号",
              19:u"空间操作",20:u"航空移动",21:u"卫星业余",22:u"卫星广播",23:u"航空移动(OR)",
              24:u"气象辅助",25:u"航空移动(R)",26:u"水上无线电导航",27:u"陆地移动",28:u"移动(航空移动(R)除外)",
              29:u"卫星无线电测定",30:u"卫星航空移动(R)",31:u"移动(航空移动(R)除外)",32:u"水上移动(遇险和呼叫)",
              33:u"水上移动(使用DSC的遇险和安全呼叫)",34:u"未划分"}


############中心站响应数据接收##################################
class ReceiveServerData(threading.Thread): 
    def __init__(self,specFrame,sock):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()
        self.sock=sock
        self.specFrame=specFrame
    def stop(self):
        self.event.clear()
    def run(self):
        while(1):
            
            self.event.wait()
            frameLen=self.sock.recv(8)
            dataLen=[]
            ListData=[]
            for i in frameLen:
                dataLen.append(ord(i))
              
            dataLength=(dataLen[0]<<56)+(dataLen[1]<<48)+(dataLen[2]<<40)+ \
            (dataLen[3]<<32)+(dataLen[4]<<24)+(dataLen[5]<<16)+(dataLen[6]<<8)+dataLen[7]  
            frameData=self.sock.recv(dataLength)
            print 'dataLength',dataLength
            for i in frameData:
                ListData.append(ord(i))
            
            frameFlag=ListData[1]
            if(frameFlag==176):
                self.ReadConnectResponse(ListData)
            elif(frameFlag==177):
                self.ReadElecTrendResponse(ListData)
            elif(frameFlag==178):
                self.ReadElecPathResponse(ListData)
            elif(frameFlag==179):
                self.ReadAbFreqResponse(ListData)
            elif(frameFlag==181):
                self.ReadStationProResponse(ListData)
            elif(frameFlag==182):
                self.ReadStationCurProResponse(ListData)
            elif(frameFlag==183):
                List=[(0,u"起始频率（Mhz）"),(1,u"终止频率（Mhz）"),(2,u"业务类型 1")]
                for i in range(3):
                    col = self.specFrame.panelQuery.GetColumn(i)
                    col.SetText(List[i][1])
                    self.specFrame.panelQuery.SetColumn(i, col)
                self.ReadFreqPlanResponse(ListData)
                
                for i in range(7):
                    self.specFrame.panelQuery.InsertColumn(i+3,u"业务类型"+str(i))
                    self.specFrame.panelQuery.SetColumnWidth(100)
            else:
                print 'frameFlag  Error'
           
    def ReadConnectResponse(self,ListData):
        pass
    def ReadElecTrendResponse(self,ListData):
        pass
    def ReadElecPathResponse(self,ListData):
        pass
    def ReadAbFreqResponse(self,ListData):
        pass
    def ReadStationProResponse(self,ListData):
        pass
    def ReadStationCurProResponse(self,ListData):
        pass
    def ReadFreqPlanResponse(self,ListData):
        i=4
        count=0
        lenData=len(ListData)
        while(i<lenData-3):
            startHigh4bit=(ListData[i+2])>>4
            startLow4bit=ListData[i+2]&0x0F
            endHigh4bit=ListData[i+6]>>4
            endLow4bit=ListData[i+6]&0x0F
            startFreqInteger=(ListData[i]<<12)+(ListData[i+1]<<4)+startHigh4bit
            startFreqFraction=float((startLow4bit<<8)+ListData[i+3])/2**12
            endFreqInteger=(ListData[i+4]<<12)+(ListData[i+5]<<4)+endHigh4bit
            endFreqFraction=float((endLow4bit<<8)+ListData[i+7])/2**12
            
            startFreq=startFreqInteger+startFreqFraction
            endFreq=endFreqInteger+endFreqFraction
            j=i+8
            freqPro=[]
            r=0
            while(r<8 and ListData[j]):
                freqPro.append(ListData[j])
                r=r+1
                j=j+1
            
            self.specFrame.panelQuery.SetStringItem(count,0,str('%0.5f'%startFreq))
            self.specFrame.panelQuery.SetStringItem(count,1,str('%0.5f'%endFreq))
            for k in xrange(len(freqPro)):
                self.specFrame.panelQuery.SetStringItem(count,k+2,dictFreqPlan[freqPro[k]])
            count=count+1
            i=i+16
            
        while(count<1000):
            self.specFrame.panelQuery.SetStringItem(count,0,'')
            self.specFrame.panelQuery.SetStringItem(count,1,'')
            self.specFrame.panelQuery.SetStringItem(count,2,'')
            count=count+1
        
'''
    
class PopFrame(wx.MDIChildFrame):
    def __init__(self,parent,name):
        wx.MDIChildFrame.__init__(self,parent,-1,name,size=(500,600))
        pane=wx.Panel(self,-1)
        self.list = wx.ListCtrl(pane,-1,style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
        self.list.InsertColumn(0, "StartFreq(Mhz)")
        self.list.InsertColumn(1, 'EndFreq(Mhz)')
        self.list.InsertColumn(2, 'Type')
        self.list.SetColumnWidth(0,120)
        self.list.SetColumnWidth(1, 120)
        self.list.SetColumnWidth(2, 120)
        for i in range(1,100):
            self.list.InsertStringItem(i-1,str(i))
        self.list.Fit()
          
'''


            

    