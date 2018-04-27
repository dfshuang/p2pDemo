import socket
import os
from tools import *
import time


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

        #并行？一直等待？
        self.Psock = socket.socket()
        self.Psock.bind(('localhost', peerPort))

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

        #发送get filename请求
        header = "GET " + filename
        header = header.encode('utf8')
        padding = [32 for x in range(HEADER_SIZE - len(header))]
    
        self.Tsock.sendall(header)
        self.Tsock.sendall(bytes(padding))

        #获取有相关文件的peer信息
        header = getHeader(self.Tsock)
        headerSplit = header.split(' ')
        if headerSplit[1] == 'OK':
            print(headerSplit[0] + ' ' + headerSplit[1])
            msgsize = int(headerSplit[2])
            filelen = int(headerSplit[3])

            data = [0 for x in range(msgSize)]
            readNbytes(conn, data, msgSize)
            print(data)
            # 获取相应的文件的其余对等方ip地址
            #msg假如为元组的列表
            msg = bytes(data).decode()
            ipPortList = msg
            #平均每个peer传输ave_len行
            ave_len = filelen/len(ipList) + 1

            #在本地新建文件，输入文件名
            newFilePath = str(input("Please input the new file name: "))
            with open(newFilePath,'a') as fw:
                for i in range(len(ipPortList)):
                    ip, port = ipPortList[i]
                    strw = '' #存储要写进文件的字符串
                    #新建一个套接字，连接peer的Psock
                    self.Csock = socket.socket()
                    self.Csock.connect((ip, port))
                    header = "FLIE " + str(i * ave_len) + ' ' + str(ave_len)
                    for linenum in range(ave_len):
                        strw = str(self.Csock.recv(1024), encoding = 'utf8')
                        print(strw)
                        #最后的对等方传输文件结束时发送'END'
                        if strw == 'END':
                            print(strw)
                            break
                        else:
                            fw.write(strw)
        else:
            print('ERROR TO GET FILE')

        pass


    def sendFile(self, filename, linelen, firstline):
        """
        peer传输文件给另一个peer
        filename: str, 要传输的文件名
        linelen: int, 要传输的行数
        firstline: int, 要传输的第一行
        """
        #接收文件的peer的ip和port，下面语句用于监听
        conn, port = self.Psock.accept()
        if os.path.exists(filename):
            with open(filename, 'r') as fr:
                rlines = fr.readlines()  #一个字符串的list
                if(len(rlines) <= firstline + linelen):
                    #最后传输完成,传了[firstline, len(rlines)-1]，传'END'
                    for index in range(firstline, len(rlines)):
                        conn.sendall(bytes(rlines[index], encoding='utf8'))
                        print(rlines[index])
                    #防止粘包
                    time.sleep(2)
                    conn.sendall(bytes("END",encoding='utf8'))
                    print("END")
                else:
                    #没传输完成，传了[firstline, firstline+linelen-1]
                    for index in range(firstline, firstline+linelen):
                        conn.sendall(bytes(rlines[index], encoding='utf8'))
                        print(rlines[index])

        else:
            print("can't find the file")

    #展示所有的可下载文件
    def show(self):
        header = 'SHOW'.encode('utf8')
        padding = [32 for x in range(HEADER_SIZE - len(header))]
        self.Tsock.sendall(header)
        self.Tsock.sendall(padding)

        pass
        

    def EXEComm(self, comm):
        """
            先开两个线程，一个用于监听peer的请求，
            另一个用于和tractor交流
            执行命令的函数
            命令如SHOW,GET fileName
        """
        #先开监听的线程

        #输入并执行命令
        while(1):
            cmdLine = str(input(">>> "))
            if cmdLine == 'help':
                print("help")
            elif cmdLine == 'show':
                show()
            elif cmdLine[:3] == 'get':
                getFile(cmdLine[4:])
                


if __name__ == '__main__':
    c = Client()
    c.EXEComm()