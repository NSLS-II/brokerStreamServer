from __future__ import (print_function, division, unicode_literals)

import socket
import select
import time
import json
import numpy as np
import base64


def read_json_from_socket(host, port, max_attempts=None,
                          timeout=10, object_hook=None):
    """
    Read a json string from a socket and convert to an object

    The socket will be single use and read until exhausted.

    The read string will be interpreted as a json string and the
    resulting object is return.

    This function will keep trying up to max_attempts times, each with a
    time out given by timeout.

    Parameters
    ----------
    host : str
        The host to try to read data from

    port : int
        The port on the host to read from

    max_attempts : int or None, optional
        The maximum number of times to try

    timeout : float, optional
        The timeout in seconds.  The default is 10

    object_hook : function, optional
        Go look up the json hook docs,  Hook function for
        decoding the json string.  Defaults to a function
        that knows decodes the  encoding of numpy arrays
        from default setting of `write_json_to_socket`

    Returns
    -------
    out : object
        What ever came across the wire as an object
    """
    if object_hook is None:
        object_hook = json_numpy_obj_hook
    count = 0
    while max_attempts is None or count < max_attempts:
        data = None
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        ready = select.select([s], [], [], timeout)

        if ready[0]:
            accum_data = []
            data = s.recv(4096)
            while len(data):
                accum_data.append(data)
                data = s.recv(4096)
            data = ''.join(accum_data)
            if data:
                data = json.loads(data, object_hook=object_hook)
                return data
        # if we have made it to here, could not open the socket or it had no
        # data, throw socket away and try again
        s.close()
        time.sleep(.01)  # might not need this, but
        count += 1


def write_json_to_socket(data, host, port, json_encoder=None):
    """
    Dumps data across the wire.

    Parameters
    ----------
    data : object
        Any python object that can be turned into json

    host : str
        Where to try to push the data to

    port : int
        The port to push to

    json_encoder : JSONEncoder, optional
        Encoder class to deal with converting the object
        to a string.  Defaults to an encoder than knows about
        numpy arrays.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    dstr = json.dumps(data, cls=NumpyEncoder)
    s.sendall(dstr)
    s.close()
    pass


# Lifted from:
# http://stackoverflow.com/a/24375113/380231
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        """ if input object is a ndarray it will be converted into a
        dict holding dtype, shape and the data base64 encoded
        """
        if isinstance(obj, np.ndarray):
            data_b64 = base64.b64encode(obj.data)
            return dict(__ndarray__=data_b64,
                        dtype=str(obj.dtype),
                        shape=obj.shape)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder(self, obj)


# Lifted from:
# http://stackoverflow.com/a/24375113/380231
def json_numpy_obj_hook(dct):
    """
    Decodes a previously encoded numpy ndarray
    with proper shape and dtype
    :param dct: (dict) json encoded ndarray
    :return: (ndarray) if input was an encoded ndarray
    """
    if isinstance(dct, dict) and '__ndarray__' in dct:
        data = base64.b64decode(dct['__ndarray__'])
        return np.frombuffer(data, dct['dtype']).reshape(dct['shape'])
    return dct
