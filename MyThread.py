# -*- coding: utf-8 -*-
import threading
import wx
from Package import *
#from HardwaveAccess import *
MutexqueueFFT=threading.Lock()
MutexqueueAbList=threading.Lock()
MutexqueueSpecUpload=threading.Lock()
MutexqueueIQUpload=threading.Lock()
queueFFT=[]
queueAbList=[]
queueSpecUpload=[]
queueIQUpload=[]
dictFreqPlan={1:u"固定",2:u"移动",3:u"无线电定位",4:u"卫星固定",5:u"空间研究",6:u"卫星地球探测",
              7:u"射电天文",8:u"广播",9:u"移动(航空移动除外)",10:u"无线电导航",11:u"航空无线电导航",
              12:u"水上移动",13:u"卫星移动",14:u"卫星间",15:u"卫星无线电导航",16:u"业余",17:u"卫星气象",18:u"标准频率和时间信号",
              19:u"空间操作",20:u"航空移动",21:u"卫星业余",22:u"卫星广播",23:u"航空移动(OR)",
              24:u"气象辅助",25:u"航空移动(R)",26:u"水上无线电导航",27:u"陆地移动",28:u"移动(航空移动(R)除外)",
              29:u"卫星无线电测定",30:u"卫星航空移动(R)",31:u"移动(航空移动(R)除外)",32:u"水上移动(遇险和呼叫)",
              33:u"水上移动(使用DSC的遇险和安全呼叫)",34:u"未划分"}

###########接受硬件上传FFT数据和异常频点并放入队列############    
'''
class ReceiveFFTThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()

    def stop(self):
        self.event.clear()

    def run(self):
        while(1):
            self.event.wait()
            try:
                MutexqueueFFT.acquire()
                recvFFT=ReceiveFFT()
                if(recvFFT):
                    queueFFT.append(recvFFT)
                    MutexqueueSpecUpload.acquire()
                    queueSpecUpload.append(recvFFT)
            except:
                print u"接收硬件上传FFT帧出错"
            finally:
                MutexqueueFFT.release()   
            try:
                MutexqueueAbList.acquire()
                recvAbList=ReceiveAbList()
                if(recvAbList):
                    queueAbList.append(recvAbList)    
                    queueSpecUpload.append(recvAbList)
                
            except:
                print u"接收硬件上传异常频点出错"
            finally:
                MutexqueueSpecUpload.release()
                MutexqueueAbList.release()  

###################接收IQ数据并画图放入上传队列###############    

class ReceiveIQThread(threading.Thread):
    def __init__(self,WaveFrame):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()
        self.WaveFrame=WaveFrame
        self.Fs=5e6
    def stop(self):
        self.event.clear()

    def run(self):
        while(waveShow):
            self.event.wait()
            try:
                recvIQ=ReceiveIQ()  
                if(recvIQ):
                    chData=[]
                    DataRate=recvIQ.IQDataPartHead.DataRate
                    if(DataRate==0x01):self.Fs=5e6
                    elif(DataRate==0x02): self.Fs=2.5e6
                    elif(DataRate==0x03):self.Fs=1e6
                    elif(DataRate==0x04):self.Fs=0.5e6
                    elif(DataRate==0x05): self.Fs=0.1e6 
                    print "IQ Wave BandWidth -->",self.Fs

                    DataArray=recvIQ.IQDataAmp
                    for IQData in DataArray:
                        HighIPath=IQData.HighIPath
                        HighQPath=IQData.HighQPath
                        LowIPath=IQData.LowIPath
                        LowQPath=IQData.LowQPath
                        if(HighIPath<0):
                            IData=(-1)*(abs(HighIPath)*256+LowIPath)
                        else:
                            IData=HighIPath*256+LowIPath
                        if(HighQPath<0):
                            QData=(-1)*(abs(HighQPath)*256+LowQPath)
                        else:
                            QData=HighQPath*256+LowQPath
                        chData.append(complex(IData,QData))
                    try:
                        self.WaveFrame.Wave(self.Fs,chData)
                    except wx.PyDeadObjectError:
                        pass

                    try:
                        MutexqueueIQUpload.acquire()
                        queueIQUpload.append(recvIQ)
                    finally:
                        MutexqueueIQUpload.release()
            except:
                print u'接收IQ数据并画图放入上传队列出错'

#################接收查询回复包线程########################
class ReceiveQueryThread(threading.Thread):
    def __init__(self,SpecFrame):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()
        self.SpecFrame=SpecFrame
    def stop(self):
        self.event.clear()
    def run(self):
        while(specShow):
            self.event.wait()
            recvQueryData=ReceiveQueryData()
            if(recvQueryData):

                functionPara=revQueryData.CommonHeader.FunctionPara
                if(functionPara==0x21):     
                    self.ShowSweepRange(recvQueryData)
                elif(functionPara==0x22):
                    self.ShowIQCentreFreq(recvQueryData)
                elif(functionPara==0x23):
                    self.ShowPressFreq(recvQueryData)
                elif(functionPara==0x24):
                    self.ShowRecvGain(recvQueryData)
                elif(functionPara==0x25):
                    self.ShowSendWeak(recvQueryData)
                elif(functionPara==0x26):
                    self.ShowTestGate(recvQueryData)
                elif(functionPara==0x27):
                    self.ShowIQPara(recvQueryData) 
                elif(functionPara==0x28):
                    self.ShowPressPara(recvQueryData)
                elif(functionPara==0x29):
                    self.ShowAccessWay(recvQueryData)
                elif(functionPara==0x2A):
                    self.ShowTransferOpen(recvQueryData)
                elif(functionPara==0x2B):
                    self.ShowTransferClose(recvQueryData)
                elif(functionPara==0x2C):
                    self.ShowIsConnect(recvQueryData)
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
                   u"频段序号":recvQueryData.SweepSectionNum,
                   u"起始频段":recvQueryData.StartSectionNo,
                   u"终止频段":recvQueryData.EndSectionNo,
                   u"变化门限":recvQueryData.ChangeThres,
                   u"文件上传抽取率":recvQueryData.ExtractM
                   }
        self.Show(8,u"扫频",dictSweep)

    def ShowIQCentreFreq(self,recvQueryData):
        FreqArray=recvQueryData.FreqArray
        Freq=[0,0,0]
        for i in range(3):
            Freq[i]=FreqArray[i].HighFreqInteger*256+FreqArray[i].LowFreqInteger  \
             +float(FreqArray[i].HighFreqFraction*256+FreqArray[i].LowFreqFraction)/2**10
          
        dictIQFreq={
        u"定频频点个数":recvQueryData.FreqNum,
        u"频率值1(Mhz)": Freq[0],
        u"频率值2(Mhz)": Freq[1],
        u"频率值3(Mhz)": Freq[2]
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
        u"数据率(MHz)": DataRate,
        u"数据块个数": recvQueryData.UploadNum,
        u"年": Time.HighYear*256+Time.LowYear,
        u"月":Time.Month,
        u"日":Time.Day,
        u"时":Time.HighHour*256+Time.LowHour,
        u"分":Time.Minute,
        u"秒":Time.Second
        }
        self.Show(8,u"定频",dictIQPara)


    def ShowPressFreq(self,recvQueryData):
        FreqArray=recvQueryData.FreqArray
        Freq=[0,0]
        for i in range(2):
            Freq[i]=FreqArray[i].HighFreqInteger*256+FreqArray[i].LowFreqInteger   \
             +float(FreqArray[i].HighFreqFraction*256+FreqArray[i].LowFreqFraction)/2**10
          
        dictPressFreq={
        u"定频频点个数":recvQueryData.PressNum,
        u"频率值1(Mhz)": Freq[0],
        u"频率值2(Mhz)": Freq[1]
        }
        self.Show(3,u"压制",dictPressFreq)

    def ShowPressPara(self,recvQueryData):
        PressMode=recvQueryData.PressMode
        PressSignal=recvQueryData.PressSignal
        
        T1=recvQueryData.HighT1*256+recvQueryData.LowT1
        T2=recvQueryData.HighT2*256+recvQueryData.LowT2
        T3=recvQueryData.HighT3*256+recvQueryData.LowT3
        T4=recvQueryData.HighT4*256+recvQueryData.LowT4

        mapPressMode={1:u"单频点自动",2:u"单频点手动",3:u"双频点自动",4:u"双频点手动",5:u"不压制"}
        mapPressSignal={1:u"单频正弦" ,2:u"等幅多频" ,3:u"噪声低频",4:u"DRM信号"}

        Mode=mapPressMode[PressMode]
        Signal=mapPressSignal[PressSignal]

        dictPressPara={
        u"压制模式":Mode,
        u"信号类型":Signal,
        u"T1":T1,
        u"T2":T2,
        u"T3":T3,
        u"T4":T4
        }
        self.Show(6,u"压制",dictPressPara)

    def ShowRecvGain(self,recvQueryData):
        recvGain=recvQueryData.recvGain-3
        self.SpecFrame.panelQuery.SetStringItem(0,1,u"接收增益(dB)")
        self.SpecFrame.panelQuery.SetStringItem(0,2,recvGain)

    def ShowSendWeak(self,recvQueryData):
        sendWeak=recvQueryData.SendWeak 
        self.SpecFrame.panelQuery.SetStringItem(0,1,u"发射衰减(dB)")
        self.SpecFrame.panelQuery.SetStringItem(0,2,sendWeak)
    def ShowTestGate(self,recvQueryData):
        mapAdapt={
        0:3,1:10,2:20,3:25,4:30,5:40
        }
        if(recvQueryData.ThresMode==0):
            AdaptThres=mapAdapt[recvQueryData.AdaptThres]
            self.SpecFrame.panelQuery.SetStringItem(0,1,u"自适应门限")
            self.SpecFrame.panelQuery.SetStringItem(0,2,AdaptThres)

        else:
            FixedThres=recvQueryData.HighFixedThres*256+recvQueryData.LowFixedThres
            self.SpecFrame.panelQuery.SetStringItem(0,1,u"固定门限")
            self.SpecFrame.panelQuery.SetStringItem(0,2,FixedThres)

    def ShowIsConnect(self,recvQueryData):
        if(recvQueryData.IsConnect==0x0F):
            IsConnect=u"在网"
        mapTerminalType={0:u"专业用户终端",1:u"普通用户终端",2:u"专业查询终端",3:u"普通查询终端"}
        TerminalType=mapTerminalType[recvQueryData.TerminalType]
        LonLatClass=recvQueryData.LonLatAlti
        Lon=LonLatClass.LonInteger+float(LonLatClass.HighLonFraction*256+LonLatClass.LowLonFraction)/2**10
        Lat=LonLatClass.LatInteger+float(LonLatClass.HighLatFraction*256+LonLatClass.LowLatFraction)/2**10
        Altitude=LonLatClass.HighAltitude*256+LonLatClass.LowAltitude

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
        u"经度":Lon,
        u"纬度标志":LatFlag,
        u"纬度":Lat,
        u"高度标志":AltitudeFlag,
        u"高度":Altitude
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
    def __init__(self,SpecFrame):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()
        self.SpecFrame=SpecFrame
    def stop(self):
        self.event.clear()
    def run(self):
        while(1):
            self.event.wait()
            try:
                MutexqueueFFT.acquire()
                if(queueFFT):
                    FFTList=[]
                    FFTObj=queueFFT[0]
                    del queueFFT[0]
                    MutexqueueFFT.release()

                    SweepTotalSection=FFTObj.SweepSectionTotalNum
                    CurSectionNo=FFTObj.CurSectionNo
                    AllFreq=FFTObj.AllFreq
                    for FFTData in AllFreq:
                        HighFreq1=FFTData.HighFreq1dB
                        LowFreq1=FFTData.LowFreq1dB
                        HighFreq2=FFTData.HighFreq2dB
                        LowFreq2=FFTData.LowFreq2dB
                        if(HighFreq1<0):
                            FFTFreq1=(-1)*(abs(HighFreq1)*256+LowFreq1)
                        else:
                            FFTFreq1=HighFreq1*256+LowFreq1
                        if(HighFreq2<0):
                            FFTFreq2=(-1)*(abs(HighFreq2)*256+LowFreq2)
                        else:
                            FFTFreq2=HighFreq2*256+LowFreq2
                        FFTList.append(FFTFreq1)
                        FFTList.append(FFTFreq2)
                    try:
                        self.SpecFrame.panelFigure.PowerSpectrum(FFTList)
                    except wx.PyDeadObjectError:
                        pass     
            except:
                print u'FFT画图出错'
            try:
                MutexqueueAbList.acquire()
                if(queueAbList):
                    recvAbList=queueAbList[0]
                    del queueAbList[0]
                    MutexqueueAbList.release() 
                    
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
            if(HighFreqNo<0):
                FreqNo=(-1)*(abs(HighFreqNo)*256+LowFreqNo)
            else:
                FreqNo=HighFreqNo*256+LowFreqNo

            Freq=82.5+25*(CurSectionNo-1)+float(25e6)/1024*FreqNo
            if(HighdB<0):
                dB=(-1)*(abs(HighdB)*256+LowdB)
            else:
                dB=HighdB*256+LowdB
            self.SpecFrame.panelQuery.SetStringItem(i,1,Freq)
            self.SpecFrame.panelQuery.SetStringItem(i,2,dB)
            i=i+1

################本地功率谱存文件线程 ##############################
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
##############本地IQ波形文件存储#################################
#class LocalSaveThread()

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


            




            



            







                






        
