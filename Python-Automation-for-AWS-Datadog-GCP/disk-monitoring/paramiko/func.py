
import subprocess
import sys
sys.path.append('paramiko')
from lambda_function import *
from lambda_function import lambda_handler
import paramiko
import pysftp
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None


import socket
from ssh2.session import Session




def deploy(event, context):
        global hostname
        global kepair
        dicttt= lambda_handler(event, context)
        for k, v in dicttt.items():
                hostname =  k
                keypair =  v
                print(hostname)
                file = open("/tmp/id_rsa.pem","w+")
                file.write(v)
                file.close()
                p = subprocess.Popen(["ls", "-l", "/tmp/"], stdout=subprocess.PIPE)
                out, err = p.communicate()
                #print(out)
                redd = subprocess.Popen(["chmod", "644", "/tmp/id_rsa.pem"], stdout=subprocess.PIPE)
                out, err = redd.communicate()
                #print(out)
                #outpt = subprocess.Popen(["cat", "/tmp/id_rsa.pem"], stdout=subprocess.PIPE)
                #out, err = outpt.communicate()
                #print(out)
                copy()
                exect()

def copy():
        myHostname = hostname
        myUsername = "ubuntu"
        mykeyfile = "/tmp/id_rsa.pem"
        with pysftp.Connection(host=myHostname, username=myUsername, private_key=mykeyfile, cnopts=cnopts) as sftp:
                print("Connection succesfully stablished ... ")
                sftp.cwd('/tmp')
                sftp.put('paramiko/disk-alert.sh')
                sftp.put('paramiko/exect.sh')
        host = hostname
        user = 'ubuntu'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, 22))
        session = Session()
        session.handshake(sock)
        session.userauth_publickey_fromfile(user, '/tmp/id_rsa.pem')

        channel = session.open_session()
        channel.execute('chmod +x /tmp/disk-alert.sh')
        channel1 = session.open_session()
        channel1.execute('chmod +x /tmp/exect.sh')
        size, data = channel.read()
        while size > 0:
                print(data)
                size, data = channel.read()
        channel.close()
        print("Exit status: %s" % channel.get_exit_status())


def exect():
	import paramiko
	k = paramiko.RSAKey.from_private_key_file("/tmp/id_rsa.pem")
	c = paramiko.SSHClient()
	c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	print("connecting")
	c.connect( hostname = hostname, username = "ubuntu", pkey = k )
	print("connected")
	commands = [ "cd /tmp; ./exect.sh" ]
	for command in commands:
		print("Executing {}".format( command ))
		stdin , stdout, stderr = c.exec_command(command)
		print(stdout.read())
		print( "Errors")
		print(stderr.read())
		c.close()
