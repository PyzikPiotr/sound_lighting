import numpy as np #importing Numpy with an alias np
import pyaudio as pa 
import struct 
import matplotlib.pyplot as plt 
import pygame
import socket

#----------Socket---------------------------
HOST = "192.168.100.55"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
#----------Socket---------------------------
#pyaudio-----------------------------------
CHUNK = 1024 * 1
FORMAT = pa.paInt16
CHANNELS = 1
RATE = 44100 # in Hz
p = pa.PyAudio()
stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input=True,
    frames_per_buffer=CHUNK
)
#pyaudio-----------------------------------
def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

difference = 0.2#w %
def checkDifference(prev, now):
    if now-prev>difference*now:
        return(True)
    else:
        return(False)
bass_max=1
mid_max=1
rest_max=1
fall=0.0001
color_fall=20
def appendTo3(number):
    number = str(number)
    while len(number)<3:
        number = "0"+number
    return number
prev_bass, prev_mid, prev_rest = 0,0,0
pygame.init()
screen = pygame.display.set_mode([500, 500])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall("000000000".encode('utf-8'))
    while 1:
        data = stream.read(CHUNK)
        dataInt = struct.unpack(str(CHUNK) + 'h', data)
        all = np.abs((np.fft.fft(dataInt))*2/(11000*CHUNK))
        bass = np.average(all[0:10])*10#zielony
        mid = np.average(all[50:100])*10000#niebieski
        rest = all[100:200].max()*10000
        # bass = all[0:13].max()*100#zielony
        # mid = all[18:100].max()*10000#niebieski
        # rest = all[101:200].max()*10000#czerwony
        # bass=all[0:17].max()
        # mid=all[17:100].max()
        # rest=
        if bass>bass_max:
            bass_max=bass
        else: 
            if bass_max>0.01: bass_max-=fall
        if mid>mid_max:
            mid_max=mid
        else:
            if mid_max>0.001: mid_max-=fall
        if rest>rest_max:
            rest_max=rest
        else:
            if rest_max>0.001: rest_max-=fall
            
        bass = translate(bass,0,bass_max,0,255)
        mid = translate(mid,0,mid_max,0,255)
        rest = translate(rest,0,rest_max,0,255)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        if(prev_bass>bass):#zielony
            prev_bass-=(color_fall*(prev_bass/255))
        else:
            if checkDifference(prev_bass,bass): prev_bass=bass
        if(prev_mid>mid):#niebieski
            prev_mid-=(color_fall*(prev_mid/255))
        else:
            if checkDifference(prev_mid,mid):prev_mid=mid
        if(prev_rest>rest):#czerwony
            prev_rest-=(color_fall*(prev_rest/255))
        else:
            if checkDifference(prev_rest,rest):prev_rest=rest
        if prev_bass<0:prev_bass=0
        if prev_mid<0:prev_mid=0
        if prev_rest<0:prev_rest=0
        pygame.draw.circle(screen, (abs(prev_rest), 0, 0), (250, 100), 75)#czerwony
        pygame.draw.circle(screen, (0, abs(prev_bass), 0), (100, 250), 75)#zielony
        pygame.draw.circle(screen, (0, 0, abs(prev_mid)), (250, 250), 75)#niebieski
        if len(s.recv(1024))>0:
            data_string = f'{appendTo3(int(prev_rest))}{appendTo3(int(prev_bass))}{appendTo3(int(prev_mid))}'
            s.sendall(data_string.encode('utf-8'))
        pygame.display.flip()
pygame.quit()
    