#!/usr/bin/python
# -*- coding: utf-8 -*-
# The modules required
import sys
import socket
import struct
import os
import random

def xor(s,t):
    if isinstance(s, str):
        return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(s, t))
    else:
        return bytes([a ^ b for a, b in zip(s, t)])

def check(cipherText,key,message):
    if xor(cipherText, key).decode('utf8') == message:
        print('Unit test passed')
        return True
    else:
        print('Unit test failed')
        return False

def send_and_receive_tcp(address, port):
    message = "HELLO ENC\r\n"   
    laskuri=-1
    keys=[None]*20
    
    for z in range(0,20):
	if(z!=19):
            keys[z]=os.urandom(32).encode('hex')+"\r\n"
	if(z==19):
	    keys[z]=os.urandom(32).encode('hex')+"\r\n"+".\r\n"
        laskuri+=1
        print ("Alkuperainen avain"+str(laskuri)+":  "+keys[z])
	
    message=message+''.join(keys)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address, port))
    s.send(message)
    
    data = s.recv(2000)
    s.close()                                      
    print (data + "TCP TOIMII")
    mystring = data
    port1 = mystring.split("\r")[0]
    port = int(port1.split(" ")[2])
    data = port1.split(" ")[1]
    keysServer = mystring.split("\n")
    palikka=1
    for a in range (1,21):
	print "server avaimet"+str(palikka)+" "+keysServer[a] 
	palikka=palikka+1                                       
                                          
    send_and_receive_udp(address, port, data,keys,keysServer)

    return


def send_and_receive_udp(address, port,message,keys,keysServer):
    cidMessage ="Hello from " + message
    structmessage= "Hello from "
    addressIp = "185.38.3.247"
    udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    laskuri=0
    x=1

    cipherText = xor(cidMessage.encode('utf8'), keys[x])
    myStruct = struct.pack('!8s??HH64s',message,True,False,0,len(cipherText),cipherText)
    print "oma pakattu"+myStruct
    udpsocket.sendto(myStruct,(addressIp, port))
    
      
    while(True):
        data, server = udpsocket.recvfrom(2000)
        
	print "server avainnumero on "+str(x)
	data= struct.unpack('!8s??HH64s', data)
        
	cid,ack,eom,dataRemain,length,content=data
	print content, type(content)
	keysServer[x] = (keysServer[x][:length]) if len(keysServer[x]) > length else content
	mystring=content
        print "data receive is",xor(mystring,keysServer[x]).decode('utf8')
        """onko data vai random sanat"""
        purettu=xor(mystring, keysServer[x]).decode('utf8')
    	"""Tarkista content sijainti,avain saattaa vaikuttaa"""
        print ("purettu "+purettu) 
        z = purettu.split(" ")
        z.reverse()
        d = ' '.join(z)
        print ("d on "+d)
	print "oma avainnumero"+str(x)
	cipherText = xor(d.encode('utf8'), keys[x])
        myStruct = struct.pack('!8s??HH64s',message,True,False,0,len(cipherText),cipherText)
        udpsocket.sendto(myStruct,(addressIp, port))
        x=x+1

    udpsocket.close()

    return
    

def main():
    USAGE = 'usage: %s <server address> <server port> ' % sys.argv[0]

    try:
       
        server_address = str(sys.argv[1])
        server_tcpport = int(sys.argv[2])
        
    except (IndexError, ValueError):
     
        sys.exit(USAGE)

    send_and_receive_tcp(server_address, server_tcpport)


if __name__ == '__main__':
    main()
