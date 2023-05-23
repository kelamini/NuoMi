#!coding=utf-8
import socket
import os
import sys
import struct
import math


class Server:
    def __init__(self, ip="192.168.4.3", point=8000):
        self.ip = ip
        self.point = point
        
    def run(self):
        self.open_server()
        while True:
            self.listen_connection()
            optional_key = self.receive_message()
            # print("optional_key: ", optional_key)
            if optional_key == "d":
                # self.conn.send("d".encode("utf-8"))
                self.accept_file()
            else:
                print("Client send message is False!!!")
                continue

    def open_server(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # 绑定 IP point
            self.server.bind((self.ip, self.point))
            # 设置监听数
            self.server.listen(5)
        except socket.error as msg:
            print (msg)
            sys.exit()

    def listen_connection(self):
        print ('Waiting connection...')
        self.conn, self.addr = self.server.accept()
        print ('Accept new connection from IP: {0}'.format(self.addr[0]))
        self.conn.settimeout(500)
        # self.conn.send('Server connection is OK!'.encode('utf-8'))

    def close_server(self):
        self.server.close()

    def send_message(self, message):
        self.conn.send(message.encode('utf-8'))

    def receive_message(self):
        return self.conn.recv(1024).decode("utf-8")

    def accept_file(self):
        fileinfo_size = struct.calcsize('128sl')
        buf = self.conn.recv(fileinfo_size)
        # 判断是否接收到文件头信息
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.strip(b'\00')
            fn = fn.decode("utf-8")
            print ('===> The file name: {0}, and file size: {1} Mb.'.format(str(fn), math.ceil(filesize/(1024**2))))

            recvd_size = 0  # 定义已接收文件的大小
            # 存储位置
            fp = open('orangepi/data' + str(fn), 'wb')
            print ('===> Start receiving!')
            # 将分批次传输的二进制流依次写入到文件
            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = self.conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = self.conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print ('===> End receive!')
        self.conn.close()  


class Client:
    def __init__(self, ip="192.168.4.3", point=8000):
        self.ip = ip
        self.point = point
    
    def run(self):
        while True:
            self.open_client()
            optional_key = input("Input you optional(load file:'d'): ")
            if optional_key == "d":
                self.send_message(optional_key)
                self.send_file()
            elif optional_key == "q":
                self.close_client()
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

    def send_message(self, message):
        self.client.send(message.encode("utf-8"))

    def receive_message(self):
        return self.client.recv(1204).decode("utf-8")

    def send_file(self, filepath):
        if os.path.isfile(filepath):
            # fileinfo_size = struct.calcsize('128sl')
            fhead = struct.pack('128sl', os.path.basename(filepath).encode('utf-8'), os.stat(filepath).st_size)
            self.client.send(fhead)

            fp = open(self.filepath, 'rb')
            while True:
                data = fp.read(1024)
                if not data:
                    print ('===> This file of {0} send over.'.format(os.path.basename(filepath)))
                    break
                self.client.send(data)
    
    def close_client(self):
        self.client.close()


if __name__ == "__main__":
    # t = threading.Thread(target=socket_service)
    # t.start()
    server = Server()
    server.run()
