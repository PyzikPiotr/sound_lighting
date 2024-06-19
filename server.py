import socket
import serial
HOST = "127.0.0.1" 
PORT = 65432 
ports = ['/dev/ttyUSB1','/dev/ttyUSB0','/dev/ttyACM0']
for port in ports:
	try:
		ser = serial.Serial(port, 115200)
	except:
		print("lel")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(9)
            conn.sendall(data)
            ser.write((data.decode("utf-8")+'\n').encode('utf-8'))
