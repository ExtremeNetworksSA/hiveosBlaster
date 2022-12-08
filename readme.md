# Hive OS Blaster
## hiveOSBlaster.py
### Purpose
This script with take a list of device IP Addresses or DNS names and a list of commands. An ssh session will be opened with each device and then run each of the commands in the command list. A log file will be created in a log directory for each device and the responses for each of the commands will be appended to the file.

### How it works
As soon as the ssh session is opened with the device, the script will log in using the provided credentials and run the 'console page 0' command. This will allow any command you add to the command file to get the full response.
This script will open ssh sessions in batches of 50 devices. Once the commands are sent and responses logged the sessions will close. Once all 50 sessions are closed the next batch will start. </b>
Multiple commands can be added to the cmd file. The script will run 1 command at a time and pause for a response. After the defined pause the script will run the next command. 
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
 - You can adjust the batch size if needed 
    >**default is 50 devices at a time*
    ###### line 89
    ```
    sizeofbatch = 50
    ```
- You can adjust the time between commands being sent
    >*default is 4 seconds between commands*
    >>**Note:** a longer time is needed for commands that take longer to run the full response - *ie* show running-config
    ###### line 69
    ```
    time.sleep(4)
    ```

### Outputs
#### log file 
A log file will be created in the log directory with the device's name pulled from the cli prompt as the filename. If a log file already exists for that device the output will be appended to the existing file. The command sent and all outputs from the commands will be added to the log file.
```
ap-100.log
```
>**Note:** if devices have the same name in prompt they will be added to the same log file. This can be changed by adjusting the name creation for the log file.

-
    ###### Line 74 Change
    ```
    file = open(PATH+"/log/"+apname+".log", 'a')
    ```
    ###### to
    ```
    file = open(PATH+"/log/"+device+".log", 'a')
    ```



## Running the Script
#### make script executable
```
chmod +x hiveOSBlaster.py
```
#### entering the device and cmd files
When running the script from terminal after entering the script name add the name of the device file and then the name of the command file
```
./hiveOSBlaster.py APs.txt cmd.txt
```

### Requirements
Python 3.6 or higher is recommended for this script.
The python paramiko module will need to be installed. If pip is installed, this can be done with 'pip install paramiko'. 
The needed modules are listed in the requirements.txt file and can be installed from there.