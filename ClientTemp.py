import socket
from time import sleep

import Adafruit_DHT

HOST = '192.168.1.5'
PORT = 9050

print('Connected to server')
# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT22

pin = 17

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

while True :
    if humidity is not None and temperature is not None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            str='Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
            sock.connect((HOST, PORT))  # connection to the server and initiate the three-way handshake
            print(str)
            data=bytes(str, encoding="ascii")
            sock.sendall(data)
            sock.close()
        except IOError as e:
            if e.errno == 101:
                print("Network Error")
                sleep(1)

    else:
        print('Failed to get reading. Try again!')
    sleep(600) #Wait 10 minutes
