import socket
import RPi.GPIO as GPIO
import time


HOST = '192.168.1.5'
PORT = 9050

print('Connected to server')
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN_1 = 23
PIR_PIN_2 = 24
GPIO.setup(PIR_PIN_1, GPIO.IN)
GPIO.setup(PIR_PIN_2, GPIO.IN)

print('Starting up the PIR Module ')
time.sleep(1)

while True:
    if GPIO.input(PIR_PIN_1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))  # connection to the server and initiate the three-way handshake
            print('Motion 1')
            sock.sendall('Motion Detected on 1'.encode('ascii'))
            sock.close()
        except IOError as e:
            if e.errno == 101:
                print("Network Error")
                time.sleep(1)
    if GPIO.input(PIR_PIN_2):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))  # connection to the server and initiate the three-way handshake
            sock.sendall('Motion Detected on 2'.encode('ascii'))
            print('Motion 2')
            sock.close()
        except IOError as e:
            if e.errno == 101:
                print("Network Error")
                time.sleep(1)
    time.sleep(1)
