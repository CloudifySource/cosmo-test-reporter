import json
import logging
import socket

__author__ = 'nirb'

UDP_IP = "54.247.25.231"
UDP_PORT = 9998


class UdpJsonHandler(logging.Handler):

    def __init__(self):
        # run the regular Handler __init__
        logging.Handler.__init__(self)

        #TODO construct default dict
        self.log_dict = {'test_name': 'demo', 'blueprint': 'none'}

    def emit(self, record):
        self.log_dict['log_message'] = self.format(record)
        msg = json.dumps(self.log_dict)

        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.sendto(msg, (UDP_IP, UDP_PORT))