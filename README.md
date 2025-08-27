## About

Code to run on the robot (Raspberry Pi). Designed to work with the [remote server code](https://github.com/tplaysted/integrated-server).

## Usage

### Create virtual environment
After cloning the repository to the raspberry pi, create a [virtual environment](https://docs.python.org/3/library/venv.html) in the installation folder. This is a necessary step as the launch script assumes there is a virtual environment in the installation folder. Make sure to create this virutal environment using system packages with `python -m venv --system-site-packages <env>`, otherwise gpio dependencies will be missing. You can use the following shell commands: 
```bash
$ mkdir .venv && cd .venv
$ python -m venv --system-site-packages .
$ source bin/activate
$ cd .. && pip install -r requirements.txt
```

### Start the pigpio daemon
Due to an [issue with the default gpio library](https://github.com/gpiozero/gpiozero/issues/1209#issue-3341416358), servo.py must use pigpio to manage the servo pwm signal. This library requires the pigpio daemon to be running in the background. Do this with a crontab as [per this forum post](https://forums.raspberrypi.com/viewtopic.php?f=32&t=103752#p717150). Note the binary may be located in `/usr/bin/` and not `/usr/local/bin`.

### Command listener
Run `./launch.sh <IP>` to start both the servo and motor control processes listening to the host IP. You may need to allow execute permissions with `sudo chmod +x launch.sh`. Run `arp -a` to check the server address. For example if the key publisher is running on `192.168.50.123`, do `./launch.sh 192.168.50.123`.
