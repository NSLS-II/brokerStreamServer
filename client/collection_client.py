import socket
import random
import broker.config as cfg
import json

range_val = random.randint(0,100)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.connect((cfg.HOST, cfg.PORT))


a = [{'arman': 2, 'diego': 3},{'arman': 2, 'diego': 3}, {'bruno': 25, 'stuart': 29}]
data = json.dumps(a)

s.sendall(data)

s.close()


