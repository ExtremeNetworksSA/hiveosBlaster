# Hive OS Blaster
## hiveOSBlaster.py
### Purpose
This script with take a list of device IP Addresses or DNS names and a list of commands. An ssh session will be opened with each device and then run each of the commands in the command list. A log file will be created in a log directory for each device and the responses for each of the commands will be appended to the file.

### User Input
A text file will need to be created listing the ip addresses or dns names of the devices.
A text file will need to be created listing the commands to be ran on each of the devices.
In the script, the device credentials will need to be updated
###### lines 27-29
```
# Device Credentials
user = 'admin'
passwd = '****'
```

### Outputs
#### log file 
A log file will be created in the log directory with the device's name as the filename. If a log file already exists for that device the output will be appended to the existing file. The command sent and all outputs from the commands will be added to the log file.
```
ap-100.log
```

## Running the Script
#### entering the device and cmd files
When running the script from terminal after entering the script name add the name of the device file and then the name of the command file
```
./hiveOSBlaster.py APs.txt cmd.txt
```

### Requirements
Python 3.6 or higher is recommended for this script.
The python paramiko module will need to be installed. If pip is installed, this can be done with 'pip install paramiko'. 
The needed modules are listed in the requirements.txt file and can be installed from there.