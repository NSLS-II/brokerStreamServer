import socket
import random
import broker.config as cfg
import json

range_val = random.randint(0,100)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.connect((cfg.HOST, cfg.PORT))


import time
# for i in xrange(range_val):

a = [{'arman': 2, 'diego': 3},{'arman': 2, 'diego': 3}, {'bruno': 5, 'stuart': 6}]
data = json.dumps(a)

s.sendall(data)

   # time.sleep(1)
#print s.recv(4096)
s.close()


