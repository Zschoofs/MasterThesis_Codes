import selectors
import socket
from datetime import datetime
import types

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM = tcp by default
sel = selectors.DefaultSelector()

HOST = '192.168.1.5'
PORT = 9050

sock.bind((HOST,PORT)) #raspberrry that listen
sock.listen()  # allow only 1 connection

sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, data=None)

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    #Any data that’s read is appended to data.outb so that it can be sent later.
    if mask & selectors.EVENT_READ:
        data_recv = sock.recv(1024)  # Should be ready to read
        if data_recv:
            str = data_recv.decode('ascii')

            # Create timestamp to add to the data
            dt = datetime.now()
            date = dt.date().strftime('%y-%m-%d')
            stringDate = dt.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            str2 = stringDate + ' ' + str
            print(str2)

            # Write the received data in a file specific to the date
            fichier = open(date + ".txt", "a")
            fichier.write("\n" + str2)
            fichier.close()
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
