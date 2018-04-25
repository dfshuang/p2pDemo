import socket
import hashlib
import multiprocessing
import time
from tools import *


class Tractor():
    def __init__(self, port = 5555, MaxConnect = 5):
        self.port = port
        self.serverSocket = socket.socket()
        self.serverSocket.bind(('localhost', port)) 
        self.serverSocket.listen(MaxConnect)
        #空字典。resourceName --> ip set    
        #保存资源与IP之间的关系
        self.resourceMap = {}
        #保存存活ip
        self.live = set()

    def recv(self):
        while True:
            conn, addr = self.serverSocket.accept()
            p = multiprocessing.Process(target = self.handle, args = (conn, addr,))
            p.start()

    def handle(self, conn, addr):
        #期待从peer获得资源信息。
        #报头定义为32字节。
        #HAVE MESSIZE MSG
        self.live.add(addr)
        header = getHeader(conn)
        print(header)
        if header[0:4] == 'HAVE':
            #OK
            msgSize = int(header[5:])
            data = [0 for x in range(msgSize)]
            readNbytes(conn, data, msgSize)
            #获取得到的资源信息(文件名,文件名)
            msg = bytes(data).decode()
            fileList = msg.split(",")
            for fileName in fileList:
                if fileName not in self.resourceMap:
                    self.resourceMap[fileName] = set()
                self.resourceMap[fileName].add(addr)
        


            


    



if __name__ == '__main__':
    t = Tractor()
    t.recv()
    pass



# m2 = hashlib.md5()   
# m2.update(src)   
# print m2.hexdigest()   