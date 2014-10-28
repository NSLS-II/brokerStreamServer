import socket
import random
import broker.config as cfg
import json

range_val = random.randint(0,100)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.connect((cfg.HOST, cfg.PORT))



# for i in xrange(range_val):
for i in xrange(500, 1000):
    a = {'arman': str(i)}
    data = json.dumps(a)

    s.sendall('arman' + str(i))

#print s.recv(4096)
s.close()
