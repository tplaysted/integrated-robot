# Command listener in python

import zmq
from time import sleep
import argparse as ap

# Get command line arguments

parser = ap.ArgumentParser(description='Listens to control actions published by the remote server.')
parser.add_argument('-i', '--interface', 
                    type=str,
                    help='Start the subscriber on a specific interface. Default is localhost')
parser.add_argument('-p', '--port', 
                    type=int,
                    help='Start the subsciber on a specific port. Default is 5555')

args = parser.parse_args()
context = zmq.Context()

interface = 'localhost' if args.interface is None else args.interface
port = '5555' if args.port is None else str(args.port)

context = zmq.Context()

#  Socket to talk to server
print("Connecting to command server…")
socket = context.socket(zmq.SUB)
socket.setsockopt_string(zmq.SUBSCRIBE, 'cmd')
socket.setsockopt(zmq.CONFLATE, 1) # only get the most recent command

socket.connect('tcp://' + interface + ':' + port)
print(f'Subscribed to port {port} on interface {interface} ...')

# Poll the command publisher indefinitely every 10ms
while True:
    try: 
        message = socket.recv_string(flags=zmq.NOBLOCK).split(':')[1] # queue might be empty
        print(f'Current command = {message}')
    except zmq.Again as e:
        pass
    
    sleep(0.01)


