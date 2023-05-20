#!coding=utf-8
import sys
import math
import threading
import socket
import struct


def socket_service(ip="192.168.4.3", point=8000):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定 IP point
        s.bind((ip, point))
        # 设置监听数
        s.listen(10)
    except socket.error as msg:
        print (msg)
        sys.exit()
    
    while True:
        print ('Waiting connection...')
        conn, addr = s.accept()
        print ('Accept new connection from IP: {0}'.format(addr[0]))
        conn.settimeout(500)
        conn.send('Server connection is OK!'.encode('utf-8'))
    
        while True:
            fileinfo_size = struct.calcsize('128sl')
            buf = conn.recv(fileinfo_size)
            # 判断是否接收到文件头信息
            if buf:
                filename, filesize = struct.unpack('128sl', buf)
                fn = filename.strip(b'\00')
                fn = fn.decode("utf-8")
                print ('===> The file name: {0}, and file size: {1} Mb.'.format(str(fn), math.ceil(filesize/(1024**2))))
    
                recvd_size = 0  # 定义已接收文件的大小
                # 存储位置
                fp = open('nuomi/data/' + str(fn), 'wb')
                print ('===> Start receiving!')
                # 将分批次传输的二进制流依次写入到文件
                while not recvd_size == filesize:
                    if filesize - recvd_size > 1024:
                        data = conn.recv(1024)
                        recvd_size += len(data)
                    else:
                        data = conn.recv(filesize - recvd_size)
                        recvd_size = filesize
                    fp.write(data)
                fp.close()
                print ('===> End receive!')
            conn.close()
            break


if __name__ == "__main__":
    t = threading.Thread(target=socket_service)
    t.start()
