# Command listener in python

import zmq
from gpiozero import Motor
from time import sleep
import argparse as ap

# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false

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

period = 1 # the time in seconds to ramp from zero to full speed
pwm_freq = 5000
throttle = 0.8

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
    print("Motor command listener connecting to host…")
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, 'cmd')
    socket.setsockopt(zmq.CONFLATE, 1) # only get the most recent command

    socket.connect('tcp://' + interface + ':' + port)
    print(f'Command listener subscribed to port {port} on interface {interface} ...')

    rate = 100 if args.rate is None else args.rate

    vel: list[float] = [0, 0] # store the wheel output state in [lv, rv]
    target: list[float] = [0, 0] # this is the target velocity we ramp to
    cmd = 'still' # current command. Should always be defined

    delta = period / rate # amount that the velocities will be stepped (constant ramp)

    lm, rm = Motor(4, 27), Motor(22, 23) # utility provided for GPIO PWM

    # Set the pwm frequencies to something higher than the default 100 Hz
    lm.forward_device.frequency = pwm_freq
    lm.backward_device.frequency = pwm_freq
    rm.forward_device.frequency = pwm_freq
    rm.backward_device.frequency = pwm_freq

    # Begin the control loop
    while True:
        try: # get any new commands
            cmd = socket.recv_string(flags=zmq.NOBLOCK).split(':')[1] # queue might be empty
            print(f'Got command: {cmd}')
        except zmq.Again:
            pass # don't have to do anything - cmd should retain its previous value

        target = targets[cmd]
        vel[0] = update_vel(vel[0], throttle * target[0], delta)
        vel[1] = update_vel(vel[1], throttle * target[1], delta)

        lm.value = vel[0]
        rm.value = vel[1]

        sleep(1 / rate)
