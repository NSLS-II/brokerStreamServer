__author__ = 'arkilic'
import time
import socket
import sys
from thread import start_new_thread
import broker.config as cfg
from Queue import Queue

HOST = cfg.HOST
PORT = cfg.PORT

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Sockets created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Binding the socket failed'
    sys.exit()

try:
    send_socket.bind((cfg.SEND_HOST, cfg.SEND_PORT))
except socket.error as msg:
    print 'Binding the socket failed'
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
send_socket.listen(10)
print 'Sockets now listening'
queue = Queue()

def remote_client_thread(send_conn,queue):
    """
    Function to create client threads!
    Whenever a client is connected to the server, a dedicated thread is initiated
    """
    while True:
        #Receiving from client that this thread is assigned to
        if queue.qsize() == 0:
            break
        else:
            print 'queue size from thread', queue.qsize()
            data = queue.get(block=True)
            try:
                send_conn.sendall(data)
                time.sleep(1) #wait as the data is being transmitted
            except:
                raise Exception('Cannot send data over send socket')
    send_conn.close()

while True:
    #accept connection and start_threads for each incoming request from collection clients
    # passing a send_server connection instance that will ship the requested data to
    #analysis clients listening
    conn, address = s.accept()
    send_connection, send_address = send_socket.accept()
    data = conn.recv(4096)
    print 'Connected with ' + address[0] + ':' + str(address[1])
    if data:
        queue.put(data)
        #place the data in the queue that is shared among all client threads
        start_new_thread(remote_client_thread, (send_connection, queue, )) #start new client thread

s.close()
