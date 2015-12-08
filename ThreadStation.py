# -*- coding: utf-8 -*-
import threading
import wx
from Package import *
import time
import Queue
from math import pi,cos,pow,log10
dictFreqPlan={1:u"固定",2:u"移动",3:u"无线电定位",4:u"卫星固定",5:u"空间研究",6:u"卫星地球探测",
              7:u"射电天文",8:u"广播",9:u"移动(航空移动除外)",10:u"无线电导航",11:u"航空无线电导航",
              12:u"水上移动",13:u"卫星移动",14:u"卫星间",15:u"卫星无线电导航",16:u"业余",17:u"卫星气象",18:u"标准频率和时间信号",
              19:u"空间操作",20:u"航空移动",21:u"卫星业余",22:u"卫星广播",23:u"航空移动(OR)",
              24:u"气象辅助",25:u"航空移动(R)",26:u"水上无线电导航",27:u"陆地移动",28:u"移动(航空移动(R)除外)",
              29:u"卫星无线电测定",30:u"卫星航空移动(R)",31:u"移动(航空移动(R)除外)",32:u"水上移动(遇险和呼叫)",
              33:u"水上移动(使用DSC的遇险和安全呼叫)",34:u"未划分"}


List=["AM","FM",'DSB','LSB','USB','VSB','AM-FM','FMCW','FMICW','PM','2ASK','4ASK','2FSK','4FSK','BPSK','QPSK']
############中心站响应数据接收##################################
class ReceiveServerData(threading.Thread): 
    def __init__(self,specFrame,sock,outPoint,threadDrawFFT,threadDrawIQ): 
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()
        self.sock=sock
        self.outPoint=outPoint
        self.specFrame=specFrame
        self.threadDrawFFT=threadDrawFFT  ##主要用来控制画功率谱和画IQ波形的线程停止和开启
        self.threadDrawIQ=threadDrawIQ 
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
            if(frameFlag>0 and frameFlag<=28):
                self.outPoint.write(bytearray(ListData))
            if(frameFlag==176):
                self.ReadConnect(ListData)
            elif(frameFlag==177):
                self.ReadElecTrend(ListData)
            elif(frameFlag==178):
                self.ReadElecPath(ListData)
            elif(frameFlag==179):
                self.ReadAbFreq(ListData)
            elif(frameFlag==181):
                self.ReadStationPro(ListData)
            elif(frameFlag==182):
                self.ReadStationCurPro(ListData)
            elif(frameFlag==183):
                List=[(0,u"起始频率（Mhz）"),(1,u"终止频率（Mhz）"),(2,u"业务类型 1")]
                for i in range(3):
                    col = self.specFrame.panelQuery.GetColumn(i)
                    col.SetText(List[i][1])
                    self.specFrame.panelQuery.SetColumn(i, col)      
                for i in range(7):
                    self.specFrame.panelQuery.InsertColumn(i+3,u"业务类型"+str(i+3))
                    self.specFrame.panelQuery.SetColumnWidth(i+3,100)
                self.ReadFreqPlan(ListData)
            elif(frameFlag==184):
                self.ReadAllStationPro(ListData)
            
            elif(frameFlag==185):
                self.ReadOnlinePortPro(ListData)
            elif(frameFlag==186):
                self.ReadRegisterPortPro(ListData)
            elif(frameFlag==187):
                self.ReadSpecData(ListData)
            elif(frameFlag==188):
                self.ReadIQData(ListData)
            else:
                print 'frameFlag error'
           
    def ReadConnect(self,ListData):
        print ' response from server'
        
    ###########################辅助函数######################
    def ByteToTime(self,Data):
        Time =(((Data[0]<<4)+((Data[1])>>4)),(Data[1]&0x0F),(Data[2]>>3), \
                                        (((Data[2]&0x07)<<2)+(Data[3]&0x03)),(Data[3]>>2))
        return Time 
    
    def ByteToPos(self,Data):
        lonFlag=1
        latFlag=1
        altiFlag=1
        
        if(Data[0]):
            lonFlag=-1
        if(Data[4]>>7):
            latFlag=-1
        if(Data[7]>>7):
            altiFlag=-1
            
        Lon=Data[1]+float((Data[2]<<8)+(Data[3]))/2**16
        Lon=Lon*lonFlag
        Lat=(Data[4]&0x7F)+float((Data[5]<<8)+Data[6])/2**16
        Lat=Lat*latFlag
        Alti=((Data[7]&0x7F)<<8)+Data[8]
        Alti=Alti*altiFlag
        
        return (Lon,Lat,Alti)
    
    def ByteToPower(self,Data):
        if(Data[0]>>7):
            Power=(Data[0]<<5)+(Data[1]>>3)-2**13-float(Data[1]&0x03)/8
        else:
            Power=(Data[0]<<5)+(Data[1]>>3)+float(Data[1]&0x03)/8
        
        return Power
    
    
    ##########################################################
    def ReadElecTrend(self,ListData):
        centreFreq=(ListData[4]<<8)+(ListData[5])
        bandWidth=ListData[6]
        refreshN=ListData[7]
        refreshIntv=ListData[8]
        N_x=ListData[9]
        N_y=ListData[10]
        delta=(ListData[11]>>3)+float(ListData[11]&0x07)/8
        ListTime=[]
        ListP=[]
        i=12
        lenData=len(ListData)
        while(i<lenData-3):
            Time=self.ByteToTime(ListData[i:i+4])
            ListTime.append(Time)
            Pos=self.ByteToPos(ListData[i+4:i+13])
            Power=self.ByteToPower(ListData[i+13:i+15])
                                
            efficent=(ListData[i+15]>>4)+float(ListData[i+15]&0x0F)/16
            ListP.append((Pos[0],Pos[1],Pos[2],Power,efficent)) 
            i=i+16
        
    ############计算网格的功率,经纬高度,并加入ListAll#########################################
        ListAll=[]
        
        count=0
        while(count<refreshN):
            L=ListP[count][0]
            B=ListP[count][1]
            H=ListP[count][2]
            P=ListP[count][4]
            E=ListP[count][5]
            delta_Y=2*pi*(6338137+H)/(360*60)*delta
            delta_X=delta_Y*cos(B)
            
            Grid=[[0 for i in xrange(2*N_y+1)] for i in xrange(2*N_x+1)]
            for i in xrange(N_x+1):
                for j in xrange(N_y+1):
                    dis=pow((N_x-i)*delta_X,2)+pow((N_y-j)*(delta_Y),2)
                    Pi=P-5*E*log10(dis)
                    pos=(L+(i-N_x)*delta/60,B+(j-N_y)*delta/60,H,Pi)
                    Grid[i][j]=pos
            for i in xrange(N_x+1,2*N_x+1,1):
                for j in xrange(N_y):
                    Pi=Grid[2*N_x-i][j][2]
                    pos=(L+(i-N_x)*delta/60,B+(j-N_y)*delta/60,H,Pi)
                    Grid[i][j]=pos
            for i in xrange(N_x+1,2*N_x+1,1):
                for j in xrange(N_y+1,2*N_y+1,1):
                    Pi=Grid[i][2*N_y-j][2]
                    pos=(L+(i-N_x)*delta/60,B+(j-N_y)*delta/60,H,Pi)
                    Grid[i][j]=pos
            for i in xrange(N_x):
                for j in xrange(N_y+1,2*N_y+1,1):
                    Pi=Grid[2*N_x-i][j][2]
                    pos=(L+(i-N_x)*delta/60,B+(j-N_y)*delta/60,H,Pi)
                    Grid[i][j]=pos
            
            for i in xrange(N_x+1,2*N_x+1,1):
                Pi=Grid[2*N_x-i][N_y]
                pos=(L+(i-N_x)*delta/60,B,H,Pi)
                Grid[i][N_y]=pos
            
            for j in xrange(N_y+1,2*N_y+1,1):
                Pi=Grid[i][2*N_y-j]
                pos=(L,B+(j-N_y)*delta/60,H,Pi)
                Grid[N_x][j]=pos
            
            ListAll.append(Grid)
            count+=1
            
                
        
        
    def ReadElecPath(self,ListData):
        centreFreq=(ListData[5]<<8)+ListData[6]
        bandWidth=ListData[7]
        i=8
        ListTime=[]
        ListP=[]
        while(i<len(ListData)-3):
            Time =self.ByteToTime(ListData[i:i+4])
            ListTime.append(Time)
            Pos=self.ByteToPos(ListData[i+4:i+13])
            Power=self.ByteToPower(ListData[i+13:i+15])
    
            ListP.append((Pos[0],Pos[1],Pos[2],Power)) 
            i=i+15
        
    def ReadAbFreq(self,ListData):
        centreFreq=(ListData[4]<<6)+(ListData[5]&0x3F)+float(((ListData[5]>>6)<<8)+ListData[6])/2**10
        bandWidth=ListData[7]&0x3F + float(((ListData[7]>>6)<<8)+ListData[8])/2**10
        if(ListData[9]):
            modulate=List[ListData[9]]
            modulateParam=ListData[10]+float(ListData[11])/2**8
        i=12
        ListP=[]
        Pos=self.ByteToPos(ListData[i:i+9])
        Power=self.ByteToPower(ListData[i+9:i+11])
                            
        efficent=(ListData[i+11]>>4)+float(ListData[i+11]&0x0F)/16
        ListP.append((Pos[0],Pos[1],Pos[2],Power,efficent)) 
        
        TimeComsume=str(ListData[i+12])+'%'
        WorkPro=dictFreqPlan[ListData[i+13]]
        IsIllegal=ListData[i+14]
        OwnUint=''
        for j in xrange((i+15),(i+23),1):
            OwnUint+=chr(ListData[j])
        
            
            
    def ReadStationPro(self,ListData):
        ListStation=[]
        i=4
        while(i<len(ListData)-3):
            OwnUnit=''
            for j in xrange(i,i+8,1):
                OwnUnit+=chr(ListData[j])
            Identifier=(ListData[i+8]<<16)+(ListData[i+9]<<8)+ListData[i+10]
            Pos=self.ByteToPos(ListData[i+11:i+20])
            FreqStart=(ListData[i+20]<<8)+ListData[i+21]
            FreqEnd=(ListData[i+22]<<8)+ListData[i+23]
            Power=self.ByteToPower(ListData[i+24:i+26])
            bandWidth=ListData[i+26]&0x3F + float(((ListData[i+26]>>6)<<8)+ListData[i+27])/2**10
            modulate=List[ListData[i+28]]
            modulateParam=ListData[i+29]+float(ListData[i+30])/2**8
            WorkPro=dictFreqPlan[ListData[i+31]]
            Radius=ListData[i+32]
            TimeComsume=str(ListData[i+33])+'%'
            ListStation.append((Pos[0],Pos[1],Pos[2],Identifier,FreqStart,FreqEnd, \
                                    Power,bandWidth,modulate,modulateParam,WorkPro,Radius,TimeComsume))
            
            i+=34
            
            
    def ReadStationCurPro(self,ListData):
        i=4
        
        OwnUnit=''
        for j in xrange(i,i+8,1):
            OwnUnit+=chr(ListData[j])
        Identifier=(ListData[i+8]<<16)+(ListData[i+9]<<8)+ListData[i+10]
        Pos=self.ByteToPos(ListData[i+11:i+20])
        centreFreq=(ListData[i+20]<<6)+(ListData[i+21]&0x3F)+float(((ListData[i+21]>>6)<<8)+ListData[i+22])/2**10
        Power=self.ByteToPower(ListData[i+23:i+25])
        efficent=(ListData[i+25]>>4)+float(ListData[i+25]&0x0F)/16
        
        bandWidth=ListData[i+26]&0x3F + float(((ListData[i+26]>>6)<<8)+ListData[i+27])/2**10
        modulate=List[ListData[i+28]]
        modulateParam=ListData[i+29]+float(ListData[i+30])/2**8
        WorkPro=dictFreqPlan[ListData[i+31]]
        TimeComsume=str(ListData[i+32])+'%'
        IsIllegal=ListData[i+33]
     
            
    def ReadFreqPlan(self,ListData):
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
    
    def ReadAllStationPro(self,ListData):
        ListStation=[]
        ListIllegal=[]
        
        i=4
        while(i<len(ListData)-3):
            OwnUnit=''
            for j in xrange(i,i+8,1):
                OwnUnit+=chr(ListData[j])
            Pos=self.ByteToPos(ListData[i+11:i+20])
            FreqStart=(ListData[i+20]<<8)+ListData[i+21]
            FreqEnd=(ListData[i+22]<<8)+ListData[i+23]
            Power=self.ByteToPower(ListData[i+24:i+26])
            bandWidth=ListData[i+26]&0x3F + float(((ListData[i+26]>>6)<<8)+ListData[i+27])/2**10
            modulate=List[ListData[i+28]]
            modulateParam=ListData[i+29]+float(ListData[i+30])/2**8
            WorkPro=dictFreqPlan[ListData[i+31]]
            Radius=ListData[i+32]
            TimeComsume=str(ListData[i+33])+'%'
            if((ListData[i+8])==0xFF):
                ListIllegal.append((Pos[0],Pos[1],Pos[2],FreqStart,FreqEnd, \
                                    Power,bandWidth,modulate,modulateParam,WorkPro,Radius,TimeComsume))
            else:
                Identifier=(ListData[i+8]<<16)+(ListData[i+9]<<8)+ListData[i+10]
                ListStation.append((Pos[0],Pos[1],Pos[2],Identifier,FreqStart,FreqEnd, \
                                    Power,bandWidth,modulate,modulateParam,WorkPro,Radius,TimeComsume))
            
            i+=34


    def ReadOnlinePortPro(self,ListData):
        ListPort0=[]
        ListPort1=[]
        ListPort2=[]
        ListPort3=[]
        i=4
        count=0
        N=(ListData[i]<<8)+ListData[i+1]
        while(count<N):
            ID=(ListData[i+3]<<8)+ListData[i+2]
            Pos=self.ByteToPos(ListData[i+5:i+14])
            if(ListData[i+4]==0):
                ListPort0.append((Pos[0],Pos[1],Pos[2],ID))
            elif(ListData[i+4]==1):
                ListPort1.append((Pos[0],Pos[1],Pos[2],ID))
            elif(ListData[i+4]==2):
                ListPort2.append((Pos[0],Pos[1],Pos[2],ID))
            elif(ListData[i+4]==3):
                ListPort3.append((Pos[0],Pos[1],Pos[2],ID))
                    
            count+=1
            i=i+14
            
    def ReadRegisterPortPro(self,ListData):
        ListPort0=[]
        ListPort1=[]
        ListPort2=[]
        ListPort3=[]
        i=4
        count=0
        N=(ListData[i]<<8)+ListData[i+1]
        while(count<N):
            ID=(ListData[i+3]<<8)+ListData[i+2]
            Pos=self.ByteToPos(ListData[i+5:i+14])
            if(ListData[i+4]==0):
                ListPort0.append((Pos[0],Pos[1],Pos[2],ID))
            elif(ListData[i+4]==1):
                ListPort1.append((Pos[0],Pos[1],Pos[2],ID))
            elif(ListData[i+4]==2):
                ListPort2.append((Pos[0],Pos[1],Pos[2],ID))
            elif(ListData[i+4]==3):
                ListPort3.append((Pos[0],Pos[1],Pos[2],ID))
                    
            count+=1
            i=i+14
            
    
    def ReadSpecData(self,ListData):
        '''
        self.threadDrawFFT.stop()
        
        self.specFrame.panelFigure.setSpLabel()
        '''
        
    def ReadIQData(self,ListData):
        pass 
    
    
    
            
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


            

    