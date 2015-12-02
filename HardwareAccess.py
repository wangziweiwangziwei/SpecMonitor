# -*- coding: utf-8 -*-
import socket
from Package import *

###########下面是接收字节转结构体对象###########

class RecvHardwaveData():
    def __init__(self,inPointFFT,inPointIQ,inPointAb):
        self.inPointFFT=inPointFFT
        self.inPointAb=inPointAb
        self.inPointIQ=inPointIQ
    def ReceiveFFT(self):
        li=list(self.inPointFFT.read(2000,100))
        if(not len(li)==1560):
            return 0
        
        specObj=SpecDataRecv()
        specObj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        specObj.LonLatAlti=LonLatAltitude(li[4],li[5],li[6],li[7],li[8]>>7, \
                                        li[8]&0x7F,li[9],li[10],li[11]>>7,  \
                                        li[11]&0x7F,li[12])
       
        specObj.Time=TimeSet(li[13],li[14]>>4,li[14]&0x0F,li[15]>>3,  \
                            li[15]&0x07,li[16]>>6,li[16]&0x03,li[17])
        specObj.SweepRecvMode=li[18]>>6
        specObj.FileUploadMode=(li[18]&0x30)>>4
        specObj.SpecChangeFlag=li[18]&0x0F
        specObj.SweepSectionTotalNum=li[19]
        specObj.CurSectionNo=li[20]
        specObj.CommonTail=FrameTail(li[1557],li[1558],li[1559])
        i=0
        while(i<512):
            specObj.AllFreq[i]=TwoFreq(li[21+i*3]>>4,li[21+i*3]&0x0F, \
                li[22+i*3],li[23+i*3])
            i=i+1
        '''
        print " specObj.SweepRecvMode",specObj.SweepRecvMode
        print "specObj.FileUploadMode",specObj.FileUploadMode
        print  "specObj.SpecChangeFlag",specObj.SpecChangeFlag
        print "specObj.SweepSectionTotalNum",specObj.SweepSectionTotalNum
        print "specObj.CurSectionNo", specObj.CurSectionNo
        i=0
        while(i<512):
            print 'freq  '+str(i)+"--" +str(li[21+i*3]>>4)+"--"+str(li[21+i*3]&0x0F)+"--"+str(li[22+i*3])+"--"+str(li[23+i*3])
            i=i+1
        '''
        return specObj
        
    def ReceiveAb_Recv(self):
        li=list(self.inPointAb.read(200,100))
        if(li[1]==0x0E):
            abObj=AbFreqRecv()
            abObj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
            abObj.LonLatAlti=LonLatAltitude(li[4],li[5],li[6],li[7],li[8]>>7, \
                                        li[8]&0x7F,li[9],li[10],li[11]>>7,  \
                                        li[11]&0x7F,li[12])
       
            abObj.Time=TimeSet(li[13],li[14]>>4,li[14]&0x00F,li[15]>>3,  \
                            li[15]&0x07,li[16]>>6,li[16]&0x03,li[17])
            
            abObj.CurSectionNo=li[18]
            abObj.AbFreqNum=li[19]
            abObj.CommonTail=FrameTail(li[50],li[51],li[52])
            i=0
            while(i<li[19]):
                abObj.AllAbFreq[i]=AbFreq(li[20+i*3]>>4,li[20+i*3]&0x0F,  \
                    li[21+i*3],li[22+i*3])
                i=i+1
            return abObj
        else:
            
            if(li[1]==0x21):
                obj=self.ByteToSweepRange(li)
            elif(li[1]==0x22):
                obj=self.ByteToIQFreq(li)
            elif(li[1]==0x23):
                obj=self.ByteToPressFreq(li)
            elif(li[1]==0x24):
                obj=self.ByteToRecvGain(li)
            elif(li[1]==0x25):
                obj=self.ByteToSendWeak(li)
            elif(li[1]==0x26):
                obj=self.ByteToThres(li)
            elif(li[1]==0x27):
                obj=self.ByteToIQPara(li)
            elif(li[1]==0x28):
                obj=self.ByteToPressPara(li)
            elif(li[1]==0x29):
                obj=self.ByteToAccessWay(li)
            elif(li[1]==0x2A):
                obj=self.ByteToTransferOpen(li)
            elif(li[1]==0x2B):
                obj=self.ByteToTransferClose(li)
            elif(li[1]==0x2C):
                obj=self.ByteToWorkMode(li)
                
            return obj    
            
    def ByteToSweepRange(self,li):
        obj=SweepRangeSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.SweepRecvMode=li[4]>>2
        obj.FileUploadMode=li[4]&0x03
        obj.SweepSectionTotalNum=li[5]
        obj.SweepSectionNo=li[6]

        obj.StartSectionNo=li[7]
        obj.HighStartFreq=li[8]
        obj.LowStartFreq=li[9]

        obj.EndSectionNo=li[10]
        obj.HighEndFreq=li[11]
        obj.LowEndFreq=li[12]
        obj.SpecChangeFlag=li[13]>>6
        obj.ExtractM=li[13]&0x3F
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj
    def ByteToIQFreq(self,li):
        obj=IQFreqSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.FreqNum=li[4]
        for i in range(3):
            obj.FreqArray[i]=CentreFreq(li[5+3*i],li[6+3*i]>>6, \
                li[6+3*i]&0x3F,li[7+3*i])
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj
         
    def ByteToPressFreq(self,li):
        obj=PressFreqSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.PressNum=li[4]
        for i in range(2):
            obj.FreqArray[i]=CentreFreq(li[5+3*i],li[6+3*i]>>6,  \
                li[6+3*i]&0x3F,li[7+3*i])
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj


    def ByteToRecvGain(self,li):
        obj=RecvGainSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.RecvGain=li[4]
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj
        
    def ByteToSendWeak(self,li):
        obj=SendWeakSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.RecvGain=li[4]
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj

    def ByteToThres(self,li):
        obj=ThresSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.ThresMode=li[4]
        obj.AdaptThres=li[5]
        obj.HighFixedThres=li[8]
        obj.LowFixedThres=li[9]
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj
    def ByteToIQPara(self,li):
        obj=IQParaSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.BandWidth=li[4]>>4
        obj.DataRate=li[4]&0x0F
        obj.UploadNum=li[5]
        obj.Time=TimeSet(li[6],li[7]>>4,li[7]&0x0F,li[8]>>3,  \
                            li[8]&0x07,li[9]>>6,li[9]&0x03,li[10])
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj

    def ByteToPressPara(self,li):
        obj=PressParaSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.PressMode=li[4]
        obj.PressSignal=li[5]>>4
        obj.PressSignalBandWidth=li[5]&0x0F
        obj.HighT1=li[6]
        obj.LowT1=li[7]
        obj.HighT2=li[8]
        obj.LowT2=li[9]
        obj.HighT3=li[10]
        obj.LowT3=li[11]
        obj.HighT4=li[12]
        obj.LowT4=li[13]
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj
        
    def ByteToAccessWay(self,li):
        obj=AccessWaySet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.AccessWay=li[4]
        obj.CommonTail=FrameTail(li[14],li[15],li[16])
        return obj
        
    def ByteToTransferOpen(self,li):
        obj=TransferSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.CommonTail=FrameTail(li[4],li[5],li[6])
        return obj
        
    def ByteToTransferClose(self,li):
        obj=TransferSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.CommonTail=FrameTail(li[4],li[5],li[6])
        return obj
        
    def ByteToWorkMode(self,li):
        obj=RecvGainSet()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.IsConnect=li[4]
        obj.TernminalType=li[5]
        obj.LonLatAlti=LonLatAltitude(li[6],li[7],li[8],li[9],li[10]>>7, \
                                        li[10]&0x7F,li[11],li[12],li[13]>>7,  \
                                        li[13]&0x7F,li[14])
        obj.CommonTail=FrameTail(li[15],li[16],li[17])
        return obj        
        
    def ReceiveIQ(self):
        li=list(self.inPointIQ.read(7000,200))
        if(not len(li)==6028):
            return 0
        print "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC%d" %(len(li))
        obj=IQData()
        obj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        obj.LonLatAlti=LonLatAltitude(li[4],li[5],li[6],li[7],li[8]>>7, \
                                        li[8]&0x7F,li[9],li[10],li[11]>>7,  \
                                        li[11]&0x7F,li[12])

        
        obj.Time=TimeSet(li[13],li[14]>>4,li[14]&0x0F,li[15]>>3,  \
                            li[15]&0x07,li[16]>>6,li[16]&0x03,li[17])
        
        obj.Param=IQDataPartHead(li[18],li[19]>>6,li[19]&0x3F,li[20],li[21]>>4, \
                                  li[21]&0x0F,li[22])
        obj.CurBlockNo=li[23]
        for i in xrange(2000):
            obj.IQDataAmp[i]=FreqIQ(li[24+3*i]>>4,li[24+3*i]&0x0F,li[25+3*i],li[26+3*i])

        obj.CommonTail=FrameTail(li[6024],li[6025],li[6026])
        return obj
        

#####################发给中心站的查询指令#######################
class ServerCommunication():
    def __init__(self):
        self.sock=0
    def ConnectToServer(self):
  
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('115.156.209.95',9123))
        print 'Client connect !' 
        self.sock=sock
    

    def SendQueryData(self,frameLen,structrueObj):
        barray=bytearray(structrueObj)
        self.sock.send(barray)

    def DisconnectToServer(self):
        self.sock.close()

