# -*- coding: utf-8 -*-
import socket
###########下面每次接收的都是结构体对象###########
'''
def SendSetData(structrueObj):
	outPoint1.write(structrue)

def SendQueryData(structrueObj):
	outPoint2.write(structrue)

def ReceiveQueryData():
	recvQueryData=inPoint1.read()

def ReceiveFFT():
	recvFFT=inPoint2.read()
def ReceiveAbList():
	recvAbList=inPoint2.read()

def ReceiveIQ():
	recvIQ=inPoint2.read()
'''

#####################中心站的查询#######################
class ServerCommunication():
    def __init__(self):
        self.sock=0
    def ConnectToServer(self):
    	try:
	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    sock.connect(('115.156.209.29',9123))
	    print 'Client connect !' 
	    self.sock=sock
	except:
	    print 'Fail to Connect To  Server!!!!!!!!! '
	    self.sock.close()

    def SendQueryData(self,frameLen,structrueObj):
	    barray=bytearray(structrueObj)
	    self.sock.send(barray)

    def DisconnectToServer(self):
	    self.sock.close()

