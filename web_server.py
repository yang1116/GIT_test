"""
web server服务
"""
import os
from socket import *
from select import select


class WebServer():
    def __init__(self, host="", port=88, html=None):
        self.host = host
        self.port = port
        self.address = (host, port)
        self.html = html
        self._rlist = []  # 读时间存储
        self.sock = self._create_socket()

    # 2. 执行start之前做好准备工作,创建tcp套接字
    def _create_socket(self):
        sock = socket()
        sock.bind(self.address)
        sock.setblocking(False)
        return sock

    # 启动整个服务
    def start(self):
        self.sock.listen(5)
        print("Listen the port %d" % self.port)
        # 3.搭建IO多路复用模型
        self._rlist = [self.sock]
        # 循环监控浏览器请求(连接，http请求)
        while True:
            rs, ws, xs = select(self._rlist, [], [])
            for r in rs:
                if r is self.sock:
                    # 处理浏览器连接
                    self._connect()
                else:
                    # 处理浏览器请求
                    try:
                        self._handle(r)
                    except Exception as e:
                        print(e)
                    finally:
                        self._rlist.remove(r)
                        r.close()

    def _connect(self):
        connfd, addr = self.sock.accept()  # 套接字是实例变量，所以不用传参了
        connfd.setblocking(False)
        self._rlist.append(connfd)

    def _handle(self, connfd):
        # 接收浏览器http请求
        request = connfd.recv(1024)
        if not request:
            raise Exception
        info = request.decode().split(" ")[1]
        print("请求内容：", info)
        # 发送响应
        self._send_response(connfd, info)

    def _send_response(self, connfd, info):
        if info == "/":
            html_name = "/index.html"
        else:
            html_name = info

        # 组织http响应格式
        try:
            file = open(self.html + html_name, "rb")
        except Exception:
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            with open(self.html + "/404.html", "rb") as f:
                data = f.read()
        else:
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            data = file.read()
        finally:
            response = response.encode() + data
            connfd.send(response)  # 发送给浏览器


if __name__ == '__main__':
    # 1. 类的基本使用方式
    httpfd = WebServer("0.0.0.0", 8888, "./static")
    httpfd.start()
