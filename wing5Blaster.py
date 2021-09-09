#!/usr/bin/env python3
import sys	
import time
import argparse
import os
import multiprocessing
import time
import socket
import paramiko

from paramiko.ssh_exception import AuthenticationException, SSHException, BadHostKeyException

PATH = os.path.dirname(os.path.abspath(__file__))


today = time.strftime("%m_%d_%Y %H:%M:%S")

parser = argparse.ArgumentParser() 

parser.add_argument('ipfile')
parser.add_argument('cmdfile')
args = parser.parse_args()

ipfile = "{0}".format(args.ipfile)
cmdfile = "{0}".format(args.cmdfile)

# Device Credentials
user = 'admin'
passwd = 'c0bra42b'

if not os.path.isdir(PATH+'/log'):
    os.makedirs(PATH+'/log')


def ap_ssh(ip,cmds, device, mp_queue):

    success = 0 
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        #print ("Establishing Connection with ",ip)
        ssh.connect(ip,username = user , password = passwd, timeout=10)
        chan = ssh.invoke_shell()
    except AuthenticationException:
        print("Authentication failed on " + device + ", please verify your credentials: %s")
        sys.stdout.flush()
    except SSHException as sshException:
        print("Unable to establish SSH connection on " + device + ": %s" % sshException)
        sys.stdout.flush()
    except BadHostKeyException as badHostKeyException:
        print("Unable to verify server's host key on " + device + ": %s" % badHostKeyException)
        sys.stdout.flush()
    except Exception as e:
        print("Operation error on " + device + ": %s" % e)
        sys.stdout.flush()
    else:
        outputs = []
        time.sleep(1)
        resp = chan.recv(9999)	
        chan.send('enable\n')
        time.sleep(1)
        resp = chan.recv(9999)
        lines = resp.splitlines()
        apname = lines[-1][:-1]
        chan.send('no page\n')
        time.sleep(1)
        resp = chan.recv(9999)

        for cmd in cmds:
            sys.stdout.flush()
            chan.sendall(cmd + '\n')
            time.sleep(4)
            if chan.recv_ready():
                change = chan.recv(9999)
                outputs += (change.decode('ascii','ignore').splitlines())
            outputs = outputs[:-1]
        devicename = device.split(".")[0]
        file = open(PATH+"/log/"+devicename+".log", 'a')
        file.write("*******************************\n" + device + "("+ip+")\n"+today+"\n*******************************\n\n")
        for line in outputs:
        	file.write(line+'\n')
        file.write("\n\n")
        file.close()
    ssh.close()

def main():
    with open(ipfile, 'r') as f:
    	ips = f.read().splitlines()
    with open(cmdfile, 'r') as f:
    	cmds = f.read().splitlines()


    sizeofbatch = 50
    for i in range(0, len(ips), sizeofbatch):
        batch = ips[i:i+sizeofbatch]
        NONE = ''
        mp_queue = multiprocessing.Queue()
        processes = []
        for device in batch:
            a = device.split('.')
            if len(a) != 4:
                try:
                    ip = socket.gethostbyname(device)
    
                except socket.gaierror:
                    print ("cannot resolve hostname: ", device	)
                    continue	
            else:
                ip = device
                dns = socket.gethostbyaddr(ip)
                device = dns[0]
            try:
                print("connecting to", device)
                socket.inet_aton(ip)
                p = multiprocessing.Process(target=ap_ssh,args=(ip,cmds, device,mp_queue))
                processes.append(p)
                p.start()
            except socket.error:
                print(device + " ("+ip+") - Failed to connect")
        for p in processes:
            try:
                p.join()
                p.terminate()
            except:
                print("error occured in thread")
        mp_queue.put('STOP')
        


if __name__ == '__main__':
    main()
