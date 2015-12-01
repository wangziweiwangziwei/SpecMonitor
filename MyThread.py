# -*- coding: utf-8 -*-
import threading
import wx
from Package import *
from HardwareAccess import *
import time
import Queue

##包括了功率谱和异常频点(功率谱数据帧后紧跟异常频点帧)

queueFFT=Queue.Queue(maxsize=100)
queueAbList=Queue.Queue(maxsize=100)
queueSpecUpload=Queue.Queue(maxsize=1000)
queueIQUpload=Queue.Queue(maxsize=1000)
queueRecvQuery=Queue.Queue()


###########接受硬件上传FFT数据和异常频点并放入队列############ 
  

class ReceiveFFTThread(threading.Thread):
    def __init__(self,recvHardObj):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()
        self.recvHardObj=recvHardObj
    def stop(self):
        self.event.clear()

    def run(self):
        while(1):
            time.sleep(0.5)
            self.event.wait()
            print u'FFT_查询回复包接收线程'
            try:
                recvFFT=self.recvHardObj.ReceiveFFT()   ###recvFFT 为功率谱帧对象
                if(not recvFFT==0):
                    queueFFT.put(recvFFT)
                   
                    if(recvFFT.CommonHeader.FunctionPara==0x0D):    
                        queueSpecUpload.put(recvFFT)
            except:
                pass
              
            try:
                recvData=self.recvHardObj.ReceiveAb_Recv()
                if(not recvData==0):
                    if(recvData.CommonHeader.FunctionPara==0x0E): 
                        queueAbList.put(recvData)    
                        queueSpecUpload.put(recvData)
                    else:
                        queueRecvQuery.put(recvData)
                    
                        
            except:
                pass            

###################接收IQ数据并画图放入上传队列###############    

class ReceiveIQThread(threading.Thread):
    def __init__(self,recvHardObj,WaveFrame):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()
        self.recvHardObj=recvHardObj
        self.WaveFrame=WaveFrame
        self.Fs=5e6
    def stop(self):
        self.event.clear()

    def run(self):
        while(1):
            time.sleep(0.5)
            self.event.wait()
            print u'接收IQ数据并画图线程'
            try:
                
                recvIQ=self.recvHardObj.ReceiveIQ()
               
                if(not recvIQ==0):
                   
                    chData=[]
                    DataRate=recvIQ.Param.DataRate
                    
                    if(DataRate==0x01):self.Fs=5e6
                    elif(DataRate==0x02): self.Fs=2.5e6
                    elif(DataRate==0x03):self.Fs=1e6
                    elif(DataRate==0x04):self.Fs=0.5e6
                    elif(DataRate==0x05): self.Fs=0.1e6
                    else:
                        pass
                    print "IQ Wave BandWidth -->",self.Fs

                    DataArray=recvIQ.IQDataAmp
                    for IQData in DataArray:
                        HighIPath=IQData.HighIPath
                        HighQPath=IQData.HighQPath
                        LowIPath=IQData.LowIPath
                        LowQPath=IQData.LowQPath
                        if(HighIPath>=8):
                            IData=(HighIPath<<8)+LowIPath-2**12
                        else:
                            IData=(HighIPath<<8)+LowIPath
                        if(HighQPath>=8):
                            QData=(HighQPath)<<8+LowQPath-2**12
                        else:
                            QData=(HighQPath<<8)+LowQPath
                        chData.append(complex(IData,QData))
                
                    if(not self.WaveFrame==None):
                        self.WaveFrame.Wave(self.Fs,IData)
                    
                    queueIQUpload.put(recvIQ)
            except:
                pass
#################查询回复包解析显示线程########################
class ReceiveQueryThread(threading.Thread):
    def __init__(self,SpecFrame):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()
        self.SpecFrame=SpecFrame
    def stop(self):
        self.event.clear()
    def run(self):
        while(1):
            time.sleep(0.5)
            self.event.wait()
            print u'查询回复包显示线程'
            recvData=0
            if(not queueRecvQuery.empty()):    
                recvData=queueRecvQuery.get()

            if(not recvData==0):
                functionPara=recvData.CommonHeader.FunctionPara
                if(functionPara==0x21):     
                    self.ShowSweepRange(recvData)
                elif(functionPara==0x22):
                    self.ShowIQCentreFreq(recvData)
                elif(functionPara==0x23):
                    self.ShowPressFreq(recvData)
                elif(functionPara==0x24):
                    self.ShowRecvGain(recvData)
                elif(functionPara==0x25):
                    self.ShowSendWeak(recvData)
                elif(functionPara==0x26):
                    self.ShowTestGate(recvData)
                elif(functionPara==0x27):
                    self.ShowIQPara(recvData) 
                elif(functionPara==0x28):
                    self.ShowPressPara(recvData)
                elif(functionPara==0x29):
                    self.ShowAccessWay(recvData)
                elif(functionPara==0x2A):
                    self.ShowTransferOpen(recvData)
                elif(functionPara==0x2B):
                    self.ShowTransferClose(recvData)
                elif(functionPara==0x2C):
                    self.ShowIsConnect(recvData)
                else:
                    pass
    def ShowSweepRange(self,recvQueryData):
        if(recvQueryData.SweepRecvMode==1):
            SweepRecvMode=u"全频段"
        elif(recvQueryData.SweepRecvMode==2):
            SweepRecvMode=u"指定频段"
        elif(recvQueryData.SweepRecvMode==3):
            SweepRecvMode=u"多频段"

        if(recvQueryData.FileUploadMode==1):
            FileUploadMode=u"手动"
        elif(recvQueryData.FileUploadMode==2):
            FileUploadMode=u"不定时自动"
        elif(recvQueryData.FileUploadMode==3):
            FileUploadMode=u"抽取自动"

        dictSweep={u"扫频模式":SweepRecvMode,
                   u"文件上传模式":FileUploadMode,
                   u"频段总数": recvQueryData.SweepSectionTotalNum,
                   u"频段序号":str(recvQueryData.SweepSectionNum),
                   u"起始频段":str(recvQueryData.StartSectionNo),
                   u"终止频段":str(recvQueryData.EndSectionNo),
                   u"变化门限":str(recvQueryData.ChangeThres),
                   u"文件上传抽取率":str(recvQueryData.ExtractM)
                   }
        self.Show(8,u"扫频",dictSweep)

    def ShowIQCentreFreq(self,recvQueryData):
        FreqArray=recvQueryData.FreqArray
        Freq=[0,0,0]
        for i in range(3):
            Freq[i]=(FreqArray[i].HighFreqInteger<<6)+FreqArray[i].LowFreqInteger  \
             +float((FreqArray[i].HighFreqFraction<<8)+FreqArray[i].LowFreqFraction)/2**10
          
        dictIQFreq={
        u"定频频点个数":str(recvQueryData.FreqNum),
        u"频率值1(Mhz)": str(Freq[0]),
        u"频率值2(Mhz)": str(Freq[1]),
        u"频率值3(Mhz)": str(Freq[2])
        }
        self.Show(4,u"定频",dictIQFreq)


    def ShowIQPara(self,recvQueryData):
        DataRate=recvQueryData.DataRate
        if(DataRate==0x01):DataRate=5e6
        elif(DataRate==0x02): DataRate=2.5e6
        elif(DataRate==0x03):DataRate=1e6
        elif(DataRate==0x04):DataRate=0.5e6
        elif(DataRate==0x05): DataRate=0.1e6 

        Time=recvQueryData.TimeSet
        dictIQPara={
        u"数据率(MHz)": str(DataRate),
        u"数据块个数": str(recvQueryData.UploadNum),
        u"年": str((Time.HighYear<<4)+Time.LowYear),
        u"月":str(Time.Month),
        u"日":str(Time.Day),
        u"时":str((Time.HighHour<<2)+Time.LowHour),
        u"分":str(Time.Minute),
        u"秒":str(Time.Second)
        }
        self.Show(8,u"定频",dictIQPara)


    def ShowPressFreq(self,recvQueryData):
        FreqArray=recvQueryData.FreqArray
        Freq=[0,0]
        for i in range(2):
            Freq[i]=(FreqArray[i].HighFreqInteger<<6)+FreqArray[i].LowFreqInteger   \
             +float((FreqArray[i].HighFreqFraction<<8)+FreqArray[i].LowFreqFraction)/2**10
          
        dictPressFreq={
        u"定频频点个数":str(recvQueryData.PressNum),
        u"频率值1(Mhz)": str(Freq[0]),
        u"频率值2(Mhz)": str(Freq[1])
        }
        self.Show(3,u"压制",dictPressFreq)

    def ShowPressPara(self,recvQueryData):
        PressMode=recvQueryData.PressMode
        PressSignal=recvQueryData.PressSignal
        
        T1=(recvQueryData.HighT1<<8)+recvQueryData.LowT1
        T2=(recvQueryData.HighT2<<8)+recvQueryData.LowT2
        T3=(recvQueryData.HighT3<<8)+recvQueryData.LowT3
        T4=(recvQueryData.HighT4<<8)+recvQueryData.LowT4

        mapPressMode={1:u"单频点自动",2:u"单频点手动",3:u"双频点自动",4:u"双频点手动",5:u"不压制"}
        mapPressSignal={1:u"单频正弦" ,2:u"等幅多频" ,3:u"噪声低频",4:u"DRM信号"}

        Mode=mapPressMode[PressMode]
        Signal=mapPressSignal[PressSignal]

        dictPressPara={
        u"压制模式":Mode,
        u"信号类型":Signal,
        u"T1":str(T1),
        u"T2":str(T2),
        u"T3":str(T3),
        u"T4":str(T4)
        }
        self.Show(6,u"压制",dictPressPara)

    def ShowRecvGain(self,recvQueryData):
        recvGain=recvQueryData.RecvGain-3
        self.SpecFrame.panelQuery.SetStringItem(0,1,u"接收增益(dB)")
        self.SpecFrame.panelQuery.SetStringItem(0,2,str(recvGain))

    def ShowSendWeak(self,recvQueryData):
        sendWeak=recvQueryData.SendWeak 
        self.SpecFrame.panelQuery.SetStringItem(0,1,u"发射衰减(dB)")
        self.SpecFrame.panelQuery.SetStringItem(0,2,str(sendWeak))
    def ShowTestGate(self,recvQueryData):
        mapAdapt={
        0:3,1:10,2:20,3:25,4:30,5:40
        }
        if(recvQueryData.ThresMode==0):
            AdaptThres=mapAdapt[recvQueryData.AdaptThres]
            self.SpecFrame.panelQuery.SetStringItem(0,1,u"自适应门限")
            self.SpecFrame.panelQuery.SetStringItem(0,2,str(AdaptThres))

        else:
            FixedThres=(recvQueryData.HighFixedThres<<8)+recvQueryData.LowFixedThres
            self.SpecFrame.panelQuery.SetStringItem(0,1,u"固定门限")
            self.SpecFrame.panelQuery.SetStringItem(0,2,str(FixedThres))

    def ShowIsConnect(self,recvQueryData):
        if(recvQueryData.IsConnect==0x0F):
            IsConnect=u"在网"
        else:
            IsConnect=u"不在网"
        mapTerminalType={0:u"专业用户终端",1:u"普通用户终端",2:u"专业查询终端",3:u"普通查询终端"}
        TerminalType=mapTerminalType[recvQueryData.TerminalType]
        LonLatClass=recvQueryData.LonLatAlti
        Lon=LonLatClass.LonInteger+float((LonLatClass.HighLonFraction<<8)+LonLatClass.LowLonFraction)/2**10
        Lat=LonLatClass.LatInteger+float((LonLatClass.HighLatFraction<<8)+LonLatClass.LowLatFraction)/2**10
        Altitude=(LonLatClass.HighAltitude<<8)+LonLatClass.LowAltitude

        if(LonLatClass.LonFlag==0):
            LonFlag=u"东经"
        else:
            LonFlag=u"西经"
        if(LonLatClass.LatFlag==0):
            LatFlag=u"北纬"
        else:
            LatFlag=u"南纬"
        if(LonLatClass.AltitudeFlag==0):
            AltitudeFlag=u'海平面上'
        else:
            AltitudeFlag=u'海平面下'

        dictIsConnect={
        u"在网标志":IsConnect,
        u"终端类型":TerminalType,
        u"经度标志":LonFlag,
        u"经度":str(Lon),
        u"纬度标志":LatFlag,
        u"纬度":str(Lat),
        u"高度标志":AltitudeFlag,
        u"高度":str(Altitude)
        }
        self.Show(8,u"终端状态",dictIsConnect)

    def ShowAccessWay(self,recvQueryData):
        AccessWay=recvQueryData.AccessWay
        if(AccessWay==1):AccessWay='WiFi'
        elif(AccessWay==2):AccessWay='BlueTooth'
        elif(AccessWay==3):AccessWay='USB'
        self.SpecFrame.panelQuery.SetStringItem(0,1,u"硬件接入方式")
        self.SpecFrame.panelQuery.SetStringItem(0,2,AccessWay)
        
    def ShowTransferOpen(self,recvQueryData):
        self.SpecFrame.panelQuery.SetStringItem(0,0,u"硬件传输开启")
    def ShowTransferClose(self,recvQueryData):
        self.SpecFrame.panelQuery.SetStringItem(0,0,u"硬件传输关闭")
    
    def Show(self,lendict,string,dic):
        keys=dic.keys()
        for i in range(lendict):
            self.SpecFrame.panelQuery.SetStringItem(i,0,string)
            self.SpecFrame.panelQuery.SetStringItem(i,1,keys[i])
            self.SpecFrame.panelQuery.SetStringItem(i,2,dic[keys[i]])


################FFT画图和异常频点显示线程#####################
class DrawSpecAbListThread(threading.Thread):
    def __init__(self,SpecFrame,WaterFrame):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()
        self.SpecFrame=SpecFrame
        self.WaterFrame=WaterFrame
        self.SpecFrame.panelFigure.setSpLabel( begin_X=70e6,intv=300e6, end_X=5995e6)
    def stop(self):
        
        self.event.clear()
    def run(self):
        while(1):
            self.event.wait()
            print "FFT画图和异常频点显示线程"
            FFTObj=0
            if(not queueFFT.empty()):
                FFTObj=queueFFT.get()
            if(not FFTObj==0):
                FFTList=[]
                AllFreq1=FFTObj.AllFreq
                for FFTData in AllFreq1:
                    HighFreq1=FFTData.HighFreq1dB
                    LowFreq1=FFTData.LowFreq1dB
                    HighFreq2=FFTData.HighFreq2dB
                    LowFreq2=FFTData.LowFreq2dB
                    if(HighFreq1>=8):
                        FFTFreq1=(HighFreq1<<8)+LowFreq1-2**12
                    else:
                        FFTFreq1=(HighFreq1<<8)+LowFreq1
                    if(HighFreq2>=8):
                        FFTFreq2=(HighFreq2<<8)+LowFreq2-2**12
                    else:
                        FFTFreq2=(HighFreq2<<8)+LowFreq2
                    FFTList.append(FFTFreq1)
                    FFTList.append(FFTFreq2)
                    
                
                print " specObj.SweepRecvMode",FFTObj.SweepRecvMode
                print "specObj.FileUploadMode",FFTObj.FileUploadMode
                print  "specObj.SpecChangeFlag",FFTObj.SpecChangeFlag
                print "specObj.SweepSectionTotalNum",FFTObj.SweepSectionTotalNum
                print "specObj.CurSectionNo", FFTObj.CurSectionNo
                print "length -->" ,len(FFTList)
                
                curSectionNo=FFTObj.CurSectionNo
                self.SpecFrame.panelFigure.PowerSpectrum(FFTList,FFTObj.CommonHeader.FunctionPara,curSectionNo)
                if(self.WaterFrame):
                    self.WaterFrame.WaterFall(FFTList)
                       
            try:
                recvAbList=0
                if(not queueAbList.empty()):
                    recvAbList=queueAbList.get()
             
                if(not recvAbList==0):    
                    self.ShowAb(recvAbList)
            except:
                print u"异常频点绘制出错"
          

    def ShowAb(self,recvAbList):
        AllAbFreq=recvAbList.AllAbFreq
        CurSectionNo=recvAbList.CurSectionNo
        i=0
        for AbFreq in AllAbFreq:
            HighFreqNo=AbFreq.HighFreqNo
            LowFreqNo=AbFreq.LowFreqNo
            HighdB=AbFreq.HighdB
            LowdB=AbFreq.LowdB
            if(HighFreqNo>=8):
                FreqNo=(HighFreqNo<<8)+LowFreqNo-2**12
            else:
                FreqNo=(HighFreqNo<<8)+LowFreqNo

            Freq=82.5+25*(CurSectionNo-1)+float(25e6)/1024*FreqNo
            if(HighdB>=8):
                dB=(HighdB<<8)+LowdB-2**12
            else:
                dB=(HighdB<<8)+LowdB
            self.SpecFrame.panelQuery.SetStringItem(i,1,str('%0.2f'%Freq))
            self.SpecFrame.panelQuery.SetStringItem(i,2,str(dB))
            i=i+1

################本地功率谱存文件线程 ##############################
'''
class LocalSaveThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()
        self.SpecList=[]  #存储完整扫频段的数据
    def stop(self):
        self.event.clear()
    def run(self):
        while(1):
            self.event.wait()
            try:
                MutexqueueSpecUpload.acquire()
                if(queueSpecUpload):
                recvFFT=queueSpecUpload[0]
                recvAbList=queueSpecUpload[1]
                del queueSpecUpload[0]
                del queueSpecUpload[1]
                MutexqueueSpecUpload.release()

                changeFlag=recvFFT.SpecChangeFlag
                TotalNum=recvFFT.SweepSectionTotalNum
                if(changeFlag==15):
                    ChangeThres=3  #10dB
                elif(changeFlag==14):
                    ChangeThres=2  #20dB
                ###ExtractM 为从设置中得到的参数###############
                head=SpecUploadHeader(0x00,recvFFT.LonLatAlti,recvFFT.SweepRecvMode,
                    recvFFT.FileUploadMode,ChangeThres,extractM,TotalNum)
                blockFFT=FFTBlock(recvFFT.CurSectionNo,recvFFT.AllFreq)
                blockAb=AbListBlock(recvAbList.CurSectionNo,recvAbList.AbFreqNum,recvAbList.AllAbFreq)
                self.SpecList.append(blockFFT)
                self.SpecList.append(blockAb)
                if(len(self.SpecList)==TotalNum*2):
                    Time=recvFFT.Time
                    CommonHeader=recvFFT.CommonHeader
                    ID=CommonHeader.HighDeviceID*256+CommonHeader.LowDeviceID
                    self.WriteLocalFile(Time,ID,head,self.SpecList)
                    self.SpecList=[]
            except:
                print u'本地功率谱存文件线程出错'  
    def WriteLocalFile(self,time,ID,head,SpecList):
        Year=TimeSet.HighYear*256+TimeSet.LowYear
        Month=TimeSet.Month
        Day=TimeSet.Day
        Hour=TimeSet.HighHour*256+TimeSet.LowHour
        Minute=TimeSet.Minute
        Second=TimeSet.Second
        fileName=str(Year)+"-"+str(Month)+"-"+str(Day)+  \
                 "-"+str(Hour)+"-"+str(Minute)+"-"+Second+"-"+str(ID)+'.pwr'
        fid=open(".\LocalData\\"+ fileName,'w')
        for x in head.bytes:
            fid.write(str(x)+'\n')
        for i in xrange(len(SpecList)/2):   
            blockFFT=SpecList[2*i]
            for x in blockFFT.bytes:
                fid.write(str(x)+'\n')
        fid.write('255\n')               #分隔符
        for i in xrange(len(SpecList)/2):
            blockAb=SpecList[2*i+1]
            for x in blockAb.bytes:
                fid.write(str(x)+'\n')
        fid.write('0\n')
        fid.close()
'''
##############直接上传接受到的功率谱数据或者IQ数据####################
class UpLoadSpecThread(threading.Thread):
    def __init__(self,serveCom,extractM):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()
        self.serveCom=serveCom
        self.extractM=extractM
        self.SpecList=[]
        self.IQList=[]
    def stop(self):
        self.event.clear()
    def run(self):
        while(1):
            self.event.wait()
            self.SendSpec()
            self.SendIQ()
            time.sleep(0.5)
    
    def SendSpec(self):
        while(not queueSpecUpload.empty()):
            recvFFT=queueSpecUpload.get()
            recvAbList=queueSpecUpload.get()
            changeFlag=recvFFT.SpecChangeFlag
            TotalNum=recvFFT.SweepSectionTotalNum
            if(changeFlag==15):
                ChangeThres=3  #10dB
            elif(changeFlag==14):
                ChangeThres=2  #20dB
            ###ExtractM 为从设置中得到的参数###############
            blockFFT=FFTBlock(recvFFT.CurSectionNo,recvFFT.AllFreq)
            blockAb=AbListBlock(recvAbList.CurSectionNo,recvAbList.AbFreqNum,recvAbList.AllAbFreq)
            self.SpecList.append(blockFFT)
            self.SpecList.append(blockAb)
            if(len(self.SpecList)==TotalNum*2):   ###扫频范围的数据
                head=SpecUploadHeader(0x00,recvFFT.LonLatAlti,recvFFT.SweepRecvMode, \
                recvFFT.FileUploadMode,ChangeThres,self.extractM,TotalNum)
                
                self.serveCom.sock.send(bytearray(head))
                for i in xrange(len(self.SpecList)/2):
                    self.serveCom.sock.send(bytearray(self.SpecList[2*i]))
                self.serveCom.sock.send(0xFF)
                for i in xrange(len(self.SpecList)/2):
                    self.serveCom.sock.send(bytearray(self.SpecList[2*i+1])) 
                self.serveCom.sock.send(0x00)
                self.SpecList=[]
                
    def SendIQ(self):
        while(not queueIQUpload.empty()):
            recvIQ=queueIQUpload.get()
            block=IQBlock(recvIQ.CurBlockNo,recvIQ.IQDataAmp)
            self.IQList.append(block)
            if(len(self.IQList)==recvIQ.Param.UploadNum):
                head=IQUploadHeader(0x00,recvIQ.LonLatAlti,recvIQ.Param)
                self.serveCom.sock.send(head)
                for data in self.IQList:
                    self.serveCom.sock.send(bytearray(data))
                self.serveCom.sock.send(0x00)
                self.IQList=[]
    
    
            
            
            
        
        
                
        
        
        




            



            







                






        
