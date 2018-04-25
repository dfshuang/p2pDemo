import socket
import os
from tools import *


class Client():
    def __init__(self, tractorAddr = 'localhost', tractorPort = 5555, peerPort = 6666, MaxConnect = 10):
        """
            初始化函数，会向服务器发送自己的资源信息
            tractorAddr = 'localhost':指定Tractor的地址
            tractorPort = 5555：指定tractor的端口
            peerPort = 6666：用于其他peer连接的端口
            MaxConnect = 10：最大连接数。即最多被这么多个对等方请求文件
        """
        self.dir = os.getcwd()
        self.Tsock = socket.socket()
        self.Tsock.connect((tractorAddr, tractorPort))

        self.Psock = socket.socket()
        self.Psock.bind('localhost', peerPort)
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
        #以下是过程描述
        #Peer: HAVE MESSIZE MSG
        #Tractor: HAVE OK
        #接受回复

        header = getHeader(self.Tsock)
        if header[:7] == 'HAVE OK':
            print(header[:7])
        else:
            print('ERROR INITIALIZATION')

    def getFile(self, fileName):
        """
            获取文件，从跟踪器上获取所有的资源ip，然后连接上获取文件。
        """
        pass

    #展示所有的可下载文件
    def show(self):
        header = 'SHOW'.encode('utf8')
        padding = [32 for x in range(HEADER_SIZE - len(header))]
        self.Tsock.sendall(header)
        self.Tsock.sendall(padding)


        
        pass
    def EXEComm(self, comm):
        """
            执行命令的函数
            命令如SHOW,GET fileName
        """


if __name__ == '__main__':
    c = Client()