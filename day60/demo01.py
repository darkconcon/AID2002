"""

    http server 2.0

    python

    HTTPServer v2.0
    功能：
    1. 接收客户端(浏览器)请求
    2. 解析客户端发送的请求 index.html
    3. 根据请求组织数据内容 请求：请求头，请求行，空行，请求体
    4. 讲数据内容组成HTTP响应格式返回给浏览器
        响应：响应头，响应行，空行，响应体

    升级：
    1. 使用IO多路复用(select)，可以满足同时处理多个客户端发来的请求
    2. 做基本的请求解析，根据具体的请求返回具体的内容
    3. 通过类接口的形式进行功能(server)封装


    HTTPServer v2.0
    功能：
    1. 接收客户端(浏览器)请求
    2. 解析客户端发送的请求 index.html
    3. 根据请求组织数据内容 请求：请求头，请求行，空行，请求体
    4. 讲数据内容组成HTTP响应格式返回给浏览器
        响应：响应头，响应行，空行，响应体

    升级：
    1. 使用IO多路复用(select)，可以满足同时处理多个客户端发来的请求
    2. 做基本的请求解析，根据具体的请求返回具体的内容
    3. 通过类接口的形式进行功能(server)封装
"""
from socket import *
from select import *


# 建立套接字 -》 绑定地址 -》 监听 -》 accept -》 处理请求
class HTTPServer:
    def __init__(self, host, port, dir):
        self.host = host
        self.port = port
        self.dir = dir
        self.address = (host, port)
        # IO多路复用列表
        self.rlist = []
        self.wlist = []
        self.xlist = []
        # 创建套接字对象
        self.create_socket()
        # 绑定地址
        self.bind()

    # 绑定地址
    def bind(self):
        self.sockfd.bind(self.address)

    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        # 可重复使用
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # 启动服务
    def serve_forever(self):
        self.sockfd.listen(5)  # 监听
        print("Listen the port {}".format(self.port))
        # IO多路复用接收客户端的请求
        self.rlist.append(self.sockfd)
        while True:  # 使用select循环处理客户端发来的请求
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for r in rs:
                if r is self.sockfd:  # r为服务端的套接字
                    connfd, addr = r.accept()
                    print("Connect from {}".format(addr))
                    self.rlist.append(connfd)
                else:  # r为客户端与服务端的连接套接字
                    # 处理客户端发来的请求
                    self.handle(r)

    # 服务端处理客户端发来的请求
    def handle(self, connfd):
        # 接收http请求
        data = connfd.recv(1024)
        if not data:  # 客户端断开连接的处理
            self.rlist.remove(connfd)  # 从select的rlist中删除连接
            connfd.close()
            return
        # 将字节串进行切割，提取请求内容
        request_line = data.splitlines()[0]  # b'GET /index.html HTTP/1.1'
        info = request_line.decode().split(" ")[1]  # /index.html
        print(connfd.getpeername(), ":", info)  # 打印客户端的地址信息
        # 21:03上课～
        # 根据具体的请求内容进行数据处理
        # /index.html: 表示客户端要访问页面资源
        if info == "/" or info[-5:] == ".html":
            self.get_html(connfd, info)  # 处理页面请求
        else:
            self.get_data(connfd, info)  # 处理其他数据请求

    # 处理客户端的获取网页请求
    def get_html(self, connfd, info):
        # 获取网站首页信息 index.html
        if info == "/":  # http://127.0.0.1:12306/，表示客户端要访问首页
            filename = self.dir + "/index.html"  # ./static/index.html
        # 获取其他页面信息
        else:  # /hahahah.html
            filename = self.dir + info  # 例如：./static/new.html
            print("filename: ", filename)
        try:
            f = open(filename, "r")
        except Exception as e:
            # 如果要访问的资源不存在，则返回404
            response = "HTTP/1.1 404 Not Found\r\n"  # 响应头
            response += "Content-Type: text/html\r\n"  # 响应行
            response += "\r\n"
            response += "<h1>Page not found, sorry...</h1>"
            connfd.send(response.encode())
        else:
            # 组织HTTP Response给浏览器  响应头，响应行，空行，响应体
            response = "HTTP/1.1 200 OK\r\n"  # 响应头
            response += "Content-Type: text/html\r\n"  # 响应行
            response += "\r\n"  # 空行
            response += f.read()  # 响应体
            connfd.send(response.encode())

    # 处理其他请求  /index.html   username password  登录按钮
    # 127.0.0.1:12306/register
    def get_data(self, connfd, info):
        response = "HTTP/1.1 200 OK\r\n"  # 响应头
        response += "Content-Type: text/html\r\n"  # 响应行
        response += "\r\n"  # 空行
        response += "<h1>zan bu chu li ~ waiting for httpserverv3.0 ~</h1>"  # 响应体
        connfd.send(response.encode())
# 休息到21：03，15分钟～下节课开始正则表达式～
if __name__ == '__main__':
    HOST = "127.0.0.1"
    PORT = 12306
    DIR = "./static"  # 存储网页地址
    server = HTTPServer(HOST, PORT, DIR)  # 实例化对象
    server.serve_forever()  # 启动服务


