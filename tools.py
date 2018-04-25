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
#进一步封装，获取头部字符串
def getHeader(conn, size = HEADER_SIZE):
    data = [0 for x in range(size)]
    readNbytes(conn, data, size)
    header = bytes(data).decode()
    return header


HEADER_SIZE= 32