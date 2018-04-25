import socket
import os
from tools import *


class Client():
    def __init__(self, tractorAddr = 'localhost', tractorPort = 5555):
        self.dir = os.getcwd()
        self.Tsock = socket.socket()
        self.Tsock.connect((tractorAddr, tractorPort))
        send_data = ','.join(os.listdir(self.dir))
        print(send_data)
        send_data = send_data.encode('utf8')
        msg_size = len(send_data)
        header = "HAVE " + str(msg_size) + " "
        
        print(header)
        header = header.encode('utf8')
        #使用空格填充。。
        padding = [32 for x in range(HEADER_SIZE - len(header))]
        self.Tsock.sendall(header)
        self.Tsock.sendall(bytes(padding))
        self.Tsock.sendall(send_data)
    def getFile(self, fileName):
        pass

    #展示所有的可下载文件
    def ls(self):
        header = 'SHOW'.encode('utf8')
        padding = [32 for x in range(HEADER_SIZE - len(header))]
        self.Tsock.sendall(header)
        self.Tsock.sendall(padding)


        
        pass


if __name__ == '__main__':
    c = Client()