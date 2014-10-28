__author__ = 'arkilic'

import socket
from Queue import Queue
import broker.config as cfg

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
q = Queue()

x = 0
s.connect((cfg.SEND_HOST, cfg.SEND_PORT))

data = None
data = s.recv(4096)
if data:
    q.put(data)
    print 'analysis received', data

s.close()
