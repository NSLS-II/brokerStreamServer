__author__ = 'arkilic'

import socket
from Queue import Queue
import broker.config as cfg
import time
import select

q = Queue()

while True:
    print('Top of the loop')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((cfg.SEND_HOST, cfg.SEND_PORT))
    print 'Sockets now connected'

    #    s.setblocking(True)
    data = None
    ready = select.select([s], [], [], 10)
    if ready[0]:
        print('ready')

        accume_data = []
        data = s.recv(4096)
        while len(data):
            accume_data.append(data)
            data = s.recv(4096)

        data = ''.join(accume_data)


    if data:
        print 'data arrived at the client server', len(data)
        q.put(data)
    s.close()
    time.sleep(.01)
