# -*- coding: utf-8 -*-
import socket
from Package import *

###########下面是接收字节转结构体对象###########

class RecvHardWaveData():
    def __init__(self,inPointFFT,inPointIQ,inPointAb):
        self.inPointFFT=inPointFFT
        self.inPointAb=inPointAb
        self.inPointIQ=inPointIQ
    def ReceiveFFT(self):
        li=list(self.inPointFFT.read(1560))
        specObj=SpecDataRecv()
        specObj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
        specObj.LonLatAlti=LonLatAltitude(li[4],li[5],li[6],li[7],li[8]>>7, \
                                        li[8]&0x7F,li[9],li[10],li[11]>>7,li[11]&0x7F,li[12])
       
        specObj.Time=TimeSet(li[13],li[14]>>4,li[14]&0x00F,li[15]>>3,  \
                            li[15]&0x07,li[16]>>6,li[16]&0x03,li[17])
        specObj.SweepRecvMode=li[18]>>6
        specObj.FileUploadMode=(li[18]&0x30)>>4
        specObj.SpecChangeFlag=li[18]&0x0F
        specObj.SweepSectionTotalNum=li[19]
        specObj.CurSectionNo=li[20]
        specObj.CommonTail=FrameTail(li[1557],li[1558],li[1559])
        i=0
        while(i<512):
            specObj.AllFreq[i]=TwoFreq(li[21+i*3]>>4,li[21+i*3]&0x0F,li[22+i*3],li[23+i*3])
            i=i+1
        return specObj
       
    def ReceiveAb_Recv(self):
        li=list(self.inPointAb.read(56))
        if(li[1]==0x0E):
            abObj=AbFreqRecv()
            abObj.CommonHeader=FrameHeader(li[0],li[1],li[2],li[3])
            abObj.LonLatAlti=LonLatAltitude(li[4],li[5],li[6],li[7],li[8]>>7, \
                                        li[8]&0x7F,li[9],li[10],li[11]>>7,li[11]&0x7F,li[12])
       
            abObj.Time=TimeSet(li[13],li[14]>>4,li[14]&0x00F,li[15]>>3,  \
                            li[15]&0x07,li[16]>>6,li[16]&0x03,li[17])
            
            abObj.CurSectionNo=li[18]
            abObj.AbFreqNum=li[19]
            abObj.CommonTail=FrameTail(li[50],li[51],li[52])
            i=0
            while(i<li[19]):
                abObj.AllAbFreq[i]=AbFreq(li[20+i*3]>>4,li[20+i*3]&0x0F,li[21+i*3],li[22+i*3])
                i=i+1
            return abObj
        else:
            if(li[1]==0x21):
                obj=self.ByteToSweepRange(li)
            elif(li[i]==0x22):
                obj=self.ByteToIQFreq(li)
            elif(li[i]==0x23):
                obj=self.ByteToPressFreq(li)
            
    def ByteToSweepRange(self):
        pass
    def ByteToIQFreq(self):
        pass
    def ByteToPressFreq(self):
        pass
    def ByteToRecvGain(self):
        pass
    def ByteToSendWeak(self):
        pass
    def ByteToThres(self):
        pass
    def ByteToIQPara(self):
        pass
    def ByteToPressPara(self):
        pass
    def ByteToAccessWay(self):
        pass
    def ByteToTransferOpen(self):
        pass
    def ByteToTransferClose(self):
        pass
    def ByteToTransferOpen(self):
        pass
    
                
        
    def ReceiveIQ(self):
        pass

#####################发给中心站的查询指令#######################
class ServerCommunication():
    def __init__(self):
        self.sock=0
    def ConnectToServer(self):
  
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('115.156.209.216',9123))
        print 'Client connect !' 
        self.sock=sock
    

    def SendQueryData(self,frameLen,structrueObj):
        barray=bytearray(structrueObj)
        self.sock.send(barray)

    def DisconnectToServer(self):
        self.sock.close()

