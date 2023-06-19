from periphery import Serial
import time

# Open /dev/ttyUSB0 with baudrate 115200, and defaults of 8N1, no flow control
serial = Serial(
        "/dev/ttyS3",
        baudrate=115200,
        databits=8,
        parity="none",
        stopbits=1,
        xonxoff=False,
        rtscts=False,
    )

list=[  0xA8, # 帧头                                 0
      
        0x00, # 人形 跟踪 模型                        1
        0x00, # 手势 状态 模型                        2
        0x00, # 人脸 状态 模型                        3
        0x00, # 火焰 状态 模型                        4

        0x01, # 人体 x 坐标 高8     （400， 200）     5
        0x90, # 人体 x 坐标 低8                       6
        0x00, # 人体 Y 坐标 高8                       7
        0xC8, # 人体 Y 坐标 低8                       8

        0x00, # 手势 状态                             9
        0x00, # 人脸 状态                             10
        0x00, # 火焰 状态                             11
        
        0x01, # 客厅 灯                               12
        0x00, # 门口 灯                               13
        0x00, # 卧室 灯                               14
        0x00, # 大门                                  15 
        
        0x11, # 数据包总长度                           16
        0xA9] # 帧尾                                  17

def uartThread(ary, ser_data):
    cnt = 0
    ary[:] = list[:]
    while True:
        list[:] = ary[:]
        serial.write(list)

        # Read up to 128 bytes with 50ms timeout
        buf = serial.read(128, 0.05)
        if buf:
            l = len(buf)
            
            for i in range(0, l):
                
                print(hex(buf[i]))

        if cnt > 10:
            cnt = 0
            print("list 0 is ", ary[0])
            print("人形 list 1 is ", ary[1]) # 人形 跟踪 模型 
            print("手势 list 2 is ", ary[2]) # 手势 状态 模型
            print("人脸 list 3 is ", ary[3]) # 人脸 状态 模型
            print("火焰 list 4 is ", ary[4]) # 火焰 状态 模型
            

            print("手势数据 list 9 is ", ary[9])   # 手势 
            print("人脸数据 list 10 is ", ary[10]) # 人脸
            print("火焰数据 list 11 is ", ary[11]) # 火焰

            print("客厅灯 list 12 is ", ary[12]) # 客厅
            print("门口 list 13 is ", ary[13]) # 门口
            print("卧室 list 14 is ", ary[14]) # 卧室
            print("大门 list 15 is ", ary[15]) # 大门            
        else:
            cnt = cnt + 1
        # print("list 5 is ", ary[5]) # 人体 x 坐标 高8
        # print("list 6 is ", ary[6]) # 人体 x 坐标 低
        # print("list 7 is ", ary[7]) # 人体 Y 坐标 高8
        # print("list 8 is ", ary[8]) # 人体 Y 坐标 低8 

        # print("ges list 9 is ", ary[9])
        # print("fire list 9 is ", ary[11])
        
        # print("list 0 is ", ary[0])

        # if buf:
        #     l = len(buf)
        #     for i in range(0, l):
        #         print(hex(buf[i]))
                
        
        time.sleep(0.1)
    serial.close()