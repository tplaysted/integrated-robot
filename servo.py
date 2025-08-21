# Command listener in python

import zmq
from gpiozero import AngularServo
from time import sleep
import argparse as ap

# pyright: reportMissingImports=false

targets = { # target velocity for the wheels [lv, rv] for each command
    'forward': [1, 1],
    'forwardleft': [0.5, 1],
    'forwardright': [1, 0.5],
    'backward': [-1, -1],
    'backwardleft': [-0.5, -1],
    'backwardright': [-1, -0.5],
    'pivotleft': [-1, 1],
    'pivotright': [1, -1],
    'still': [0, 0]
}

tilt_speed = 30 # degrees per second

def update_vel(current, target, delta): # step current vel towards target vel
    if current < target:
        return min(target, current + delta)

    if current > target:
        return max(target, current - delta)

    return current

if __name__=="__main__":
    # Get command line arguments
    parser = ap.ArgumentParser(description='Listens to control actions published by the remote server.')
    parser.add_argument('-i', '--interface',
                        type=str,
                        help='Start the subscriber on a specific interface. Default is localhost')
    parser.add_argument('-p', '--port',
                        type=int,
                        help='Start the subsciber on a specific port. Default is 5555')
    parser.add_argument('-r', '--rate',
                        type=int,
                        help='Approximate frequency of the control loop - default is 100 Hz')

    args = parser.parse_args()
    context = zmq.Context()

    interface = 'localhost' if args.interface is None else args.interface
    port = '5555' if args.port is None else str(args.port)

    context = zmq.Context()

    #  Socket to talk to server
    print("Connecting to command server…")
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, 'tilt')
    socket.setsockopt(zmq.CONFLATE, 1) # only get the most recent command

    socket.connect('tcp://' + interface + ':' + port)
    print(f'Subscribed to port {port} on interface {interface} ...')

    rate = 100 if args.rate is None else args.rate

    angle = 0
    delta = tilt_speed / rate
    tilt = 'stop' # this is the command

    servo = AngularServo(24)

    # Begin the control loop
    while True:
        try: # get any new commands
            tilt = socket.recv_string(flags=zmq.NOBLOCK).split(':')[1] # queue might be empty
        except zmq.Again:
            pass # don't have to do anything - cmd should retain its previous value

        print(tilt)


        sleep(1 / rate)
