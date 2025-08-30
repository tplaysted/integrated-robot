# Command listener in python

import zmq
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep
import argparse as ap

# pyright: reportMissingImports=false

pigpio_factory = PiGPIOFactory()
tilt_speed = 90 # degrees per second

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
    print("Servo listener connecting to host...")
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, 'tilt')
    socket.setsockopt(zmq.CONFLATE, 1) # only get the most recent command

    socket.connect('tcp://' + interface + ':' + port)
    print(f'Servo listener subscribed to port {port} on interface {interface} ...')

    rate = 100 if args.rate is None else args.rate

    angle = 0
    target = 0
    request = ''
    delta = tilt_speed / rate

    servo = AngularServo(24, pin_factory=pigpio_factory,
                             min_angle=180,
                             max_angle=0,
                             min_pulse_width=0.5/1000,
                             max_pulse_width=2.5/1000)

    # Begin the control loop
    while True:
        try: # get any new commands
            request = socket.recv_string(flags=zmq.NOBLOCK).split(':')[1] # queue might be empty
            target = int(request)
            print(f'Got angle request: {target:.2f}°')
        except zmq.Again:
            pass # don't have to do anything - tilt should retain its previous value
        except ValueError:
            print(f'Servo listener got angle request \'{request}\', expected int.')


        if target > angle:
            angle = min(angle + delta, target)

        if target < angle:
            angle = max(angle - delta, target)

        try:
            servo.angle = angle
        except:
            print('Unable to set servo')

        sleep(1 / rate)
