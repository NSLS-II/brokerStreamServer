__author__ = 'arkilic'

import socket
from Queue import Queue
import broker.config as cfg
import time


def server_receive_thread(s, q):
    # while True:
    time.sleep(1)
    data = s.recv(4096)
    if data:
        q.put(data, block=False)
        print 'data arrived at the client server', data

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
q = Queue()
s.connect((cfg.SEND_HOST, cfg.SEND_PORT))

print 'Sockets now connected'
import select

s.setblocking(0)
data = None
ready = select.select([s], [], [], 10)
if ready[0]:
    try:
        data = s.recv(4096)
    except:
        raise
if data:
    print 'data arrived at the client server', data
    q.put(data)
s.close()