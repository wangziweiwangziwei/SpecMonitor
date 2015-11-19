# -*- coding: utf-8 -*-
from ctypes import *

class FrameHeader(BigEndianStructure):
	_fields_=[("Header",c_ubyte),
	            ("FunctionPara",c_ubyte),
	            ("LowDeviceID",c_ubyte),
	            ("HighDeviceID",c_ubyte)
	           ]

class FrameTail(BigEndianStructure):
    _fields_=[("HighVerify",c_ubyte),
                ("LowVerify",c_ubyte),
                ("Tail",c_ubyte)
                ]

class CentreFreq(BigEndianStructure):
	_fields_=[("HighFreqInteger",c_uint8),
	          ("HighFreqFraction",c_uint8,2),
              ("LowFreqInteger",c_uint8,6),
              ("LowFreqFraction",c_uint8),
	            ]

class TimeSet(BigEndianStructure):
	_fields_=[("HighYear",c_uint8),
	          ("LowYear",c_uint8,4),
	          ("Month",c_uint8,4),
	          ("Day",c_uint8,5),
	          ("HighHour",c_uint8,3),
	          ("Minute",c_uint8,6),
	          ("LowHour",c_uint8,2),
	          ("Second",c_uint8),
	          ("ByteZero1",c_uint8),
	          ("ByteZero2",c_uint8),
	          ("ByteZero3",c_uint8)
	          ]

class LonLatAltitude(BigEndianStructure):
	_fields_=[ ("LonFlag",c_uint8),
			  ("LonInteger",c_uint8),
			  ("HighLonFraction",c_uint8),
			  ("LowLonFraction",c_uint8),
			  ("LatFlag",c_uint8,1),
			  ("LatInteger",c_uint8,7),
			  ("HighLatFraction",c_uint8),
			  ("LowLatFraction",c_uint8),
			  ("AltitudeFlag",c_uint8,1),
			  ("HighAltitude",c_uint8,7),
			  ("LowAltitude",c_uint8)
	]





#############扫频范围设置###########
class SweepRangeSet(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
	           ("SweepRecvMode",c_uint8,6),
	           ("FileUploadMode",c_uint8,2),
	           ("SweepSectionTotalNum",c_uint8),
	           ("SweepSectionNo",c_uint8),

	           ("StartSectionNo",c_uint8),
	           ("StartSixBit0",c_uint8,6),
	           ("HighStartFreq",c_uint8,2),
	           ("LowStartFreq",c_uint8),
	       
	           ("EndSectionNo",c_uint8),
	           ("EndSixBit0",c_uint8,6),
	           ("HighEndFreq",c_uint8,2),
	           ("LowEndFreq",c_uint8),
	            
	           ("ChangeThres",c_uint8,2),
	           ("ExtractM",c_uint8,6),
	           ("CommonTail",FrameTail)
	]

############定频接收中心频率设置#############
class IQFreqSet(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
	          ("FreqNum",c_uint8),
	          ("FreqArray",CentreFreq*3),
	          ("CommonTail",FrameTail)
	         ]

#############压制发射频率设置#############
class PressFreqSet(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
	          ("PressNum",c_uint8),
	          ("FreqArray",CentreFreq*2),
	          ("ByteZero1",c_uint8),
	          ("ByteZero2",c_uint8),
	          ("ByteZero3",c_uint8),
	          ("CommonTail",FrameTail)
	          ]

############接收通道增益设置##############

class RecvGainSet(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
              ("RecvGain",c_uint8),
              ("ByteZero1",c_uint8),
	          ("ByteZero2",c_uint8),
	          ("ByteZero3",c_uint8),
	          ("ByteZero4",c_uint8),
	          ("ByteZero5",c_uint8),
	          ("ByteZero6",c_uint8),
	          ("ByteZero7",c_uint8),
	          ("ByteZero8",c_uint8),
	          ("ByteZero9",c_uint8),
	          ("CommonTail",FrameTail)

	         ]


################发射通道衰减设置###########
class SendWeakSet(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
              ("SendWeak",c_uint8),
              ("ByteZero1",c_uint8),
	          ("ByteZero2",c_uint8),
	          ("ByteZero3",c_uint8),
	          ("ByteZero4",c_uint8),
	          ("ByteZero5",c_uint8),
	          ("ByteZero6",c_uint8),
	          ("ByteZero7",c_uint8),
	          ("ByteZero8",c_uint8),
	          ("ByteZero9",c_uint8),
	          ("CommonTail",FrameTail)

	         ]

###############检测门限设置###############
class ThresSet(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
              ("ThresMode",c_uint8),
              ("AdaptThres",c_uint8),
	          ("HighFixedThres",c_uint8),
	          ("LowFixedThres",c_uint8),
	          ("ByteZero1",c_uint8),
	          ("ByteZero2",c_uint8),
	          ("ByteZero3",c_uint8),
	          ("ByteZero4",c_uint8),
	          ("ByteZero5",c_uint8),
	          ("ByteZero6",c_uint8),
	          ("CommonTail",FrameTail)
	]

#############定频接收参数设置###########
class IQParaSet(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
	          ("BandWidth",c_uint8,4),
	          ("DataRate",TimeSet),
	          ("UploadNum",c_uint8),
	          ("Time",TimeSet),
	          ("CommonTail",FrameTail)
	]

############压制发射参数设置############
class PressParaSet(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
			  ("PressMode",c_uint8),
			  ("PressSignal",c_uint8,4),
			  ("PressSignalBandWidth",c_uint8,4),
			  ("HighT1",c_uint8),
			  ("LowT1",c_uint8),
			  ("HighT2",c_uint8),
			  ("LowT2",c_uint8),
			  ("HighT3",c_uint8),
			  ("LowT3",c_uint8),
			  ("HighT4",c_uint8),
			  ("LowT4",c_uint8),
			  ("CommonTail",FrameTail)

	]

#############硬件接入方式设置##########
class AccessWaySet(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
              ("AccessWay",c_uint8),
              ("ByteZero1",c_uint8),
	          ("ByteZero2",c_uint8),
	          ("ByteZero3",c_uint8),
	          ("ByteZero4",c_uint8),
	          ("ByteZero5",c_uint8),
	          ("ByteZero6",c_uint8),
	          ("ByteZero7",c_uint8),
	          ("ByteZero8",c_uint8),
	          ("ByteZero9",c_uint8),
              ("CommonTail",FrameTail)

	          ]


#############功率谱异常频点上传关闭关闭#######
class TransferSet(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
	          ("CommonTail",FrameTail)
	          ]

#############查询信令#########################################
class Query(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
	          ("CommonTail",FrameTail)
	          ]


#############终端是否在网及类型的应答#########
class IsConnectResponse(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
			  ("IsConnect",c_uint8),
			  ("TerminalType",c_uint8),
			  ("LonLatAlti",LonLatAltitude),
			  ("CommonTail",FrameTail)
	          ]

##############功率谱数据帧####################
class TwoFreq(BigEndianStructure):
    _fields_=[("HighFreq1dB",c_int8,4),
    		  ("HighFreq2dB",c_int8,4),
    		  ("LowFreq1dB",c_uint8),
    		  ("LowFreq2dB",c_uint8)
                ]


class SpecDataRecv(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
	          ("LonLatAlti",LonLatAltitude),
	          ("Time",TimeSet),
	          ("SweepRecvMode",c_uint8,2),
	          ("FileUploadMode",c_uint8,2),
	          ("SpecChangeFlag",c_uint8,4),
	          ("SweepSectionTotalNum",c_uint8),
	          ("CurSectionNo",c_uint8),
	          ("AllFreq",TwoFreq*512),
	          ("CommonTail",FrameTail)

	]

##############异常频点数据帧###################
class AbFreq(BigEndianStructure):
	_fields_=[("HighFreqNo",c_int8,4),
	          ("HighdB",c_int8,4),
	          ("LowFreqNo",c_uint8),
	          ("LowdB",c_uint8)
	          ]
class AbFreqRecv(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
	          ("LonLatAlti",LonLatAltitude),
	          ("Time",TimeSet),
	          ("CurSectionNo",c_uint8),
	          ("AbFreqNum",c_uint8),
	          ("AllAbFreq",AbFreq*10),
              ("CommonTail",FrameTail)

	]

##############IQ波形数据帧######################
class FreqIQ(BigEndianStructure):
	_fields_=[("HighIPath",c_int8,4),
	          ("HighQPath",c_int8,4),
	          ("LowIPath",c_uint8),
	          ("LowQPath",c_uint8)]

class IQDataPartHead(BigEndianStructure):
	_fields_=[("HighCentreFreqInteger",c_uint8),
	          ("HighCentreFreqFraction",c_uint8,2),
	          ("LowCentreFreqInteger",c_uint8,6),
	          ("LowCentreFreqFraction",c_uint8),
	          ("BandWidth",c_uint8,4),
	          ("DataRate",c_uint8,4),
	          ("UploadNum",c_uint8)]

class IQData(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
	          ("LonLatAlti",LonLatAltitude),
	          ("Time",TimeSet),
	          ("Param",IQDataPartHead),
	          ("CurBlockNo",c_uint8),
	          ("IQDataAmp",FreqIQ*2000),
	          ("CommonTail",FrameTail)

	]

##############文件上传##########################

##############功率谱文件上传########################
class FFTBlock(Union):
	_fields_=[("CurSectionNo",c_uint8),
	          ("AllFreq",TwoFreq*512)
	         ]
class SpecUploadHeader(Union):
	_fields_=[("Header",c_uint8),
	          ("LonLatAlti",LonLatAltitude),
	          ("SweepRecvMode",c_uint8,6),
	          ("FileUploadMode",c_uint8,2),
	          ("SpecChangeThres",c_uint8,2),
	          ("ExtractM",c_uint8,6),
	          ("SweepSectionTotalNum",c_uint8)
	          ]

class AbListBlock(Union):
	_fields_=[("CurSectionNo",c_uint8),
	           ("AbFreqNum",c_uint8),
               ("AllAbFreq",AbFreq*10)
	]

##############IQ波形文件上传#########################
class IQUploadHeader(Union):
	_fields_=[("Header",c_uint8),
	          ("LonLatAlti",LonLatAltitude),
	          ("Param",IQDataPartHead)
	          ]

class IQBlock(Union):
    _fields_=[("CurBlockNo",c_uint8),
              ("IQDataAmp",FreqIQ*2000)
 ]	    


############服务请求数据帧######################################

########终端入网请求#######################
class ConnectServer(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
	          ("TerminalType",c_uint8),
			  ("LonLatAlti",LonLatAltitude),
			  ("CommonTail",FrameTail)
	]

#######入网响应数据帧####################
class ConnectResponse(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
	          ("IsAgreeConnect",c_uint8),
	          ("TerminalType",c_uint8),
	          ("LonLatAlti",LonLatAltitude),
	          ("CommonTail",FrameTail)
	          ]




#########无线频率规划查询请求#################
class QueryFreqPlan(BigEndianStructure):
	_fields_=[("CommonHeader",FrameHeader),
	          ("FreqStartHigh",c_uint8),
                  ("FreqStartMid",c_uint8),
	          ("FreqStartLow",c_uint8),
	          ("FreqEndHigh",c_uint8),
                  ("FreqEndMid",c_uint8),
	          ("FreqEndLow",c_uint8),
	          ("CommonTail",FrameTail)
	         ]


