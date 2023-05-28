#!coding=utf-8
import socket
import os
import sys
import struct
import math

from publish_rtsp import FfmpegPublishRtsp




  

class Server:
    def __init__(self, ip="192.168.4.15", point=8000):
        self.ip = ip
        self.point = point
        self.open_server()
    def run(self):
        self.open_server()
        while True:
            self.listen_connection()
            self.optional_key = self.receive_message()
            print("optional_key: ", self.optional_key)

            # if optional_key == "mystream_0":
            #     self.conn.send("True".encode("utf-8"))
            #     publish_ffmpeg_frame = FfmpegPublishRtsp(urlrtsp=self.ip, portrtsp=8554, streamrtsp=optional_key)
            #     publish_ffmpeg_frame.run(img)
            # else:
            #     print("Client send message is False!!!")
            #     continue

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


# server = Server("192.168.4.15", 8000)
# # server processing

#-------------------- sysFlag ------------------#
            # | bit 15- 8  | bit 7-0   |
            # | Model      | camare    |   
            # | 0000 0000  | 0000 0000 |
            # now using
            #
            # Camera
            # bit 0  ->  Car_Manager    camId:0
            # bit 1  ->  Door           camId:2
            # bit 2  ->  Kitchen
            #
            # Model
            # bit 8  ->  yolov5         human_track
            # bit 9  ->  retinaface     face_detec


SYS_FLAG_ON = 1
SYS_FLAG_OFF = 0

SYS_FLAG_BIT_CAM0 = 0
SYS_FLAG_BIT_CAM1 = 1
SYS_FLAG_BIT_CAM2 = 2

SYS_FLAG_BIT_MODEL_HUM = 8
SYS_FLAG_BIT_MODEL_FAC = 9
SYS_FLAG_BIT_MODEL_GES = 10
# system flag class
class SysFlag:
    def __init__(self, val=0x1):
        # 0000 0000| 0000 0001
        # Enable Cam0
        self.flag = val
        
    def match(self, str):

        # init
        if str == "mystream_0":        
            self.flag = 1

        # person track
        elif str == "ON_person_track":
            self.flag = 2
        elif str == "OFF_person_track":
            self.flag = 1

        # face
        elif str == "ON_face_detection":
            self.flag = 3
        elif str == "OFF_face_detection":
            self.flag = 1    
    
        
    def setBit(self, bit, val):
        if val:
            self.flag |= 1 << bit
        else:
            self.flag &= 0 << bit
        
sysCtl = SysFlag()




# server: server class
def server_thread(server, even, ser_data):
    
    server.listen_connection()
        
    server.optional_key = server.receive_message()
    
    print("optional_key:", server.optional_key)
    
    if server.optional_key == "Tell me your push rtsp stream address.":
        server.send_message("streamrtsp")
        print("send massage")
    even.set()

    while True:
        server.listen_connection()
        
        server.optional_key = server.receive_message()
        
        print("optional_key:", server.optional_key)
        server.conn.send("True".encode("utf-8"))

        sysCtl.match(server.optional_key)
        ser_data.value = sysCtl.flag 
        print("valus is ", sysCtl.flag)
        # 设置even
        even.set()
        


# if __name__ == "__main__":
#     # t = threading.Thread(target=socket_service)
#     # t.start()
#     server = Server()
#     server.run()
