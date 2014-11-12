from __future__ import print_function, division

import socket
import broker.config as cfg
import json
import numpy as np
import time
from nsls2 import core
import numpy as np

from client import write_json_to_socket

_im_shape = (150, 150)
center = 2000
sigma = 1250
_I_func = lambda count: (1 + np.exp(-((count - center)/sigma) ** 2))
_cur_position = np.array(np.asarray(_im_shape) / 2, dtype=np.float)


def _scale_func(scale, count):
    if not count % 50:
        return scale - .5
    if not count % 25:
        return scale + .5
    return None

_scale = 1
_count = 0
_decay = 30
for j in range(center * 2):
    # this as all synthetic data generation code
    print('spammed {}'.format(j))
    # add a random step
    step = np.random.randn(2) * _scale
    _cur_position += step
    # clip it
    _cur_position = np.array([np.clip(v, 0, mx) for
                                       v, mx in zip(_cur_position,
                                                    _im_shape)])

    R = core.pixel_to_radius(_im_shape,
                             _cur_position).reshape(_im_shape)

    I = _I_func(_count)
    im = np.exp((-R**2 / _decay)) * I

    a = []

    new_scale = _scale_func(_scale, _count)
    if new_scale is not None or _count == 0:
        _scale = new_scale
        a.append({'T': _scale})

    a.append({'img': im.tolist(), 'count': j})

    _count += 1

    # ##################################
    # this is the entirety of the socket nonsense
    write_json_to_socket(a, cfg.HOST, cfg.PORT)
    # ##################################

    # sleep for a bit to not clobber everything else
    time.sleep(.5)
