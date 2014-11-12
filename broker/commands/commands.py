__author__ = 'arkilic'
import socket
import random
import broker.config as cfg
import json
from metadataStore.collectionapi import commands


def create(header=None, beamline_config=None,event_descriptor=None):
    """
    Create a run header, beamline_config, and/or event_descriptor. First dump it into metadataStore then
    stream it to data analysis clients

    :param header: metadataStore run header
    :type header: dict

    :param beamline_config: metadataStore beamline_configuration
    :type beamline_config: dict

    :param event_descriptor: metadataStore event_descriptor
    :type event_descriptor: dict

    :return: Operation completion status
    :rtype: bool
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((cfg.HOST, cfg.PORT))
    except:
        raise
    try:
        commands.create(header=header, beamline_config=beamline_config, event_descriptor=event_descriptor)
    except:
        s.close()
        raise
    content_list = list()
    temp = dict()

    if header is not None:
        temp['content'] = 'header'
        temp['payload'] = header
        content_list.append(temp)
        temp = dict()

    if beamline_config is not None:
        temp['content'] = 'beamline_config'
        temp['payload'] = beamline_config
        content_list.append(temp)
        temp = dict()

    if event_descriptor is not None:
        temp['content'] = 'event_descriptor'
        temp['payload'] = event_descriptor
        content_list.append(temp)
        temp = dict()

    data = json.dumps(content_list)
    s.sendall(data)
    return True


def record(event):
    """

    :param event:
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((cfg.HOST, cfg.PORT))
    except:
        raise
    try:
        commands.record(event=event)
    except:
        s.close()
        raise
    content_list = list()
    temp = dict()

    if event is not None:
        temp['content'] = 'event'
        temp['payload'] = event
        content_list.append(temp)
    data = json.dumps(content_list)
    s.sendall(data)
    return True


def test():
    import random

    for i in xrange(2):
        print i
        x = random.randint(0,10000)

        create(header={'scan_id':x , 'tags': ['CSX_Experiment1', 'CSX_Experiment2']} ,
               event_descriptor={'scan_id': x, 'descriptor_name': 'scan', 'event_type_id': 12, 'tag': 'experimental'})

        record(event={'scan_id': x, 'descriptor_name': 'scan', 'seq_no': 0})
