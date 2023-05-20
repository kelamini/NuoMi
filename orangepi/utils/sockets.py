#!coding=utf-8
import socket
import os
import sys
import struct


def socket_client(file_path, ip="127.0.0.1", point=8000):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, point))
    except socket.error as msg:
        print (msg)
        sys.exit(0)
    print(str(s.recv(1024)))

    filepath = file_path
    if os.path.isfile(filepath):
        # fileinfo_size = struct.calcsize('128sl')
        fhead = struct.pack('128sl', os.path.basename(filepath).encode('utf-8'), os.stat(filepath).st_size)
        s.send(fhead)

        fp = open(filepath, 'rb')
        while True:
            data = fp.read(1024)
            if not data:
                print ('===> This file of {0} send over.'.format(os.path.basename(filepath)))
                break
            s.send(data)
        s.close()

   
if __name__ == '__main__':
    file_path = input("Input you will send file path: ")
    socket_client(file_path)
