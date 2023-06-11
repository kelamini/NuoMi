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

list=[0xA8, # 帧头                                 0
      

      0x01, # 人体 x 坐标 高8     （400， 200）     1
      0x90, # 人体 x 坐标 低8                       2
      0x00, # 人体 Y 坐标 高8                       3
      0xC8, # 人体 Y 坐标 低8                       4
      0x00, # 手势 状态                             5
      0x00, # 人脸 状态                             6
      0x00, # 火焰 状态                             7
      0x01, # 客厅 灯                               8
      0x00, # 门口 灯                               9
      0x00, # 卧室 灯                               10
      0x00, # 大门                                  11
      0x03, # 车                                    12  
    
      0x0E, # 数据总长度                            13
      0xA9] # 帧尾                                  14

def uartThread(val):


    while True:
        
        serial.write(list)

        # Read up to 128 bytes with 50ms timeout
        # buf = serial.read(128, 0.05)
    
        # 手势
        list[5] = val.value
        # print("value is", val.value)
        # print("list 5 is ", list[5])
        # if buf:
        #     l = len(buf)
        #     for i in range(0, l):
        #         print(hex(buf[i]))
                
        
        # print("read {:d} bytes: _{:s}_".format(len(buf), buf))
        time.sleep(0.1)
    serial.close()