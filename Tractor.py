import socket
import hashlib
import multiprocessing
import time
from tools import *


class Tractor():

    def __init__(self, port=5555, MaxConnect=10):
        """
            初始化函数，会根据参数建立socket连接。并设置侦听数量，但是要获得连接，使用recv函数
            port=5555:指定端口用于连接
            MaxConnect=5:指定最大连接数 
        """
        self.port = port
        self.serverSocket = socket.socket()
        self.serverSocket.bind(('localhost', port))
        self.serverSocket.listen(MaxConnect)
        # 空字典。resourceName --> ip set
        # 保存资源与IP之间的关系
        self.resourceMap = {}
        # 保存存活ip
        self.live = set()

    def recv(self):
        """
            接受函数。。。
            无参数
            接受连接，并建立相应的线程处理连接。
            线程函数为handle
        """
        while True:
            conn, addr = self.serverSocket.accept()
            p = multiprocessing.Process(target=self.handle, args=(conn, addr,))
            p.start()

    def handle(self, conn, addr):
        """
            处理函数，处理客户端的资源请求与响应
            conn:连接套接字
            addr:客户端地址
        """

        # 期待从peer获得资源信息。

        #以下是过程描述
        #Peer: HAVE MESSIZE MSG
        #Tractor: HAVE OK

        #将客户端的地址加入存活列表，
        #TODO 这是否有必要？ BY littledarren
        self.live.add(addr)

        #获取头部信息
        header = getHeader(conn)
        print(header)
        if header[0:4] == 'HAVE':
            # OK
            msgSize = int(header[5:])
            data = [0 for x in range(msgSize)]
            readNbytes(conn, data, msgSize)
            # 获取得到的资源信息(文件名,文件名)
            msg = bytes(data).decode()
            fileList = msg.split(",")
            #保存资源与ip的映射关系
            for fileName in fileList:
                if fileName not in self.resourceMap:
                    self.resourceMap[fileName] = set()
                self.resourceMap[fileName].add(addr)
            #发送头部信息
            header = 'HAVE OK'.encode('utf8')
            padding = [32 for x in range(HEADER_SIZE - len(header))]
            self.serverSocket.sendall(header)
            self.serverSocket.sendall(padding)
        else:
            #应该不可能吧
            pass
        #至此，客户端只会向跟踪服务器请求资源信息。

        #阻塞于此。
        while True:
            header = getHeader(conn)
            self.EXEComm(header)
    
    def replySHOW(self):
        """
            处理客户端SHOW的请求(下面的并非参数)
            client: SHOW
            Tractor:SHOW OK fileName, fileName
        """
        #返回一个资源列表(文件名,文件名)
        send_data = ','.join(list(self.resourceMap.keys())).encode('utf8')
        header = ('SHOW OK ' + str(len(send_data))).encode('utf8')
        padding = padding = [32 for x in range(HEADER_SIZE - len(header))]
        self.serverSocket.sendall(header)
        self.serverSocket.sendall(padding)
        self.serverSocket.sendall(send_data)

    def EXEComm(self, header):

        if header[:4] == 'SHOW':
            self.replySHOW()
        elif header[:3] == 'GET'
        
                



            


if __name__ == '__main__':
    t = Tractor()
    t.recv()
    pass


# m2 = hashlib.md5()
# m2.update(src)
# print m2.hexdigest()
