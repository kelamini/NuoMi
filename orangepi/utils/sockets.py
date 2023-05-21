#!coding=utf-8
import socket
import os
import sys
import struct


class Client:
    def __init__(self, file_path, ip="127.0.0.1", point=8000):
        self.ip = ip
        self.point = point
        self.filepath = file_path
    
    def run(self):
        while True:
            self.open_client()
            optional_key = input("Input you optional(load file:'d'): ")
            if optional_key == "d":
                self.client.send(optional_key.encode("utf-8"))
                self.send_file()
            elif optional_key == "q":
                self.client.close()
                break
            else:
                print("Your input is Error!!!")
                continue

    def open_client(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.ip, self.point))
        except socket.error as msg:
            print (msg)
            sys.exit(0)
        # print(self.client.recv(1024).decode("utf-8"))

    def send_file(self):
        if os.path.isfile(self.filepath):
            # fileinfo_size = struct.calcsize('128sl')
            fhead = struct.pack('128sl', os.path.basename(self.filepath).encode('utf-8'), os.stat(self.filepath).st_size)
            self.client.send(fhead)

            fp = open(self.filepath, 'rb')
            while True:
                data = fp.read(1024)
                if not data:
                    print ('===> This file of {0} send over.'.format(os.path.basename(self.filepath)))
                    break
                self.client.send(data)
            self.client.close()


if __name__ == '__main__':
    file_path = input("Input you will send file path: ")
    client = Client(file_path)
    client.run()
