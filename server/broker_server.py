'''
    Simple socket server using threads
    '''

import socket
import sys
from thread import *
from Queue import Queue

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8331 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Binding the socket failed'
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'


def clientthread(conn,queue):
    #Function to create client threads!
    #Whenever a client is connected to the server, a dedicated thread is initiated
    while True:
        #Receiving from client that this thread is assigned to
        try:
            data = conn.recv(16)
            print data
            queue.put(data)
            print 'queue size from thread', queue.qsize()
        except:
            raise
       # if not data:
       #     break
        conn.sendall(data)
    #whatever is received, send it to all clients
    
    #came out of loop
    conn.close()



while 1:
    queue = Queue()
    #client
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
        
    start_new_thread(clientthread ,(conn,queue,))
    print 'Here is the queue size', queue.qsize()
    #conn.sendall('arman'+ addr[0])
s.close()
