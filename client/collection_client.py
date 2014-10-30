import socket
import random
import broker.config as cfg
import json
import numpy as np
import time

for j in range(15):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((cfg.HOST, cfg.PORT))
    a = [{'arman': 2, 'diego': 3, 'count': j},
         {'arman': 2, 'img': np.random.rand(5, 5).tolist(), 'count': j},
         ]
    data = json.dumps(a)

    s.sendall(data)

    s.close()
    time.sleep(1)
