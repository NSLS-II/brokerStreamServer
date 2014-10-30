__author__ = 'arkilic'

import socket
from Queue import Queue
import broker.config as cfg
import time
import select


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
q = Queue()
s.connect((cfg.SEND_HOST, cfg.SEND_PORT))
print 'Sockets now connected'

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