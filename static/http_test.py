"""
http协议
"""
from socket import *


def handle(connfd):
    # 接收http请求内容
    request = connfd.recv(1024)
    print(request.decode())
    # 给浏览器回信，因为不符合响应格式，所以浏览器无法显示(火狐浏览器除外)
    # response = """HTTP/1.1 200 OK
    # Content-Type:text/html
    #
    # hello world
    # """

    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type:image/html\r\n"
    response += "\r\n"
    with open("../02_MULTITASKING/1.jpg", "rb") as f:
        data = f.read()
    response = response.encode() + data
    connfd.send(response)


def main():
    sock = socket()
    sock.bind(("0.0.0.0", 8887))
    sock.listen(5)
    while True:
        # 接收服务器的连接
        connfd, addr = sock.accept()
        print("Connect from", addr)
        # 处理浏览器请求
        handle(connfd)
        connfd.close()
    sock.close()


if __name__ == '__main__':
    main()
