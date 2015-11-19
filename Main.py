# -*- coding: utf-8 -*-
import wx
from IQWave import  WaveIQ
from Spectrum import Spec
from WaterFall import Water 
from DemodEye import Eye
from DemodConstel import Constel
from DemodCCDF import CCDF

from GlobalList import *
import matplotlib 
import os
import AllDialog
from HardwareAccess import *
from Package import *
from MyThread import *
import usb
import time

class MainWindow(wx.MDIParentFrame):
    def __init__(self):
        wx.MDIParentFrame.__init__(self,None,-1,u"频谱监测",style=wx.DEFAULT_FRAME_STYLE)
        self.SetSize((wx.Display().GetClientArea().GetWidth(),wx.Display().GetClientArea().GetHeight()))
        #icon=wx.Image("./icons/icon.png",wx.BITMAP_TYPE_PNG).Scale(16,16).ConvertToBitmap()
        #self.SetIcon(wx.IconFromBitmap(icon))
        self.Centre()
        self.MakeMenuBar()
        self.SetBackgroundColour((242,245,250))
        matplotlib.rcParams["figure.facecolor"] = '#F2F5FA'
        matplotlib.rcParams["axes.facecolor"] = '0'
        matplotlib.rcParams["ytick.color"] = '0'
        matplotlib.rcParams["xtick.color"] = '0'
        matplotlib.rcParams["grid.color"] = 'w'
        matplotlib.rcParams["text.color"] = 'w'
        matplotlib.rcParams["figure.edgecolor"]="0"
        matplotlib.rcParams["xtick.labelsize"]=12
        matplotlib.rcParams["ytick.labelsize"]=12
        matplotlib.rcParams["axes.labelsize"]=14
        matplotlib.rcParams["grid.linestyle"]="-"
        matplotlib.rcParams["grid.linewidth"]=0.5
        matplotlib.rcParams["grid.color"]='#707070'
       

        self.SpecFrame=None
        self.WaterFrame=None
        self.WaveFrame=None 
        self.DemodWaveFrame=None
        self.DemodConstelFrame=None
        self.DemodCCDFFrame=None
        self.DemodEyeFrame=None

        self.SpecFrame=Spec(self)
        self.SpecFrame.Show()
        self.Tile(wx.VERTICAL)
        global specShow
        specShow=True
        self.Bind(wx.EVT_WINDOW_DESTROY,self.OnCloseSpecFrame,self.SpecFrame)

        self.serverCom=ServerCommunication()
        
        #################硬件端口定义##############
        self.inPoint1=0
        self.inPoint2=0
        self.inPoint3=0
        self.outPoint=0
        
        ################公共帧###################
        self.tail=FrameTail(0,0,0xAA)
        
        ###############编码表##############
        self.dictThres={3:0x00,10:0x01,20:0x02,25:0x03,30:0x04,40:0x05}
    def OnCloseSpecFrame(self,event):
        self.SpecFrame=None
        global specShow
        specShow=False

    def OnCloseWaveFrame(self,event):
        self.WaveFrame=None
        global waveShow
        waveShow=False

    def OnCloseWaterFrame(self,event):
        self.WaterFrame=None
        global waterShow
        waterShow=False
    def OnCloseDemodWaveFrame(self,event):
        self.DemodWaveFrame=None
        global demodWaveShow
        demodWaveShow=False
    
    def OnCloseDemodConstelFrame(self,event):
        self.DemodConstelFrame=None
        global demodConstelShow
        demodConstelShow=False

    def OnCloseDemodEyeFrame(self,event):
        self.DemodEyeFrame=None
        global demodEyeShow
        demodEyeShow=False
    
    def OnCloseDemodCCDFFrame(self,event):
        self.DemodCCDFFrame=False
        global demodCCDFShow
        demodCCDFShow=False
    

    def MakeMenuBar(self):
        self.menubar=wx.MenuBar()
           
        self.filemenu=wx.Menu()
        i=self.filemenu.Append(-1,u"开启上传")
        self.Bind(wx.EVT_MENU,self.OnStartTransfer,i)  
        self.filemenu.AppendSeparator()
        i=self.filemenu.Append(-1,u"关闭上传")
        self.Bind(wx.EVT_MENU,self.OnCloseTransfer,i)    
        self.filemenu.AppendSeparator()
        i=self.filemenu.Append(-1,u"接入方式...")
        self.Bind(wx.EVT_MENU,self.OnSetAccessWay,i) 
        self.menubar.Append(self.filemenu,u"&硬件控制")

        self.display_menu=wx.Menu()
        i= self.display_menu.Append(-1,u"接收增益")
        self.Bind(wx.EVT_MENU,self.OnSetRecvGain,i)
        self.display_menu.AppendSeparator()
        i= self.display_menu.Append(-1,u"发射衰减")
        self.Bind(wx.EVT_MENU,self.OnSetSendWeak,i)
        self.display_menu.AppendSeparator()
        i= self.display_menu.Append(-1,u"检测门限")
        self.Bind(wx.EVT_MENU,self.OnSetThres,i)
        self.display_menu.AppendSeparator()
        submenu=wx.Menu()
        i1=submenu.Append(-1,u"压制公共参数")
        i2=submenu.Append(-1,u"单频点压制")
        i3=submenu.Append(-1,u"双频点压制")
        self.Bind(wx.EVT_MENU,self.OnSetPressPara,i1)
        self.Bind(wx.EVT_MENU,self.OnSetPressOne,i2)
        self.Bind(wx.EVT_MENU,self.OnSetPressTwo,i3)
        self.display_menu.AppendMenu(-1,u"压制发射...",submenu)
        self.menubar.Append(self.display_menu,u"&参数设置")

        self.setting_menu=wx.Menu()
        i=self.setting_menu.Append(-1,u"全频段...")
        self.Bind(wx.EVT_MENU,self.OnSetFullSweep,i)
        self.setting_menu.AppendSeparator()
        i=self.setting_menu.Append(-1,u"指定频段...")
        self.Bind(wx.EVT_MENU,self.OnSetSpecialSweep,i)
        self.setting_menu.AppendSeparator()
        i=self.setting_menu.Append(-1,u"多频段...")
        self.Bind(wx.EVT_MENU,self.OnSetMutiSweep,i)
        self.menubar.Append(self.setting_menu,u"&扫频设置")

        self.linkmenu=wx.Menu()
        i= self.linkmenu.Append(-1,u"定频公共参数")
        self.Bind(wx.EVT_MENU,self.OnSetIQPara,i)
        self.setting_menu.AppendSeparator()
        i=self.linkmenu.Append(-1,u"定频频点频率")
        self.Bind(wx.EVT_MENU,self.OnSetIQFreq,i)
        
        self.menubar.Append(self.linkmenu,u"&定频设置")


        self.commandmenu=wx.Menu()
        i=self.commandmenu.Append(-1,u"扫频范围")
        self.Bind(wx.EVT_MENU,self.OnQuerySweepRange,i)
        self.commandmenu.AppendSeparator()
        submenu=wx.Menu()
        i1=submenu.Append(-1,u"定频接收频率")
        i2=submenu.Append(-1,u"定频接收参数")
        self.Bind(wx.EVT_MENU,self.OnQueryIQFreq,i1)
        self.Bind(wx.EVT_MENU,self.OnQueryIQPara,i2)
        self.commandmenu.AppendMenu(-1,u"定频参数",submenu)
        self.commandmenu.AppendSeparator()

        submenu=wx.Menu()
        i1=submenu.Append(-1,u"压制发射频率")
        i2=submenu.Append(-1,u"压制发射参数")
        self.Bind(wx.EVT_MENU,self.OnQueryPressFreq,i1)
        self.Bind(wx.EVT_MENU,self.OnQueryPressPara,i2)
        self.commandmenu.AppendMenu(-1,u"压制参数",submenu)

        self.commandmenu.AppendSeparator()
        i=self.commandmenu.Append(-1,u"接收增益")
        self.Bind(wx.EVT_MENU,self.OnQueryRecvGain,i)
        self.commandmenu.AppendSeparator()
        i=self.commandmenu.Append(-1,u"发射衰减")
        self.Bind(wx.EVT_MENU,self.OnQuerySendWeak,i)
        self.commandmenu.AppendSeparator()
        i=self.commandmenu.Append(-1,u"检测门限")
        self.Bind(wx.EVT_MENU,self.OnQueryThres,i)
        self.commandmenu.AppendSeparator()
        i=self.commandmenu.Append(-1,u"硬件接入方式")
        self.Bind(wx.EVT_MENU,self.OnQueryAccessWay,i)
        self.commandmenu.AppendSeparator()
        i=self.commandmenu.Append(-1,u"硬件是否开启")
        self.Bind(wx.EVT_MENU,self.OnQueryTransferOn,i)
        self.commandmenu.AppendSeparator()
        i=self.commandmenu.Append(-1,u"硬件是否关闭")
        self.Bind(wx.EVT_MENU,self.OnQueryTransferOff,i)
        self.menubar.Append(self.commandmenu,u"&查询")

        self.uploadmenu=wx.Menu()
        submenu=wx.Menu()
        i1=submenu.Append(-1,u"功率谱文件")
        i2=submenu.Append(-1,u"IQ波形文件")
        self.uploadmenu.AppendMenu(-1,u"本地存储",submenu)
        self.Bind(wx.EVT_MENU,self.OnLocalSaveSpec,i1)
        self.Bind(wx.EVT_MENU,self.OnLocalSaveWave,i2)

        self.uploadmenu.AppendSeparator()
        submenu=wx.Menu()
        i1=submenu.Append(-1,u"功率谱文件")
        i2=submenu.Append(-1,u"IQ波形文件")
        self.uploadmenu.AppendMenu(-1,u"文件上传",submenu)
        self.Bind(wx.EVT_MENU,self.OnUploadSpec,i1)
        self.Bind(wx.EVT_MENU,self.OnUploadWave,i2)
        self.menubar.Append(self.uploadmenu,u"&文件处理")
        
        self.servicemenu=wx.Menu()
        i=self.servicemenu.Append(-1,u"入网请求\tCTRL+O")
        self.Bind(wx.EVT_MENU,self.OnConnect,i)
        self.servicemenu.AppendSeparator()
        i=self.servicemenu.Append(-1,u"电磁态势数据请求")
        self.Bind(wx.EVT_MENU,self.OnReqElecTrend,i)
        self.servicemenu.AppendSeparator()
        i=self.servicemenu.Append(-1,u"电磁路径数据请求")
        self.servicemenu.AppendSeparator()
        self.Bind(wx.EVT_MENU,self.OnReqElecPath,i)
        i=self.servicemenu.Append(-1,u"异常频点定位请求")
        self.servicemenu.AppendSeparator()
        self.Bind(wx.EVT_MENU,self.OnReqAbFreq,i)

        submenu=wx.Menu()
        i1=submenu.Append(-1,u"台站登记属性")
        i2=submenu.Append(-1,u"登记台站当前属性")
        i3=submenu.Append(-1,u"全部台站记录属性")
        self.Bind(wx.EVT_MENU,self.OnQueryStationPro,i1)
        self.Bind(wx.EVT_MENU,self.OnQueryCurStationPro,i2)
        self.Bind(wx.EVT_MENU,self.OnQueryAllStationPro,i3)
        self.servicemenu.AppendMenu(-1,u"台站属性查询",submenu)
        self.servicemenu.AppendSeparator()
        submenu=wx.Menu()
        i1=submenu.Append(-1,u"在网终端属性")
        i2=submenu.Append(-1,u"所有注册终端属性")
        self.Bind(wx.EVT_MENU,self.OnQueryPortPro,i1)
        self.Bind(wx.EVT_MENU,self.OnQueryAllPortPro,i2)
        self.servicemenu.AppendMenu(-1,u"终端属性查询",submenu)
        self.servicemenu.AppendSeparator()
        i=self.servicemenu.Append(-1,u"国家无线电频率规划查询")
        self.Bind(wx.EVT_MENU,self.OnQueryFreqPlan,i)
        submenu=wx.Menu()
        i1=submenu.Append(-1,u"更改扫频参数")
        i2=submenu.Append(-1,u"更改定频参数")
        i3=submenu.Append(-1,u"启动压制发射")
        self.Bind(wx.EVT_MENU,self.OnChangeAnotherSweep,i1)
        self.Bind(wx.EVT_MENU,self.OnChangeAnotherIQPara,i2)
        self.Bind(wx.EVT_MENU,self.OnChangeAnotherPress,i3)
        self.servicemenu.AppendSeparator()
        self.servicemenu.AppendMenu(-1,u"高级用户更改另一终端请求",submenu)
        self.menubar.Append(self.servicemenu,u"&服务请求")
        
        self.IQmenu=wx.Menu()
        i=self.IQmenu.Append(-1,u"历史功率谱")
        self.Bind(wx.EVT_MENU,self.OnSetSpecTime,i)
        self.IQmenu.AppendSeparator()
        submenu=wx.Menu()
        i1=submenu.Append(-1,u"解调时间段")
        i2=submenu.Append(-1,u"窗口显示类型")
        self.Bind(wx.EVT_MENU,self.OnSetDemodTime,i1)
        self.Bind(wx.EVT_MENU,self.OnDemodDisplay,i2)
        self.IQmenu.AppendMenu(-1,u"解调历史IQ数据",submenu)
        self.menubar.Append(self.IQmenu,u"&文件请求")


        self.windowmenu=wx.Menu()
        i=self.windowmenu.Append(-1,u"显示设置")
        self.Bind(wx.EVT_MENU,self.OnDisplayWindow,i)
        self.menubar.Append(self.windowmenu,u"&显示窗口")


        self.SetMenuBar(self.menubar)
    
    ####入网相关######
    def OnConnect(self,event):
        self.serverCom.ConnectToServer()
        receiveServerDataThread=ReceiveServerData(self.SpecFrame,self.serverCom.sock)
        receiveServerDataThread.start()
        print 'start receiving data thread'
    ###硬件相关################
    
    def OnStartTransfer(self,event):
        dev = usb.core.find(idVendor=0x04b4, idProduct=0x00f1)
        cfg=dev[0]
        intf=cfg[(0,0)]
        #0x01
        self.outPoint=intf[0]
        #0x81 fft
        self.inPoint1=intf[1]
        #0x82 iq
        self.inPoint2=intf[3]
        #0x83 query receive and abFreq
        self.inPoint3=intf[5]
        transfer=TransferSet()
        transfer.CommonHeader=FrameHeader(0x55,0x0A,0x0F,0)
        transfer.CommonTail=self.tail
        self.outPoint.write(bytearray(transfer))
        
        print 'usb transfer open'
        
    def OnCloseTransfer(self,event):
        transfer=TransferSet()
        transfer.CommonHeader=FrameHeader(0x55,0x0B,0x0F,0)
        transfer.CommonTail=self.tail
        self.outPoint.write(bytearray(transfer))
        
        print 'usb transfer close'

    ###设置相关指令####
    def OnSetAccessWay(self,event):
        dlg=AllDialog.AccessSetDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            if(dlg.CtrlUSB.GetValue()): pass
        
            header=FrameHeader(0x55,0x09,0x0F,0x00)
            usbWay=AccessWaySet(header,0x03,0,0,0,0,0,0,0,0,0,self.tai)
            self.outPoint.write(bytearray(usbWay))
        dlg.Destroy()
      
    def OnSetRecvGain(self,event):
        dlg=AllDialog.GainSetDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            Gain=int(dlg.sliderGain.GetValue())
            header=FrameHeader(0x55,0x04,0x0F,0x00)
            gainSet=RecvGainSet()
            gainSet.CommonHeader=header
            gainSet.RecvGain=Gain+3
            gainSet.CommonTail=self.tail
            self.outPoint.write(bytearray(gainSet))
        dlg.Destroy()
        
            
    def OnSetSendWeak(self,event):
        dlg=AllDialog.WeakSetDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            Weak=int(dlg.sliderWeak.GetValue())
            header=FrameHeader(0x55,0x05,0x0F,0x00)
            SendWeak=SendWeakSet()
            SendWeak.CommonHeader=header
            SendWeak.RecvGain=Weak
            SendWeak.CommonTail=self.tail
            self.outPoint.write(bytearray(SendWeak))
        dlg.Destroy()
        
    def OnSetThres(self,event):
        dlg=AllDialog.ThresSetDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            thres=int(dlg.selected.GetValue())
            thresMode=0x01
            thresSet=ThresSet()
            if(thres<=40 and thres>=3):
                thres= self.dictThres[thres]
                thresMode=0x00
                thresSet.AdaptThres=thres
            else:    
                thresSet.HighFixedThres=thres& 0xF0;
                thresSet.LowFixedThres=thres& 0x0F;
                
            header=FrameHeader(0x55,0x06,0x0F,0x00)
            thresSet.CommonHeader=header 
            thresSet.ThresMode=thresMode            
            thresSet.CommonTail=self.tail
            self.outPoint.write(bytearray(thresSet))
        dlg.Destroy()
    
    def OnSetPressPara(self,event):
        dlg=AllDialog.PressParaSetDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            freqNum=dlg.radioFreq.GetSelection()
            if(dlg.radioBox.GetSelection()==0):
                oneFreqT1=int(dlg.textPressTime1.GetValue())
                oneFreqT2=int(dlg.textPressWait.GetValue())
                if(freqNum==0):
                    pressMode=0x02
                else:
                    pressMode=0x04
            elif(dlg.radioBox.GetSelection()==1):
                twoFreqT1=int(dlg.textPressTotal.GetValue())
                twoFreqT2=int(dlg.textPressWait.GetValue())
                twoFreqT3=int(dlg.textPressTime1.GetValue())
                twoFreqT4=int(dlg.textPressTime2.GetValue())
                
                if(freqNum==0):
                    pressMode=0x01
                else:
                    pressMode=0x03
            else:
                    pressMode=0x05
            
            PressSignal=dlg.combox.GetSelection()    
            pressSet=PressParaSet()   
            header=FrameHeader(0x55,0x08,0x0F,0)
            pressSet.PressMode=pressMode
            pressSet.CommonHeader=header
            pressSet.PressSignal=PressSignal+1
            if(PressSignal==2 or PressSignal==3):
                pressSet.PressSignalBandWidth=PressSignal
            else:
                pressSet.PressSignalBandWidth=PressSignal+1
            if(freqNum==0):
                pressSet.HighT1=oneFreqT1&0xF0
                pressSet.LowT1=oneFreqT1&0x0F
                pressSet.HighT2=oneFreqT2&0xF0
                pressSet.LowT2= oneFreqT2&0x0F    
            else:
                pressSet.HighT1=twoFreqT1&0xF0
                pressSet.LowT1=twoFreqT1&0x0F
                pressSet.HighT2=twoFreqT2&0xF0
                pressSet.LowT2= twoFreqT2&0x0F
                pressSet.HighT3=twoFreqT3&0xF0
                pressSet.LowT3=twoFreqT3&0x0F
                pressSet.HighT4=twoFreqT4&0xF0
                pressSet.LowT4=twoFreqT4&0x0F 
            pressSet.CommonTail=self.tail
            self.outPoint.write(bytearray(pressSet))
        dlg.Destroy()
            
        
    def OnSetPressOne(self,event):
        dlg=AllDialog.PressOneSetDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            PressFreq=float(dlg.textPressFreq.GetValue())
            array=self.FreqToByte(PressFreq)
            pressFreqSet=PressFreqSet()
            pressFreqSet.CommonHeader=FrameHeader(0x55,0x03,0x0F,0)
            pressFreqSet.CommonTail=self.tail
            pressFreqSet.PressNum=1
            pressFreqSet.FreqArray[0]=CentreFreq(array[0],array[1],array[2],array[3])    
            self.outPoint.write(bytearray(pressFreqSet))
        dlg.Destroy()
        
    def FreqToByte(self,freq):
        freqInt=int(freq)
        freqFloat=freq-freqInt
        freqF=int(freqFloat*2**10)
        highFreqInt=freqInt>>6
        lowFreqInt=freqInt&0x003F
        highFreqFrac=freqF>>8
        lowFreqFrac=freqF&0x0FF
        return (highFreqInt,lowFreqInt,highFreqFrac,lowFreqFrac)
        

    def OnSetPressTwo(self,event):
        
        dlg=AllDialog.PressTwoSetDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            PressFreq1=float(dlg.textPressFreq1.GetValue())
            PressFreq2=float(dlg.textPressFreq2.GetValue())
            array1=self.FreqToByte(PressFreq1)
            array2=self.FreqToByte(PressFreq2)
            pressFreqSet=PressFreqSet()
            pressFreqSet.CommonHeader=FrameHeader(0x55,0x03,0x0F,0)
            pressFreqSet.CommonTail=self.tail
            pressFreqSet.PressNum=2
            pressFreqSet.FreqArray[0]=CentreFreq(array1[0],array1[1],array1[2],array1[3])    
            pressFreqSet.FreqArray[1]=CentreFreq(array2[0],array2[1],array2[2],array2[3])    
            self.outPoint.write(bytearray(pressFreqSet))
        dlg.Destroy()
            

    def OnSetFullSweep(self,event):
        dlg=AllDialog.FullSweepSetDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            sweepRangeSet=SweepRangeSet()
            sweepRangeSet.CommonHeader=FrameHeader(0x55,0x01,0x0F,0)
            sweepRangeSet.CommonTail=self.tail
            sweepRangeSet.SweepRecvMode=1
            if(dlg.radioM.GetValue()):
                sweepRangeSet.FileUploadMode=3
                sweepRangeSet.ExtractM=int(dlg.textM.GetValue())
            elif(dlg.radioAuto.GetValue()):
                sweepRangeSet.FileUploadMode=2
                sweepRangeSet.ChangeThres=int(dlg.ChangeThres.GetValue())
            else:
                sweepRangeSet.FileUploadMode=1
            self.outPoint.write(bytearray(sweepRangeSet))
        dlg.Destroy()
           

    def OnSetSpecialSweep(self,event):
        dlg=AllDialog.SpecialSweepSetDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            sweepRangeSet=SweepRangeSet()
            sweepRangeSet.CommonHeader=FrameHeader(0x55,0x01,0x0F,0)
            sweepRangeSet.CommonTail=self.tail
            sweepRangeSet.SweepRecvMode=2
            if(dlg.radioM.GetValue()):
                sweepRangeSet.FileUploadMode=3
                sweepRangeSet.ExtractM=int(dlg.textM.GetValue())
            elif(dlg.radioAuto.GetValue()):
                sweepRangeSet.FileUploadMode=2
                sweepRangeSet.ChangeThres=int(dlg.ChangeThres.GetValue())
            else:
                sweepRangeSet.FileUploadMode=1
            freqStart=int(dlg.FreqStart.GetValue())
            freqEnd=int(dlg.FreqEnd.GetValue())
            array=self.SweepSection(freqStart, freqEnd)
            sweepRangeSet=self.FillSweepRange(sweepRangeSet, array)
            self.outPoint.write(bytearray(sweepRangeSet))
            
        dlg.Destroy()
    def FillSweepRange(self,sweepRangeSet,array):
        sweepRangeSet.StartSectionNo=array[0]
        sweepRangeSet.EndSectionNo=array[1]
        sweepRangeSet.HighStartFreq=array[2]
        sweepRangeSet.LowStartFreq=array[3]
        sweepRangeSet.HighEndFreq=array[4]
        sweepRangeSet.LowEndFreq=array[5]
        return sweepRangeSet
    def SweepSection(self,freqStart,freqEnd):
        startK=(freqStart-70)/25
        endK=(freqEnd-70)/25
        startNum=int(float(freqStart-(startK*25+70))*1024/25)
        endNum=int(float(freqEnd-(endK*25+70))*1024/25)
        startKth=startK+1
        endKth=endK+1
        startf_h=startNum>>8
        startf_l=startNum&0x0FF
        endf_h=endNum>>8
        endf_l=endNum&0x0FF
        return (startKth,endKth,startf_h,startf_l,endf_h,endf_l)
        
        
    def OnSetMutiSweep(self,event):
        dlg=AllDialog.MutiSweepSetDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            sweepRangeSet=SweepRangeSet()
            sweepRangeSet.CommonHeader=FrameHeader(0x55,0x01,0x0F,0)
            sweepRangeSet.CommonTail=self.tail
            sweepRangeSet.SweepRecvMode=3
            if(dlg.radioM.GetValue()):
                sweepRangeSet.FileUploadMode=3
                sweepRangeSet.ExtractM=int(dlg.textM.GetValue())
            elif(dlg.radioAuto.GetValue()):
                sweepRangeSet.FileUploadMode=2
                sweepRangeSet.ChangeThres=int(dlg.ChangeThres.GetValue())
            else:
                sweepRangeSet.FileUploadMode=1
            
            freqStart=int(dlg.FreqStart1.GetValue())
            freqEnd=int(dlg.FreqEnd1.GetValue())
            array=self.SweepSection(freqStart, freqEnd)
            sweepRangeSet= self.FillSweepRange(sweepRangeSet, array)
            self.outPoint.write(bytearray(sweepRangeSet))
            if(dlg.FreqStart2.GetValue()):
                freqStart=int(dlg.FreqStart2.GetValue())
                freqEnd=int(dlg.FreqEnd2.GetValue())
                array=self.SweepSection(freqStart, freqEnd)
                sweepRangeSet= self.FillSweepRange(sweepRangeSet, array)
                self.outPoint.write(bytearray(sweepRangeSet))
            if(dlg.FreqStart3.GetValue()):
                freqStart=int(dlg.FreqStart3.GetValue())
                freqEnd=int(dlg.FreqEnd3.GetValue())
                array=self.SweepSection(freqStart, freqEnd)
                sweepRangeSet= self.FillSweepRange(sweepRangeSet, array)
                self.outPoint.write(bytearray(sweepRangeSet))
            if(dlg.FreqStart4.GetValue()):
                freqStart=int(dlg.FreqStart4.GetValue())
                freqEnd=int(dlg.FreqEnd4.GetValue())
                array=self.SweepSection(freqStart, freqEnd)
                sweepRangeSet= self.FillSweepRange(sweepRangeSet, array)
                self.outPoint.write(bytearray(sweepRangeSet))
            if(dlg.FreqStart5.GetValue()):
                freqStart=int(dlg.FreqStart5.GetValue())
                freqEnd=int(dlg.FreqEnd5.GetValue())
                array=self.SweepSection(freqStart, freqEnd)
                sweepRangeSet= self.FillSweepRange(sweepRangeSet, array)
                self.outPoint.write(bytearray(sweepRangeSet))                
        dlg.Destroy()        
            
                            
    def OnSetIQPara(self,event):
        dlg=AllDialog.IQParaSetDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            bandWidth=int(dlg.BandWidth.GetSelection())
            uploadNum=int(dlg.textUploadNum.GetValue())
            delayTime=int(dlg.textDelay.GetValue())
            
            curTime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
            iqPara=IQParaSet()
            iqPara.CommonHeader=FrameHeader(0x55,0x07,0x0F,0)
            iqPara.CommonTail=self.tail
            iqPara.BandWidth=bandWidth+1
            iqPara.UploadNum=uploadNum
            Year=int(curTime[0:4])
            Month=int(curTime[4:6])
            Day=int(curTime[6:8])
            Hour=int(curTime[8:10])
            Min=int(curTime[10:12])
            Second=int(curTime[12:14])+delayTime
            iqPara.DataDate.HighYear=Year>>4
            iqPara.DataDate.LowYear=Year&0x00F
            iqPara.Month=Month
            iqPara.Day=Day
            iqPara.HighHour=Hour>>2
            iqPara.LowHour=Hour&0x03
            iqPara.Minute=Min
            iqPara.Second=Second
            self.outPoint.write(bytearray(iqPara))
        dlg.Destroy()
    def OnSetIQFreq(self,event):
        dlg=AllDialog.IQFreqSetDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            iqFreq=IQFreqSet()
            iqFreq.CommonHeader=FrameHeader(0x55,0x02,0x0F,0)
            iqFreq.CommonTail=self.tail
            listFreq=[]
            Freq1=int(dlg.textFreq1.GetValue())
            Freq2=dlg.textFreq2.GetValue()
            Freq3=dlg.textFreq3.GetValue()
            listFreq.append(Freq1)
            if(Freq2):
                listFreq.append(Freq2)
            if(Freq3):
                listFreq.append(Freq3)
            for i in xrange(len(listFreq)):
                array=self.FreqToByte(listFreq[i])
                iqFreq.FreqArray[i]=CentreFreq(array[0],array[1],array[2],array[3])
            iqFreq.FreqNum=len(listFreq)
            self.outPoint.write(bytearray(iqFreq))        
        dlg.Destroy()
        

    ###查询相关指令#####
    
    def QuerySend(self,funcPara):
        query=Query()
        query.CommonHeader=FrameHeader(0x55,funcPara,0x0F,0)
        query.CommonTail=self.tail
        self.outPoint.write(bytearray(query))   
        
    def OnQuerySweepRange(self,event):
        self.QuerySend(0x11)
    
    def OnQueryIQFreq(self,event):
        self.QuerySend(0x12)
    def OnQueryIQPara(self,event):
        self.QuerySend(0x17)
    def OnQueryPressFreq(self,event):
        self.QuerySend(0x13)
    def OnQueryPressPara(self,event):
        self.QuerySend(0x18)
    def OnQueryRecvGain(self,event):
        self.QuerySend(0x14)
    def OnQuerySendWeak(self,event):
        self.QuerySend(0x15)
    def OnQueryThres(self,event):
        self.QuerySend(0x16)
    def OnQueryAccessWay(self,event):
        self.QuerySend(0x19)
    def OnQueryTransferOn(self):
        self.QuerySend(0x1A)
    def OnQueryTransferOff(self):
        self.QuerySend(0x1B)
        
    ####文件上传#####
    
    def OnLocalSaveSpec(self,event):
        pass
    def OnUploadSpec(self,event):
        pass

    def OnLocalSaveWave(self,event):
        pass
    def OnUploadWave(self,event):
        pass
    
    ########服务请求###############
    
    ###电磁分布AND异常频点定位######

    def OnReqElecTrend(self,event):
        dlg=AllDialog.ReqElecTrendDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            pass
        dlg.Destroy()
    def OnReqElecPath(self,event):
        dlg=AllDialog.ReqElecPathDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            pass
        dlg.Destroy()
    def OnReqAbFreq(self,event):
        dlg=AllDialog.ReqAbFreqDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            pass
        dlg.Destroy()
        

    #########台站相关属性#############

    def OnQueryStationPro(self,event):
        dlg=AllDialog.QueryStationProDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            pass
        dlg.Destroy()

    def OnQueryCurStationPro(self,event):
        dlg=AllDialog.QueryCurStationProDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            pass
        dlg.Destroy()

    def OnQueryAllStationPro(self,event):
        dlg=AllDialog.QueryAllStationProDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            pass
        dlg.Destroy()
    #############在网和全部终端属性以及无线电频率规划#########

    def OnQueryPortPro(self,event):
        pass
    def OnQueryAllPortPro(self,event):
        pass

    def OnQueryFreqPlan(self,event):
        dlg=AllDialog.QueryFreqPlanDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            freqStart=int(dlg.FreqStart.GetValue())
            freqEnd=int(dlg.FreqEnd.GetValue())
        dlg.Destroy()
        highFreqStart=freqStart/65536
        midFreqStart=(freqStart-highFreqStart*65536)/256
        lowFreqStart=freqStart-highFreqStart*65536-midFreqStart*256
        
        highFreqEnd=freqEnd/65536
        midFreqEnd=(freqEnd-highFreqEnd*65536)/256
        lowFreqEnd=freqEnd-highFreqEnd*65536-midFreqEnd*256
        header=FrameHeader(0x55,0xA7,0x0F,0)
        
        structObj=QueryFreqPlan(header,highFreqStart,midFreqStart,lowFreqStart,highFreqEnd,midFreqEnd,lowFreqEnd,self.tail)
        #frameLen=sizeof(structObj)
        frameLen=11
        self.serverCom.SendQueryData(frameLen,structObj)

    ###########高级用户更改另一终端请求########################
    def OnChangeAnotherSweep(self,event):
        dlg=AllDialog.ChangeAnotherSweep()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            pass
        dlg.Destroy()
    def OnChangeAnotherIQPara(self,event):
        pass
    def OnChangeAnotherPress(self,event):
        pass

    #############指定终端历史功率谱文件请求#####################
    def OnSetSpecTime(self,event):
        dlg=AllDialog.SetSpecTimeDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            pass
        dlg.Destroy()

    #############指定终端历史IQ数据请求######################
    def OnSetDemodTime(self,event):
        dlg=AllDialog.SetDemodTimeDialog()
        result=dlg.ShowModal()  
        if(result==wx.ID_OK):
            pass
        dlg.Destroy()


    ############窗口显示（解调的和正常应该显示的）#########
    
    def OnDemodDisplay(self,event):
        dlg=AllDialog.IQDisplaySetDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            if(dlg.CtrlDemodWave.GetValue()): self.OnNewChild("Demod Wave")
            elif(dlg.CtrlDemodConstel.GetValue()):self.OnNewChild("Constel")
            elif(dlg.CtrlDemodEye.GetValue()): self.OnNewChild("Eye")
            elif(dlg.CtrlDemodCCDF.GetValue()):self.OnNewChild("CCDF")
            else:
                pass
        dlg.Destroy()

    def OnDisplayWindow(self,event):
        dlg=AllDialog.DisplaySetDialog()
        result=dlg.ShowModal()
        if(result==wx.ID_OK):
            if(dlg.CtrlSpec.GetValue()): self.OnNewChild("Spectrum")
            elif(dlg.CtrlWater.GetValue()):self.OnNewChild("WaterFall")
            elif(dlg.CtrlWave.GetValue()):self.OnNewChild("Wave")
            else:
                pass
        dlg.Destroy()
      
    
    def OnNewChild(self,string):
        
        global waveShow
        global specShow
        global waterShow
        global demodWaveShow
        global demodConstelShow
        global demodCCDFShow
        global demodEyeShow
        
        if(string=="Wave"): 
            if(not waveShow):
                self.WaveFrame=WaveIQ(self,"IQ Wave")
                self.WaveFrame.Show()
                self.Bind(wx.EVT_WINDOW_DESTROY,self.OnCloseWaveFrame,self.WaveFrame)
                self.Tile(wx.HORIZONTAL)
                waveShow=True
                    
        elif(string=="Spectrum"):
            if(not specShow):
                self.SpecFrame=Spec(self)
                self.SpecFrame.Show()
                self.Bind(wx.EVT_WINDOW_DESTROY,self.OnCloseSpecFrame,self.SpecFrame)
                self.Tile(wx.HORIZONTAL)
                specShow=True
                    
        elif(string=="WaterFall"):
            if(not waterShow):
                self.WaterFrame=Water(self)
                self.WaterFrame.Show()
                self.Bind(wx.EVT_WINDOW_DESTROY,self.OnCloseWaterFrame,self.WaterFrame)
                self.Tile(wx.HORIZONTAL)
                waterShow=True
        elif(string=="Demod Wave"):
            if(not demodWaveShow):
                self.DemodWaveFrame=WaveIQ(self,"Demod Wave")
                self.DemodWaveFrame.Show()
                self.Bind(wx.EVT_WINDOW_DESTROY,self.OnCloseDemodWaveFrame,self.DemodWaveFrame)
                self.Tile(wx.HORIZONTAL)
                demodWaveShow=True
        elif(string=="Constel"):
            if(not demodConstelShow):
                self.DemodConstelFrame=Constel(self)
                self.DemodConstelFrame.Show()
                self.Bind(wx.EVT_WINDOW_DESTROY,self.OnCloseDemodConstelFrame,self.DemodConstelFrame)
                self.Tile(wx.HORIZONTAL)
                demodConstelShow=True

        elif(string=="Eye"):
            if(not demodEyeShow):
                self.DemodEyeFrame=Eye(self)
                self.DemodEyeFrame.Show()
                self.Bind(wx.EVT_WINDOW_DESTROY,self.OnCloseDemodEyeFrame,self.DemodEyeFrame)
                self.Tile(wx.HORIZONTAL)
                demodEyeShow=True

        elif(string=="CCDF"):
            if(not demodCCDFShow):
                self.DemodCCDFFrame=CCDF(self)
                self.DemodCCDFFrame.Show()
                self.Bind(wx.EVT_WINDOW_DESTROY,self.OnCloseDemodCCDFFrame,self.DemodCCDFFrame)
                self.Tile(wx.HORIZONTAL)
                demodCCDFShow=True

        

            
if __name__=="__main__":
    app=wx.App()
    main_frame=MainWindow()
    main_frame.Show()
    app.MainLoop()

os._exit(1)
           
