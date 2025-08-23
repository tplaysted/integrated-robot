## About

Code to run on the robot (Raspberry Pi). Designed to work with the [remote server code](https://github.com/tplaysted/integrated-server).

## Usage
After cloning the repository to the raspberry pi, create a [virtual environment](https://docs.python.org/3/library/venv.html) in the installation folder. Make sure to create this virutal environment using system packages with `python -m venv --system-site-packages <env>`, otherwise gpio dependencies will be missing. After activating the environment, get dependencies with `pip install -r requirements.txt`.

Due to an [issue with the default gpio library](https://github.com/issues/created?issue=gpiozero%7Cgpiozero%7C1209), servo.py must use pigpio to manage the servo pwm signal. This library requires the pigpio daemon to be running in the background. Do this with a crontab as [per this forum post](https://forums.raspberrypi.com/viewtopic.php?f=32&t=103752#p717150). Note the binary may be located in `/usr/bin/` and not `/usr/local/bin`.
### Command listener
Run `python cmd_sub.py` to start the command listener. Use `-i` to specify the interface. Run `arp -a` first to check the server address. For example if the key publisher is running on `192.168.50.123`, do `python cmd_sub.py -i 192.168.50.123`. The port can be set manually, but is recommended to leave the default. 
