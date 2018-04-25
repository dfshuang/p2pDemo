import socket
import os

HEADER_SIZE= 32

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

if __name__ == '__main__':
    c = Client()