# -*- coding: utf-8 -*-
import wx
class DisplaySetDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"显示窗口选择",size=(200,250))

        self.CtrlWave=wx.CheckBox(self,-1,u"波形",(35,30),(100,20))
        self.CtrlSpec=wx.CheckBox(self,-1,u"功率谱",(35,60),(100,20))
        self.CtrlWater=wx.CheckBox(self,-1,u"瀑布图",(35,90),(100,20))
        wx.Button(self,wx.ID_OK,"OK",(35,150),(60,20))
        wx.Button(self,wx.ID_CANCEL,"CANCEL",(120,150),(60,20))
class IQDisplaySetDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"解调窗口选择",size=(200,250))
        self.CtrlDemodWave=wx.CheckBox(self,-1,u"解调波形",(35,30),(100,20))
        self.CtrlDemodConstel=wx.CheckBox(self,-1,u"星座图",(35,60),(100,20))
        self.CtrlDemodEye=wx.CheckBox(self,-1,u"眼图",(35,90),(100,20))
        self.CtrlDemodCCDF=wx.CheckBox(self,-1,u"CCDF",(35,120),(100,20))
        wx.Button(self,wx.ID_OK,"OK",(35,170),(60,20))
        wx.Button(self,wx.ID_CANCEL,"CANCEL",(120,170),(60,20))
class AccessSetDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"接入方式选择",size=(200,250))
        self.CtrlUSB=wx.CheckBox(self,-1,"USB",(35,30),(100,20))
        self.CtrWifi=wx.CheckBox(self,-1,"WIFI",(35,60),(100,20))
        self.CtrlBT=wx.CheckBox(self,-1,"BLUETOOTH",(35,90),(100,20))
        wx.Button(self,wx.ID_OK,"OK",(35,150),(60,20))
        wx.Button(self,wx.ID_CANCEL,"CANCEL",(120,150),(60,20))
class GainSetDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"接收增益设置",size=(300,200))
        wx.StaticBox(self, -1, u'接受增益(dB)', (10, 20), size=(240, 60))
        self.sliderGain = wx.Slider(self,-1, 7,-1, 73, (20, 40), (220, -1),wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
        wx.Button(self,wx.ID_OK,"OK",(20,100),(60,20))
        wx.Button(self,wx.ID_CANCEL,"CANCEL",(100,100),(60,20))
class WeakSetDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"发射衰减设置",size=(300,200))
        wx.StaticBox(self, -1, u'发射衰减(dB)', (10, 20), size=(240, 60))
        self.sliderWeak = wx.Slider(self,-1, 7,-1, 73, (20, 40), (220, -1),wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
        wx.Button(self,wx.ID_OK,"OK",(20,100),(60,20))
        wx.Button(self,wx.ID_CANCEL,"CANCEL",(100,100),(60,20))
class ThresSetDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"检测门限设置(dB)",size=(300,200))

        self.radio1 = wx.RadioButton(self, -1, u"自适应", pos=(20,40), style=wx.RB_GROUP)
        self.radio2 = wx.RadioButton(self, -1, u"固定", pos=(20,80))
        sampleList = ['3','10','20','25','30','40']
        self.combox = wx.ComboBox(self, -1,value='20',pos=(80,40),size=(100,30),choices=sampleList)
        self.text = wx.TextCtrl(self, -1, "", pos=(80, 80),size=(100,25))
        wx.Button(self,wx.ID_OK,"OK",(20,130),(60,20))
        wx.Button(self,wx.ID_CANCEL,"CANCEL",(100,130),(60,20))
        
        self.text.Enable(False)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, self.radio1)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, self.radio2)
        self.selected=self.combox
    def OnRadio(self, event):
        if self.radio1.GetValue():
            self.combox.Enable(True)
            self.text.Enable(False)
            self.selected=self.combox

        else:
            if self.radio2.GetValue():
                self.text.Enable(True)
                self.combox.Enable(False)
                self.selected=self.text

class PressParaSetDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"压制参数设置",size=(400,350))
        sampleList=[u"手动",u"自动",u"不压制"]
        self.radioBox= wx.RadioBox(self, -1,label=u"压制模式",pos=(20,15),size=(100,30),choices=sampleList)
        self.radioBox.SetSelection(2)
        
        sampleList=[u"单频点",u"双频点"]
        self.radioFreq= wx.RadioBox(self, -1,label=u"压制个数",pos=(20,70),size=(100,30),choices=sampleList)
        self.radioFreq.SetSelection(0)
        
        wx.StaticText(self,-1,u"压制信号类型：",pos=(20,130))
        sampleList = [u'单频正弦',u'等幅多频',u'噪声调频',u'数字射频']
        self.combox = wx.ComboBox(self, -1,u'单频正弦',pos=(200,130),size=(80,30),choices=sampleList)
        
        wx.StaticText(self,-1,u"压制时间 (ms): ",(20,170),(100,25))
        wx.StaticText(self,-1,u"等待时间 (ms): ",(20,200),(100,25))
        wx.StaticText(self,-1,u"压制总时间 (ms)",(20,230),(100,25))
        
        self.textPressTime1=wx.TextCtrl(self,-1,"",(200,170),(80,25))
        self.textPressTime2=wx.TextCtrl(self, -1,"",(300,170),(80,25))

        self.textPressWait=wx.TextCtrl(self,-1,"",(200,200),(80,25))
        self.textPressTotal=wx.TextCtrl(self, -1,"",(200,230),(80,25))
        
        wx.Button(self,wx.ID_OK,"OK",size=(60,20),pos=(20,280))
        wx.Button(self,wx.ID_CANCEL,"CANCEL",(100,280),(60,20))
        self.Bind(wx.EVT_RADIOBOX,self.OnRadio,self.radioFreq)
        self.textPressTime2.Enable(False)
        self.textPressTotal.Enable(False)
            
    def OnRadio(self,event):
        if(self.radioFreq.GetSelection()==0):
            self.textPressTime2.Enable(False)
            self.textPressTotal.Enable(False)
        else:
            self.textPressTime2.Enable(True)
            self.textPressTotal.Enable(True)    
        
class PressOneSetDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"单频点压制",size=(300,200))

        wx.StaticText(self,-1,u"频点频率 (MHz): ",(35,30),(100,20))
        
        self.textPressFreq=wx.TextCtrl(self,-1,"",(150,30),(80,25))
        
        wx.Button(self,wx.ID_OK,"OK",(35,70),(60,20))
        wx.Button(self,wx.ID_CANCEL,"CANCEL",(120,70),(60,20))


class PressTwoSetDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"双频点压制",size=(300,200))

        wx.StaticText(self,-1,u"频点频率 1(MHz): ",(35,40),(100,25))
        wx.StaticText(self,-1,u"频点频率 2(MHz): ",(35,70),(100,25))
        self.textPressFreq1=wx.TextCtrl(self,-1,"",(150,40),(80,25))
        self.textPressFreq2=wx.TextCtrl(self,-1,"",(150,70),(80,25))
        wx.Button(self,wx.ID_OK,"OK",(35,120),(60,20))
        wx.Button(self,wx.ID_CANCEL,"CANCEL",(120,120),(60,20))
        
class IQFreqSetDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"定频频点及频率设置",size=(340,300))
        wx.StaticText(self,-1,u"频率个数",pos=(20,20))
        wx.StaticLine(self,-1,pos=(20,40),size=(220,2),style=wx.LI_HORIZONTAL)

        sampleList=[u"1个",u"2个",u"3个"]
        self.radioBox= wx.RadioBox(self, -1,pos=(20,50),size=(100,30),choices=sampleList)
        self.radioBox.SetSelection(0)

        wx.StaticText(self,-1,u"频率值 (MHz)",pos=(20,120))
        wx.StaticLine(self,-1,pos=(20,140),size=(220,2),style=wx.LI_HORIZONTAL)

        self.textFreq1=wx.TextCtrl(self,-1,"",(20,160),(60,25))
        self.textFreq2=wx.TextCtrl(self,-1,"",(100,160),(60,25))
        self.textFreq3=wx.TextCtrl(self, -1,"",(180,160),(60,25))
        wx.Button(self,wx.ID_OK,"OK",size=(60,20),pos=(20,230))
        wx.Button(self,wx.ID_CANCEL,"CANCEL",(100,230),(60,20))
        
        self.textFreq2.Enable(False)
        self.textFreq3.Enable(False)
        self.Bind(wx.EVT_RADIOBOX,self.OnRadio,self.radioBox)
    def OnRadio(self,event):
        switch=self.radioBox.GetSelection()
        if(switch==0):
            self.textFreq2.Enable(False)
            self.textFreq3.Enable(False)
        elif(switch==1):
            self.textFreq2.Enable(True)
            self.textFreq3.Enable(False)
        elif(switch==2):
            self.textFreq2.Enable(True)
            self.textFreq3.Enable(True)
        else:
            pass 
        
class IQParaSetDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"定频公共参数设置",size=(340,250))

        wx.StaticText(self,-1,u"带宽/数据率 (MHz/Msps):",pos=(30,30))
        sampleList = ['5/5','2.5/2.5','1/1','0.5/0/5','0.1/0/1']
        self.BandWidth = wx.ComboBox(self, -1,'5/5',pos=(200,30),size=(100,30),choices=sampleList)
        
        wx.StaticText(self,-1,u"上传数据块个数(1-256) : ",(30,70))
        self.textUploadNum=wx.TextCtrl(self,-1,"1",(200,70),(100,25))
        
        wx.StaticText(self,-1,u"延时时间(s): ",(30,110))
        self.textDelay=wx.TextCtrl(self,-1,"",(200,110),(100,25))
        wx.Button(self,wx.ID_OK,"OK",size=(60,20),pos=(20,170))
        wx.Button(self,wx.ID_CANCEL,"CANCEL",(100,170),(60,20))

class FullSweepSetDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"全频段扫频",size=(340,300))
        panel=wx.Panel(self,-1)
        self.radioM=wx.RadioButton(panel,-1,u"抽取定时自动传输")
        self.textM=wx.TextCtrl(panel,-1,"63",size=(60,25))
        self.ChangeThres=wx.ComboBox(panel,-1,"10",choices=["10","20"],size=(100,25))
        self.radioAuto=wx.RadioButton(panel,-1,u"不定时自动传输",size=(150,25))

        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel,-1,u"传输方式: ",size=(120,25)),0,wx.TOP|wx.LEFT,20)
        sizer.Add((10,10))
        sizer.Add(wx.RadioButton(panel,-1,u"手动传输",size=(120,25)),0,wx.LEFT,20)
        sizer.Add(self.radioAuto,0,wx.LEFT,20)

        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.radioM,0,wx.LEFT,20)
        hBox1.Add(wx.StaticText(panel,-1,u"抽取倍率M(1-63)"),0,wx.LEFT,20)
        hBox1.Add(self.textM,0,wx.LEFT,10)
        sizer.Add(hBox1)
        hBox2=wx.BoxSizer(wx.HORIZONTAL)          
        hBox2.Add(wx.StaticText(panel,-1,u"数据变化门限(dB)",size=(100,25)),0,wx.LEFT|wx.TOP,20)
        hBox2.Add(self.ChangeThres,0,wx.LEFT|wx.ALIGN_BOTTOM,10)
        sizer.Add(hBox2)
        sizer.Add((20,30))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.Button(panel,wx.ID_OK,"OK",size=(60,25)),0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_CANCEL,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio)
        self.textM.Enable(False)
    def OnRadio(self,event):
        if(self.radioM.GetValue()):
            self.textM.Enable(True)
        else:
            self.textM.Enable(False)
        if(self.radioAuto.GetValue()):
            self.ChangeThres.Enable(True)
        else:
            self.ChangeThres.Enable(False)


class SpecialSweepSetDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"指定频段扫频",size=(350,350))
        
        panel=wx.Panel(self,-1)
        self.radioM=wx.RadioButton(panel,-1,u"抽取定时自动传输")
        self.textM=wx.TextCtrl(panel,-1,"63",size=(60,25))
        self.ChangeThres=wx.ComboBox(panel,-1,"10",choices=["10","20"],size=(100,25))
        self.radioAuto=wx.RadioButton(panel,-1,u"不定时自动传输",size=(150,25))
        self.FreqStart=wx.TextCtrl(panel,-1,size=(60,25))
        self.FreqEnd=wx.TextCtrl(panel,-1,size=(60,25))

        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel,-1,u"传输方式: ",size=(120,25)),0,wx.TOP|wx.LEFT,20)
        sizer.Add((10,10))
        sizer.Add(wx.RadioButton(panel,-1,u"手动传输",size=(120,25)),0,wx.LEFT,20)
        sizer.Add(self.radioAuto,0,wx.LEFT,20)

        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.radioM,0,wx.LEFT,20)
        hBox1.Add(wx.StaticText(panel,-1,u"抽取倍率M(1-63)"),0,wx.LEFT,20)
        hBox1.Add(self.textM,0,wx.LEFT,10)
        sizer.Add(hBox1)
        hBox2=wx.BoxSizer(wx.HORIZONTAL)          
        hBox2.Add(wx.StaticText(panel,-1,u"数据变化门限(dB)",size=(100,25)),0,wx.LEFT|wx.TOP,20)
        hBox2.Add(self.ChangeThres,0,wx.LEFT|wx.ALIGN_BOTTOM,10)
        sizer.Add(hBox2)
        sizer.Add((20,10))
        sizer.Add(wx.StaticText(panel,-1,u"指定频率范围(70-5995)(MHz): ",size=(150,25)),0,wx.LEFT,20)
        sizer.Add((20,10))
        hBox3=wx.BoxSizer(wx.HORIZONTAL)          
        hBox3.Add(self.FreqStart,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        hBox3.Add(wx.StaticText(panel,-1,u"——"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,10)
        hBox3.Add(self.FreqEnd,0,wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
        sizer.Add((20,20))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.Button(panel,wx.ID_OK,"OK",size=(60,25)),0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_CANCEL,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio)
        self.textM.Enable(False)

    def OnRadio(self,event):
        if(self.radioM.GetValue()):
            self.textM.Enable(True)
        else:
            self.textM.Enable(False)
        if(self.radioAuto.GetValue()):
            self.ChangeThres.Enable(True)
        else:
            self.ChangeThres.Enable(False)



class MutiSweepSetDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"指定频段扫频",size=(400,500))
        
        panel=wx.Panel(self,-1)
        self.radioM=wx.RadioButton(panel,-1,u"抽取定时自动传输")
        self.textM=wx.TextCtrl(panel,-1,"63",size=(60,25))
        self.ChangeThres=wx.ComboBox(panel,-1,"10",choices=["10","20"],size=(100,25))
        self.radioAuto=wx.RadioButton(panel,-1,u"不定时自动传输",size=(150,25))
        self.Check1=wx.CheckBox(panel,-1)
        self.FreqStart1=wx.TextCtrl(panel,-1,size=(60,25))
        self.FreqEnd1=wx.TextCtrl(panel,-1,size=(60,25))
        self.Check2=wx.CheckBox(panel,-1)
        self.FreqStart2=wx.TextCtrl(panel,-1,size=(60,25))
        self.FreqEnd2=wx.TextCtrl(panel,-1,size=(60,25))
        self.Check3=wx.CheckBox(panel,-1)
        self.FreqStart3=wx.TextCtrl(panel,-1,size=(60,25))
        self.FreqEnd3=wx.TextCtrl(panel,-1,size=(60,25))
        self.Check4=wx.CheckBox(panel,-1)
        self.FreqStart4=wx.TextCtrl(panel,-1,size=(60,25))
        self.FreqEnd4=wx.TextCtrl(panel,-1,size=(60,25))
        self.Check5=wx.CheckBox(panel,-1)
        self.FreqStart5=wx.TextCtrl(panel,-1,size=(60,25))
        self.FreqEnd5=wx.TextCtrl(panel,-1,size=(60,25))

        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel,-1,u"传输方式: ",size=(120,25)),0,wx.TOP|wx.LEFT,20)
        sizer.Add((10,10))
        sizer.Add(wx.RadioButton(panel,-1,u"手动传输",size=(120,25)),0,wx.LEFT,20)
        sizer.Add(self.radioAuto,0,wx.LEFT,20)

        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.radioM,0,wx.LEFT,20)
        hBox1.Add(wx.StaticText(panel,-1,u"抽取倍率M(1-63)"),0,wx.LEFT,20)
        hBox1.Add(self.textM,0,wx.LEFT,10)
        sizer.Add(hBox1)
        hBox2=wx.BoxSizer(wx.HORIZONTAL)          
        hBox2.Add(wx.StaticText(panel,-1,u"数据变化门限(dB)",size=(100,25)),0,wx.LEFT|wx.TOP,20)
        hBox2.Add(self.ChangeThres,0,wx.LEFT|wx.ALIGN_BOTTOM,10)
        sizer.Add(hBox2)
        sizer.Add((20,10))
        sizer.Add(wx.StaticText(panel,-1,u"指定频率范围(70-5995)(MHz): ",size=(150,25)),0,wx.LEFT,20)
        sizer.Add((20,10))
        hBox3=wx.BoxSizer(wx.HORIZONTAL)   
        hBox3.Add(self.Check1,0,wx.LEFT|wx.ALIGN_BOTTOM,20)       
        hBox3.Add(self.FreqStart1,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        hBox3.Add(wx.StaticText(panel,-1,u"——"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,10)
        hBox3.Add(self.FreqEnd1,0,wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
        sizer.Add((20,10))
        hBox3=wx.BoxSizer(wx.HORIZONTAL)          
        hBox3.Add(self.Check2,0,wx.LEFT|wx.ALIGN_BOTTOM,20)      
        hBox3.Add(self.FreqStart2,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        hBox3.Add(wx.StaticText(panel,-1,u"——"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,10)
        hBox3.Add(self.FreqEnd2,0,wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
        sizer.Add((20,10))
        hBox3=wx.BoxSizer(wx.HORIZONTAL)      
        hBox3.Add(self.Check3,0,wx.LEFT|wx.ALIGN_BOTTOM,20)          
        hBox3.Add(self.FreqStart3,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        hBox3.Add(wx.StaticText(panel,-1,u"——"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,10)
        hBox3.Add(self.FreqEnd3,0,wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
        sizer.Add((20,10))
        hBox3=wx.BoxSizer(wx.HORIZONTAL)          
        hBox3.Add(self.Check4,0,wx.LEFT|wx.ALIGN_BOTTOM,20)      
        hBox3.Add(self.FreqStart4,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        hBox3.Add(wx.StaticText(panel,-1,u"——"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,10)
        hBox3.Add(self.FreqEnd4,0,wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
        sizer.Add((20,10))
        hBox3=wx.BoxSizer(wx.HORIZONTAL)          
        hBox3.Add(self.Check5,0,wx.LEFT|wx.ALIGN_BOTTOM,20)      
        hBox3.Add(self.FreqStart5,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        hBox3.Add(wx.StaticText(panel,-1,u"——"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,10)
        hBox3.Add(self.FreqEnd5,0,wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
        sizer.Add((20,20))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.Button(panel,wx.ID_OK,"OK",size=(60,25)),0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_CANCEL,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio)
        self.textM.Enable(False)
        self.Bind(wx.EVT_CHECKBOX,self.OnCheck)
        self.FreqStart2.Enable(False)
        self.FreqStart3.Enable(False)
        self.FreqStart4.Enable(False)
        self.FreqStart5.Enable(False)
        
        self.FreqEnd2.Enable(False)
        self.FreqEnd3.Enable(False)
        self.FreqEnd4.Enable(False)
        self.FreqEnd5.Enable(False)
        self.Check1.SetValue(True)

    def OnRadio(self,event):
        if(self.radioM.GetValue()):
            self.textM.Enable(True)
        else:
            self.textM.Enable(False)
        if(self.radioAuto.GetValue()):
            self.ChangeThres.Enable(True)
        else:
            self.ChangeThres.Enable(False)

    def OnCheck(self,event):
        if(self.Check2.GetValue()):
            self.FreqStart2.Enable(True)
            self.FreqEnd2.Enable(True)
        elif(self.Check3.GetValue()):
            self.FreqStart3.Enable(True)
            self.FreqEnd3.Enable(True)
        elif(self.Check4.GetValue()):
            self.FreqStart4.Enable(True)
            self.FreqEnd4.Enable(True)
        
        elif(self.Check5.GetValue()):
            self.FreqStart5.Enable(True)
            self.FreqEnd5.Enable(True)
  

######################################电磁态势的框#####################
class ReqElecTrendDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"电磁分布态势数据请求",size=(400,500))
        panel=wx.Panel(self,-1)
        List=[u"FM调频广播频段",u"GSM下行频段1",u"GSM下行频段2",u"IS95 CDMA 下行频段",u"TD 3G频段",u"TD LTE 频段1",
        u"TD LTE 频段2",u"WCDMA 下行频段",u"联通TDLTE 频段1",u"联通TDLTE 频段2",u"CDMA 2000 下行频段",u"电信TDLTE频段1",
        u"电信TDLTE频段2",u"LTE FDD 频段1",u"LTE FDD 频段2",u"ISM 433M频段",u"ISM 工业频段",u"ISM科研频段",u"ISM医疗频段"]

        self.FreqSection=wx.ComboBox(panel,-1,u"FM调频广播频段",choices=List)
        self.radioChoose=wx.RadioButton(panel,-1,u"选择频率")
        self.radioHand=wx.RadioButton(panel,-1,u"手动频率")
        self.CentreFreq=wx.TextCtrl(panel,-1,size=(80,25))
        self.BandWidth=wx.TextCtrl(panel,-1,size=(80,25))
        self.Radius=wx.TextCtrl(panel,-1,size=(80,25))
        self.FenBianLv=wx.TextCtrl(panel,-1,size=(80,25))
        self.RefreshIntv=wx.TextCtrl(panel,-1,size=(80,25))
        self.StartTimeYear=wx.ComboBox(panel,-1,"2015",choices=["2015","2016","2017","2018"])
        self.StartTimeMonth=wx.ComboBox(panel,-1,"12",choices=["1","2","3","4","5","6","7","8","9","10","11","12"])
        self.StartTimeDay=wx.TextCtrl(panel,-1,"1",size=(60,25))
        self.StartTimeHour=wx.TextCtrl(panel,-1,"0",size=(60,25))
        self.StartTimeMinute=wx.TextCtrl(panel,-1,"0",size=(60,25))

        self.EndTimeYear=wx.ComboBox(panel,-1,"2015",choices=["2015","2016","2017","2018"])
        self.EndTimeMonth=wx.ComboBox(panel,-1,"12",choices=["1","2","3","4","5","6","7","8","9","10","11","12"])
        self.EndTimeDay=wx.TextCtrl(panel,-1,"1",size=(60,25))
        self.EndTimeHour=wx.TextCtrl(panel,-1,"0",size=(60,25))
        self.EndTimeMinute=wx.TextCtrl(panel,-1,"0",size=(60,25))

        sizer=wx.BoxSizer(wx.VERTICAL)
        hBox=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add((30,30))
        hBox.Add(self.radioChoose,0,wx.LEFT,20)
        hBox.Add(self.radioHand,0,wx.LEFT,20)
        sizer.Add(hBox)
        sizer.Add(self.FreqSection,0,wx.LEFT|wx.TOP,20)

        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"中心频率(MHz)",size=(100,25)),0,wx.LEFT,20)
        hBox1.Add(self.CentreFreq,0,wx.LEFT,20)
        sizer.Add(hBox1)
        
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"带宽(MHz)",size=(100,25)),0,wx.LEFT,20)
        hBox1.Add(self.BandWidth,0,wx.LEFT,20)
        sizer.Add(hBox1)

        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"地理半径(km)",size=(100,25)),0,wx.LEFT,20)
        hBox1.Add(self.Radius,0,wx.LEFT,20)
        sizer.Add(hBox1)
        
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"经纬度分辨率",size=(100,25)),0,wx.LEFT,20)
        hBox1.Add(self.FenBianLv,0,wx.LEFT,20)
        sizer.Add(hBox1)

        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"动态刷新间隔(Min)",size=(130,25)),0,wx.LEFT,20)
        hBox1.Add(self.RefreshIntv,0,wx.LEFT,20)
        sizer.Add(hBox1)

        sizer.Add(wx.StaticText(panel,-1,u"起始时间(年-月-日-时-分)：",size=(160,25)),0,wx.LEFT,20)
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.StartTimeYear,0,wx.LEFT,20)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeMonth,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeDay,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeHour,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeMinute,0)
        sizer.Add(hBox1)

        sizer.Add(wx.StaticText(panel,-1,u"终止时间(年-月-日-时-分)：",size=(160,25)),0,wx.LEFT,20)
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.EndTimeYear,0,wx.LEFT,20)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeMonth,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeDay,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeHour,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeMinute,0)
        sizer.Add(hBox1)
        sizer.Add((30,30))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.Button(panel,wx.ID_OK,"OK",size=(60,25)),0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_CANCEL,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio)
        self.CentreFreq.Enable(False)
        self.BandWidth.Enable(False)
        self.radioChoose.SetValue(True)
    def OnRadio(self,event):
        if(self.radioChoose.GetValue()):
            self.FreqSection.Enable(True)
            self.BandWidth.Enable(False)
            self.CentreFreq.Enable(False)

        elif(self.radioHand.GetValue()):
            self.FreqSection.Enable(False)
            self.CentreFreq.Enable(True)
            self.BandWidth.Enable(True)

            
class ReqElecPathDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"电磁路径分布数据请求",size=(400,580))
        panel=wx.Panel(self,-1)
        self.radioBox1=wx.RadioBox(panel,-1,choices=[u"本地获取",u"中心站获取"],style=wx.RA_VERTICAL)
        self.radioBox2=wx.RadioBox(panel,-1,choices=[u"显示历史分布",u"显示实时分布"],style=wx.RA_VERTICAL)
        self.radioBox3=wx.RadioBox(panel,-1,choices=[u"选择频率",u"手动频率"])
        self.radioBox1.SetSelection(0)
        self.radioBox2.SetSelection(0)
        self.radioBox3.SetSelection(0)
   
        List=[u"FM调频广播频段",u"GSM下行频段1",u"GSM下行频段2",u"IS95 CDMA 下行频段",u"TD 3G频段",u"TD LTE 频段1",
        u"TD LTE 频段2",u"WCDMA 下行频段",u"联通TDLTE 频段1",u"联通TDLTE 频段2",u"CDMA 2000 下行频段",u"电信TDLTE频段1",
        u"电信TDLTE频段2",u"LTE FDD 频段1",u"LTE FDD 频段2",u"ISM 433M频段",u"ISM 工业频段",u"ISM科研频段",u"ISM医疗频段"]

        self.FreqSection=wx.ComboBox(panel,-1,u"FM调频广播频段",choices=List)
        self.CentreFreq=wx.TextCtrl(panel,-1,size=(80,25))
        self.BandWidth=wx.TextCtrl(panel,-1,size=(80,25))

        self.StartTimeYear=wx.ComboBox(panel,-1,"2015",choices=["2015","2016","2017","2018"])
        self.StartTimeMonth=wx.ComboBox(panel,-1,"12",choices=["1","2","3","4","5","6","7","8","9","10","11","12"])
        self.StartTimeDay=wx.TextCtrl(panel,-1,"1",size=(60,25))
        self.StartTimeHour=wx.TextCtrl(panel,-1,"0",size=(60,25))
        self.StartTimeMinute=wx.TextCtrl(panel,-1,"0",size=(60,25))

        self.EndTimeYear=wx.ComboBox(panel,-1,"2015",choices=["2015","2016","2017","2018"])
        self.EndTimeMonth=wx.ComboBox(panel,-1,"12",choices=["1","2","3","4","5","6","7","8","9","10","11","12"])
        self.EndTimeDay=wx.TextCtrl(panel,-1,"1",size=(60,25))
        self.EndTimeHour=wx.TextCtrl(panel,-1,"0",size=(60,25))
        self.EndTimeMinute=wx.TextCtrl(panel,-1,"0",size=(60,25))

        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add((15,15))
        sizer.Add(self.radioBox3,0,wx.LEFT,20)
        sizer.Add(self.FreqSection,0,wx.LEFT|wx.TOP,20)

        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"中心频率(MHz)",size=(100,25)),0,wx.LEFT,20)
        hBox1.Add(self.CentreFreq,0,wx.LEFT,20)
        sizer.Add(hBox1)
        
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"带宽(MHz)",size=(100,25)),0,wx.LEFT,20)
        hBox1.Add(self.BandWidth,0,wx.LEFT,20)
        sizer.Add(hBox1)

        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"分布数据来源：",size=(100,25)),0,wx.LEFT|wx.ALIGN_TOP,20)
        hBox1.Add(self.radioBox1,0,wx.LEFT|wx.ALIGN_TOP,20)
        sizer.Add(hBox1)
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"显示数据来源：",size=(100,25)),0,wx.LEFT|wx.ALIGN_TOP,20)
        hBox1.Add(self.radioBox2,0,wx.LEFT|wx.ALIGN_TOP,20)
        sizer.Add(hBox1)
        
        sizer.Add((10,10))
        sizer.Add(wx.StaticText(panel,-1,u"起始时间(年-月-日-时-分)：",size=(160,25)),0,wx.LEFT,20)
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.StartTimeYear,0,wx.LEFT,20)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeMonth,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeDay,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeHour,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeMinute,0)
        sizer.Add(hBox1)

        sizer.Add(wx.StaticText(panel,-1,u"终止时间(年-月-日-时-分)：",size=(160,25)),0,wx.LEFT,20)
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.EndTimeYear,0,wx.LEFT,20)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeMonth,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeDay,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeHour,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeMinute,0)
        sizer.Add(hBox1)
        sizer.Add((30,30))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.Button(panel,wx.ID_OK,"OK",size=(60,25)),0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_CANCEL,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        
        panel.SetSizer(sizer)
        self.Bind(wx.EVT_RADIOBOX, self.OnRadio,self.radioBox3)
        self.CentreFreq.Enable(False)
        self.BandWidth.Enable(False)

    def OnRadio(self,event):
        if(self.radioBox3.GetSelection()==0):
            self.FreqSection.Enable(True)
            self.BandWidth.Enable(False)
            self.CentreFreq.Enable(False)

        elif(self.radioBox3.GetSelection()==1):
            self.FreqSection.Enable(False)
            self.CentreFreq.Enable(True)
            self.BandWidth.Enable(True)


class ReqAbFreqDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"异常频点定位数据请求",size=(450,400))

        panel=wx.Panel(self,-1)
        self.CentreFreq=wx.TextCtrl(panel,-1,size=(80,25))
        self.UploadNum=wx.TextCtrl(panel,-1,"1",size=(80,25))
        self.radioBox=wx.RadioBox(panel,-1,choices=["POA","POA/TDOA"])
        self.radioBox.SetSelection(0)
        sampleList = ['5/5','2.5/2.5','1/1','0.5/0/5','0.1/0/1']
        self.BandWidth = wx.ComboBox(panel, -1,'5/5',size=(80,30),choices=sampleList)
      
        self.StartTimeYear=wx.ComboBox(panel,-1,"2015",choices=["2015","2016","2017","2018"])
        self.StartTimeMonth=wx.ComboBox(panel,-1,"12",choices=["1","2","3","4","5","6","7","8","9","10","11","12"])
        self.StartTimeDay=wx.TextCtrl(panel,-1,"1",size=(60,25))
        self.StartTimeHour=wx.TextCtrl(panel,-1,"0",size=(60,25))
        self.StartTimeMinute=wx.TextCtrl(panel,-1,"0",size=(60,25))
        self.StartTimeSecond=wx.TextCtrl(panel,-1,"0",size=(60,25)) 

        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add((15,15))
        sizer.Add(wx.StaticText(panel,-1,u"几何定位方法",size=(120,25)),0,wx.LEFT,20)
        sizer.Add(self.radioBox,0,wx.LEFT,20)

        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"中心频率(MHz)",size=(160,25)),0,wx.LEFT,20)
        hBox1.Add(self.CentreFreq,0,wx.LEFT,20)
        sizer.Add(hBox1)

        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"带宽/数据率 (MHz/Msps):",size=(160,25)),0,wx.LEFT,20)
        hBox1.Add(self.BandWidth,0,wx.LEFT,20)
        sizer.Add(hBox1)

        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"上传数据块个数(1-256):",size=(160,25)),0,wx.LEFT,20)
        hBox1.Add(self.UploadNum,0,wx.LEFT,20)
        sizer.Add(hBox1)

        sizer.Add((10,10))
        sizer.Add(wx.StaticText(panel,-1,u"采集起始时间(年-月-日-时-分-秒)："),0,wx.LEFT,20)
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.StartTimeYear,0,wx.LEFT,20)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeMonth,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeDay,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeHour,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeMinute,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeSecond,0)
        sizer.Add(hBox1)

        sizer.Add((30,30))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.Button(panel,wx.ID_OK,"OK",size=(60,25)),0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_CANCEL,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)
        

#################################台站属性框###########################
class QueryStationProDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"台站登记属性查询",size=(300,200))
        panel=wx.Panel(self,-1)
        sizer=wx.BoxSizer(wx.VERTICAL)
        self.FreqStart=wx.TextCtrl(panel,-1,size=(60,25))
        self.FreqEnd=wx.TextCtrl(panel,-1,size=(60,25))

        sizer.Add((20,15))
        sizer.Add(wx.StaticText(panel,-1,u"台站指定频率范围(MHz): ",size=(150,25)),0,wx.LEFT,20)
        sizer.Add((20,10))
        hBox3=wx.BoxSizer(wx.HORIZONTAL)          
        hBox3.Add(self.FreqStart,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        hBox3.Add(wx.StaticText(panel,-1,u"——"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,10)
        hBox3.Add(self.FreqEnd,0,wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
        sizer.Add((20,20))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.Button(panel,wx.ID_OK,"OK",size=(60,25)),0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_CANCEL,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)



class QueryCurStationProDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"登记台站当前属性查询",size=(300,200))
        panel=wx.Panel(self,-1)
        self.StationID=wx.TextCtrl(panel,-1,size=(80,25))
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add((20,30))
        hBox3=wx.BoxSizer(wx.HORIZONTAL)     
        hBox3.Add(wx.StaticText(panel,-1,u"指定台站识别码: ",size=(100,25)),0,wx.LEFT,20)
        hBox3.Add(self.StationID,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
        sizer.Add((20,20))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.Button(panel,wx.ID_OK,"OK",size=(60,25)),0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_CANCEL,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)



class QueryAllStationProDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"所有台站属性查询",size=(300,200))
        panel=wx.Panel(self,-1)
        self.StationID=wx.TextCtrl(panel,-1,size=(80,25))
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add((20,30))
        hBox3=wx.BoxSizer(wx.HORIZONTAL)     
        hBox3.Add(wx.StaticText(panel,-1,u"指定台站识别码: ",size=(100,25)),0,wx.LEFT,20)
        hBox3.Add(self.StationID,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
        sizer.Add((20,20))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.Button(panel,wx.ID_OK,"OK",size=(60,25)),0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_CANCEL,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)


##################国家无线电频率规划##############################3    

class QueryFreqPlanDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"国家无线电频率规划",size=(300,200))
        panel=wx.Panel(self,-1)
        sizer=wx.BoxSizer(wx.VERTICAL)
        self.FreqStart=wx.TextCtrl(panel,-1,size=(60,25))
        self.FreqEnd=wx.TextCtrl(panel,-1,size=(60,25))

        sizer.Add((20,15))
        sizer.Add(wx.StaticText(panel,-1,u"台站指定频率范围(MHz): ",size=(150,25)),0,wx.LEFT,20)
        sizer.Add((20,10))
        hBox3=wx.BoxSizer(wx.HORIZONTAL)          
        hBox3.Add(self.FreqStart,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        hBox3.Add(wx.StaticText(panel,-1,u"——"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,10)
        hBox3.Add(self.FreqEnd,0,wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
        sizer.Add((20,20))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.Button(panel,wx.ID_OK,"OK",size=(60,25)),0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_CANCEL,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)



#########################高级别用户改变另一终端###############################3
class ChangeAnotherSweep(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"改变另一终端扫频参数",size=(400,800))
        
        panel=wx.Panel(self,-1)
        sizer=wx.BoxSizer(wx.VERTICAL)
        sampleList = ['3','10','20','25','30','40']
        self.AdaptThres = wx.ComboBox(self, -1,value='20',size=(100,30),choices=sampleList)
        self.StaticThres = wx.TextCtrl(self, -1, "",size=(100,25))
        
        self.sliderGain = wx.Slider(self,-1, 7,-1, 73,(20,20),(220, -1),wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.textM=wx.TextCtrl(panel,-1,"63",size=(60,25))
        self.ChangeThres=wx.ComboBox(panel,-1,"10",choices=["10","20"],size=(100,25))

        self.RadioBoxTrans=wx.RadioBox(panel,-1,choices=[u"手动传输",u"不定时自动传输",u"抽取定时自动传输"])
        self.RadioBoxSweep=wx.RadioBox(panel,-1,choices=[u"全频带",u"指定频段",u"多频段"])
        self.RadioBoxThres=wx.RadioBox(panel,-1,choices=[u"自适应门限",u"固定门限"])
        self.RadioBoxSweep.SetSelection(0)
        self.RadioBoxTrans.SetSelection(0)
        self.RadioBoxThres.SetSelection(0)

        self.Check1=wx.CheckBox(panel,-1)
        self.FreqStart1=wx.TextCtrl(panel,-1,size=(60,25))
        self.FreqEnd1=wx.TextCtrl(panel,-1,size=(60,25))
        self.Check2=wx.CheckBox(panel,-1)
        self.FreqStart2=wx.TextCtrl(panel,-1,size=(60,25))
        self.FreqEnd2=wx.TextCtrl(panel,-1,size=(60,25))
        self.Check3=wx.CheckBox(panel,-1)
        self.FreqStart3=wx.TextCtrl(panel,-1,size=(60,25))
        self.FreqEnd3=wx.TextCtrl(panel,-1,size=(60,25))
        self.Check4=wx.CheckBox(panel,-1)
        self.FreqStart4=wx.TextCtrl(panel,-1,size=(60,25))
        self.FreqEnd4=wx.TextCtrl(panel,-1,size=(60,25))
        self.Check5=wx.CheckBox(panel,-1)
        self.FreqStart5=wx.TextCtrl(panel,-1,size=(60,25))
        self.FreqEnd5=wx.TextCtrl(panel,-1,size=(60,25))

        sizer.Add(wx.StaticText(panel,-1,u"扫频模式选择: ",size=(120,25)),0,wx.TOP|wx.LEFT,20)
        sizer.Add(self.RadioBoxSweep,0,wx.LEFT,20)
        sizer.Add((10,10))
        sizer.Add(wx.StaticText(panel,-1,u"传输方式选择: ",size=(120,25)),0,wx.LEFT,20)
        sizer.Add(self.RadioBoxTrans,0,wx.LEFT,20)
        sizer.Add((10,10))
        sizer.Add(wx.StaticText(panel,-1,u"检测门限类型: ",size=(120,25)),0,wx.LEFT,20)
        sizer.Add(self.RadioBoxThres,0,wx.LEFT,20)
        
        
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"抽取倍率M(1-63)"),0,wx.LEFT,20)
        hBox1.Add(self.textM,0,wx.LEFT,10)
        sizer.Add(hBox1)

        sizer.Add((10,10))
        hBox2=wx.BoxSizer(wx.HORIZONTAL)          
        hBox2.Add(wx.StaticText(panel,-1,u"数据变化门限(dB)",size=(100,25)),0,wx.LEFT,20)
        hBox2.Add(self.ChangeThres,0,wx.LEFT|wx.ALIGN_BOTTOM,10)
        sizer.Add(hBox2)

        sizer.Add((10,10))
        hBox2=wx.BoxSizer(wx.HORIZONTAL)          
        hBox2.Add(wx.StaticText(panel,-1,u"接收增益(dB)",size=(100,25)),0,wx.LEFT,20)
        hBox2.Add(self.sliderGain,0,wx.LEFT|wx.ALIGN_BOTTOM,10)
        sizer.Add(hBox2)
        
        sizer.Add((10,10))
        hBox2=wx.BoxSizer(wx.HORIZONTAL)          
        hBox2.Add(wx.StaticText(panel,-1,u"自适应门限(dB)",size=(100,25)),0,wx.LEFT,20)
        hBox2.Add(self.AdaptThres,0,wx.LEFT|wx.ALIGN_BOTTOM,10)
        sizer.Add(hBox2)

        sizer.Add((10,10))
        hBox2=wx.BoxSizer(wx.HORIZONTAL)          
        hBox2.Add(wx.StaticText(panel,-1,u"固定门限(dB)",size=(100,25)),0,wx.LEFT,20)
        hBox2.Add(self.StaticThres,0,wx.LEFT|wx.ALIGN_BOTTOM,10)
        sizer.Add(hBox2)

        sizer.Add((20,10))
        sizer.Add(wx.StaticText(panel,-1,u"指定频率范围(MHz): ",size=(150,25)),0,wx.LEFT,20)
        hBox3=wx.BoxSizer(wx.HORIZONTAL)   
        hBox3.Add(self.Check1,0,wx.LEFT|wx.ALIGN_BOTTOM,20)       
        hBox3.Add(self.FreqStart1,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        hBox3.Add(wx.StaticText(panel,-1,u"——"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,10)
        hBox3.Add(self.FreqEnd1,0,wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
        sizer.Add((20,10))
        hBox3=wx.BoxSizer(wx.HORIZONTAL)          
        hBox3.Add(self.Check2,0,wx.LEFT|wx.ALIGN_BOTTOM,20)      
        hBox3.Add(self.FreqStart2,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        hBox3.Add(wx.StaticText(panel,-1,u"——"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,10)
        hBox3.Add(self.FreqEnd2,0,wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
        sizer.Add((20,10))
        hBox3=wx.BoxSizer(wx.HORIZONTAL)      
        hBox3.Add(self.Check3,0,wx.LEFT|wx.ALIGN_BOTTOM,20)          
        hBox3.Add(self.FreqStart3,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        hBox3.Add(wx.StaticText(panel,-1,u"——"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,10)
        hBox3.Add(self.FreqEnd3,0,wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
        sizer.Add((20,10))
        hBox3=wx.BoxSizer(wx.HORIZONTAL)          
        hBox3.Add(self.Check4,0,wx.LEFT|wx.ALIGN_BOTTOM,20)      
        hBox3.Add(self.FreqStart4,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        hBox3.Add(wx.StaticText(panel,-1,u"——"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,10)
        hBox3.Add(self.FreqEnd4,0,wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
        sizer.Add((20,10))
        hBox3=wx.BoxSizer(wx.HORIZONTAL)          
        hBox3.Add(self.Check5,0,wx.LEFT|wx.ALIGN_BOTTOM,20)      
        hBox3.Add(self.FreqStart5,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        hBox3.Add(wx.StaticText(panel,-1,u"——"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,10)
        hBox3.Add(self.FreqEnd5,0,wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
        sizer.Add((20,20))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.Button(panel,wx.ID_OK,"OK",size=(60,25)),0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_CANCEL,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)
        self.Bind(wx.EVT_RADIOBOX, self.OnRadio)
        self.textM.Enable(False)
        self.StaticThres.Enable(False)
        self.Bind(wx.EVT_CHECKBOX,self.OnCheck)
        self.FreqStart2.Enable(False)
        self.FreqStart3.Enable(False)
        self.FreqStart4.Enable(False)
        self.FreqStart5.Enable(False)
        
        self.FreqEnd2.Enable(False)
        self.FreqEnd3.Enable(False)
        self.FreqEnd4.Enable(False)
        self.FreqEnd5.Enable(False)
        self.Check1.SetValue(False)

        print '*************************'

    def OnRadio(self,event):
        if(self.RadioBoxTrans.GetSelection()==2):
            self.textM.Enable(True)
        else:
            self.textM.Enable(False)
        if(self.RaioBoxThres.GetSelection()==0):
            self.AdaptThres.Enable(True)
            self.StaticThres.Enable(False)
        else:
            self.AdaptThres.Enable(False)
            self.StaticThres.Enable(True)

    def OnCheck(self,event):
        if(self.RadioBoxSweep.GetSelection()==1):
            if(self.Check1.GetValue()):
                self.FreqStart1.Enable(True)
                self.FreqEnd1.Enable(True)

        elif(self.RadioBoxSweep.GetSelection()==2):
            if(self.Check1.GetValue()):
                self.FreqStart1.Enable(True)
                self.FreqEnd1.Enable(True)
            elif(self.Check2.GetValue()):
                self.FreqStart2.Enable(True)
                self.FreqEnd2.Enable(True)
            elif(self.Check3.GetValue()):
                self.FreqStart3.Enable(True)
                self.FreqEnd3.Enable(True)
            elif(self.Check4.GetValue()):
                self.FreqStart4.Enable(True)
                self.FreqEnd4.Enable(True)
            
            elif(self.Check5.GetValue()):
                self.FreqStart5.Enable(True)
                self.FreqEnd5.Enable(True)

class ChangeAnotherIQPara(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"台站登记属性查询",size=(350,350))
class ChangeAnotherPress(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"台站登记属性查询",size=(350,350))


#######################请求历史功率谱和历史IQ数据#########################
class SetSpecTimeDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"指定终端历史功率谱查询",size=(400,350))
        panel=wx.Panel(self,-1)
        self.ApointID=wx.TextCtrl(panel,-1,size=(80,25))
        self.StartTimeYear=wx.ComboBox(panel,-1,"2015",choices=["2015","2016","2017","2018"])
        self.StartTimeMonth=wx.ComboBox(panel,-1,"12",choices=["1","2","3","4","5","6","7","8","9","10","11","12"])
        self.StartTimeDay=wx.TextCtrl(panel,-1,"1",size=(60,25))
        self.StartTimeHour=wx.TextCtrl(panel,-1,"0",size=(60,25))
        self.StartTimeMinute=wx.TextCtrl(panel,-1,"0",size=(60,25))

        self.EndTimeYear=wx.ComboBox(panel,-1,"2015",choices=["2015","2016","2017","2018"])
        self.EndTimeMonth=wx.ComboBox(panel,-1,"12",choices=["1","2","3","4","5","6","7","8","9","10","11","12"])
        self.EndTimeDay=wx.TextCtrl(panel,-1,"1",size=(60,25))
        self.EndTimeHour=wx.TextCtrl(panel,-1,"0",size=(60,25))
        self.EndTimeMinute=wx.TextCtrl(panel,-1,"0",size=(60,25))
        
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add((10,30))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"指定设备ID:",size=(100,25)),0,wx.LEFT,20)
        hBox1.Add(self.ApointID,0,wx.LEFT,20)
        sizer.Add(hBox1)
        sizer.Add((10,10))
        sizer.Add(wx.StaticText(panel,-1,u"起始时间(年-月-日-时-分)：",size=(160,25)),0,wx.LEFT,20)
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.StartTimeYear,0,wx.LEFT,20)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeMonth,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeDay,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeHour,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeMinute,0)
        sizer.Add(hBox1)

        sizer.Add((10,10))
        sizer.Add(wx.StaticText(panel,-1,u"终止时间(年-月-日-时-分)：",size=(160,25)),0,wx.LEFT,20)
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.EndTimeYear,0,wx.LEFT,20)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeMonth,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeDay,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeHour,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeMinute,0)
        sizer.Add(hBox1)
        sizer.Add((30,30))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.Button(panel,wx.ID_OK,"OK",size=(60,25)),0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_CANCEL,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)

class SetDemodTimeDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"指定终端IQ数据查询",size=(400,350))
        panel=wx.Panel(self,-1)
        self.ApointID=wx.TextCtrl(panel,-1,size=(80,25))
        self.StartTimeYear=wx.ComboBox(panel,-1,"2015",choices=["2015","2016","2017","2018"])
        self.StartTimeMonth=wx.ComboBox(panel,-1,"12",choices=["1","2","3","4","5","6","7","8","9","10","11","12"])
        self.StartTimeDay=wx.TextCtrl(panel,-1,"1",size=(60,25))
        self.StartTimeHour=wx.TextCtrl(panel,-1,"0",size=(60,25))
        self.StartTimeMinute=wx.TextCtrl(panel,-1,"0",size=(60,25))

        self.EndTimeYear=wx.ComboBox(panel,-1,"2015",choices=["2015","2016","2017","2018"])
        self.EndTimeMonth=wx.ComboBox(panel,-1,"12",choices=["1","2","3","4","5","6","7","8","9","10","11","12"])
        self.EndTimeDay=wx.TextCtrl(panel,-1,"1",size=(60,25))
        self.EndTimeHour=wx.TextCtrl(panel,-1,"0",size=(60,25))
        self.EndTimeMinute=wx.TextCtrl(panel,-1,"0",size=(60,25))
        
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add((10,30))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"指定设备ID:",size=(100,25)),0,wx.LEFT,20)
        hBox1.Add(self.ApointID,0,wx.LEFT,20)
        sizer.Add(hBox1)
        sizer.Add((10,10))
        sizer.Add(wx.StaticText(panel,-1,u"起始时间(年-月-日-时-分)：",size=(160,25)),0,wx.LEFT,20)
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.StartTimeYear,0,wx.LEFT,20)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeMonth,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeDay,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeHour,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeMinute,0)
        sizer.Add(hBox1)

        sizer.Add((10,10))
        sizer.Add(wx.StaticText(panel,-1,u"终止时间(年-月-日-时-分)：",size=(160,25)),0,wx.LEFT,20)
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.EndTimeYear,0,wx.LEFT,20)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeMonth,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeDay,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeHour,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeMinute,0)
        sizer.Add(hBox1)
        sizer.Add((30,30))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.Button(panel,wx.ID_OK,"OK",size=(60,25)),0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_CANCEL,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)



        





        

