__author__ = 'arkilic'
import socket
import random
import broker.config as cfg
import json
from metadataStore.collectionapi import commands



def create(header=None, beamline_config=None,event_descriptor=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((cfg.HOST, cfg.PORT))
    except:
        raise socket.SO_ERROR('Cannot establish connection to server')

    #send across to metadataStore
    #this validates the entry.
    #TODO: Add means to ensure data structure on header, beamline_config, and event_descriptor
    # commands.create(header=header, beamline_config=beamline_config, event_descriptor=event_descriptor)
    data = json.dumps(beamline_config)
    s.sendall(data)


def record(event_dict):
    pass

create(beamline_config={'scan_id': 1})
