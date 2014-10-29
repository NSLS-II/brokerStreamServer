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
        raise

    #send across to metadataStore
    #this validates the entry.
    #TODO: Add means to ensure data structure on header, beamline_config, and event_descriptor
    try:
        commands.create(header=header, beamline_config=beamline_config, event_descriptor=event_descriptor)
    except:
        s.close()
        raise
    content_list = list()
    my_data = dict()
    my_data['payload'] = 'header'
    if header is not None:
        my_data
    if beamline_config is not None:
        my_data.append(header)

    data = json.dumps(my_data)
    s.sendall(data)


def record(event_dict):
    pass


import random

x = random.randint(0,10000)
create(header={'scan_id':x , 'tags': ['CSX_Experiment1', 'CSX_Experiment2']})
