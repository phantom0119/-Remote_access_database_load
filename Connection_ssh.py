"""
Connect to Ubuntu using the SSH Protocol.
The purpose is to obtain the ID and PW of the Mysql server.

1. Connect to an Ubuntu server via SSH.
2. Run the shell script on Ubuntu Server to register environment variables.
  --> The shell script is set with permissions so that the 'pcb' account can execute.
  --> Environment variables are ID and PW of MySQL Server.
3. After obtaining the ID and PW values, close the SSH session and return values.
"""

import os
import sys
import paramiko  # pip install paramiko




def connect_ssh(hname, hport, husername, hpassword):
    SSH = paramiko.SSHClient()  # Object of SSH Client
    mysqlid = None  #Mysql Server login ID
    mysqlpw = None  #PW
    status  = None  #Connection Code (200:OK, 400:Command Error, 500:Internal Server Error)
    HOST_KEY = r'C:\Users\phant\.ssh\known_hosts'   #Host key Path in windows
    
    # Automatic Host key registration
    #SSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Load the server's host key
    # Add key to the ssh object for verification
    SSH.load_host_keys(HOST_KEY)
    
    # Reject untrusted hosts
    SSH.set_missing_host_key_policy(paramiko.RejectPolicy())
    
    try :
        # Connect to SSH Server
        SSH.connect(hostname=hname, 
                    port=hport, 
                    username=husername,
                    password=hpassword)
        
        ##########################################################
        #  - DANGER -  
        # Sessions are different for each "exec_command" call.
        # So, must get the result in a single command.
        ###########################################################
        # Get MySQL Login ID and PW
        COMMAND = "source ~/working/set_mysql_env.sh && env"
        
        stdin, stdout, stderr = SSH.exec_command(COMMAND)
        
        
        output = stdout.read().decode().strip()
        errors = stderr.read().decode().strip()
        
        if errors:
            sys.stdout.write(f"Error: {errors}\n")
            status = '400'
        else:
            #sys.stdout.write(f"Result of command\n{output}")
            for line in output.splitlines():
                if line.startswith('MYSQL_ID='):
                    mysqlid = line.split('=')[1]
                elif line.startswith('MYSQL_PW='):
                    mysqlpw = line.split('=')[1]
            status = '200'
                    
    except Exception as e :
        sys.stdout.write(f"Connection Fail.\nError:{e}")
        status = '500'
        
    finally :
        SSH.close()
        return status, mysqlid, mysqlpw



def get_ssh_password():
    """
    get Ubuntu Server Login password from Windows environment variables.
    Return : Password of Ubuntu Server
    """
    pw = os.getenv('ssh_pw')
    return pw


def get_ssh_info() :
    """
    get Ubuntu Server access infomation.
    Return : Dictionary format
     1. Login ID    ->  key = 'ID' 
     2. IP Address  ->  key = 'IP'
     3. Access Port ->  key = 'PORT'
    """
    info = {'ID':'pcb', 'IP':'192.168.3.4', 'PORT':22}
    return info




if __name__ == "__main__" :
    #1 get ssh password from Environment Variable.
    ssh_pw = os.getenv('ssh_pw')

    #2 branch: not found password = exit.
    if ssh_pw == None:
        sys.stdout.write("SSH Password is not found..! Check again.\n")
        exit()
    else:
        sys.stdout.write("SSH password is found.\n")
        HOST_NAME = '192.168.3.4'
        PORT = 22
        USERNAME = 'pcb'
        PASSWORD = ssh_pw

        status, mysqlid, mysqlpw = connect_ssh(HOST_NAME, PORT, USERNAME, PASSWORD)
        
        print(status, mysqlid, mysqlpw)
    
    
    

