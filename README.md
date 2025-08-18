## About

Code to run on the robot (Raspberry Pi). Designed to work with the [remote server code](https://github.com/tplaysted/integrated-server).

## Usage
After cloning the repository to the raspberry pi, create a [virtual environment](https://docs.python.org/3/library/venv.html) in the installation folder. Make sure to create this virutal environment using system packages with `python -m venv --system-site-packages <env>`, otherwise gpio dependencies will be missing. After activating the environment, get dependencies with `pip install -r requirements.txt`.

### Command listener
Run `python cmd_sub.py` to start the command listener. Use `-i` to specify the interface. Run `arp -a` first to check the server address. For example if the key publisher is running on `192.168.50.123`, do `python cmd_sub.py -i 192.168.50.123`. The port can be set manually, but is recommended to leave the default. 
