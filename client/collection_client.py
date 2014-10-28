import socket
import random

range_val = random.randint(0,100)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('localhost', 8339))
for i in xrange(range_val):
    s.send('arman'+str(i))
#print s.recv(4096)
s.close()
