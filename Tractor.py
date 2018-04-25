import socket
import hashlib
import multiprocessing
import time

HEADER_SIZE= 32

#从连接读取指定长度的数据
def readNbytes(conn, data, size):
    count = 0
    while count != size:
        buffer = conn.recv(size - count)
        # for i in range(count, count + len(buffer)):
        #     data[i] = buffer[i - count]
        #切片有神奇的膜法。。。
        data[count:count + len(buffer)] = buffer

        count += len(buffer)



class Tractor():
    def __init__(self, port = 5555, MaxConnect = 5):
        self.port = port
        self.serverSocket = socket.socket()
        self.serverSocket.bind(('localhost', port)) 
        self.serverSocket.listen(MaxConnect)
        #空字典。resourceName --> ip set    
        self.resourceMap = {}
        #存活ip-->port
        self.live = {}

    def recv(self):
        while True:
            conn, addr = self.serverSocket.accept()
            p = multiprocessing.Process(target = self.handle, args = (conn, addr,))
            p.start()

    def handle(self, conn, addr):
        #期待从peer获得资源信息。
        #报头定义为32字节。
        #HAVE MESSIZE MSG
        data = [0 for x in range(HEADER_SIZE)]
        readNbytes(conn, data, HEADER_SIZE)
        header = bytes(data).decode()
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
                print(conn.getpeername())


            


    



if __name__ == '__main__':
    t = Tractor()
    t.recv()
    pass



# m2 = hashlib.md5()   
# m2.update(src)   
# print m2.hexdigest()   