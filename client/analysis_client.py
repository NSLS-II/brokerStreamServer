__author__ = 'arkilic'

import socket
from thread import start_new_thread
from Queue import Queue
import broker.config as cfg
import sys


def server_receive_thread(conn, q):
    while True:
        data = conn.recv(4096)
        if data:
            q.put(data, block=False)
            print 'data arrived at the client server', data
        else:
            break

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
q = Queue()

try:
    s.bind((cfg.SEND_HOST, cfg.SEND_PORT))
except socket.error as msg:
    print 'Binding the socket failed'
    sys.exit()


s.listen(10)
print 'Sockets now listening'

import time
while True:
    conn, address = s.accept()
    start_new_thread(server_receive_thread, (conn, q, ))
    time.sleep(1)
s.close()