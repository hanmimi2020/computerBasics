"""
交作业方式：
作业文件路径为
axe34/socket_test.py
axe34/server_thread.c
axe34/server_fork.c


作业：
1, 用 py 的多线程模块 threading 实现一个多线程程序
    发送 3000 个 socket 请求到 localhost:3000 并接受响应
    不输出任何数据到终端
    记得 join
    本作业为 socket_test.py

2, 提供的代码是用多线程实现的并发服务器
    但是这个实现是有 bug 的
    使用作业 1 的程序就可以测出来错误
    请分析并改正这个 bug
    这个 bug 至少有 2 个修复方法
    本作业为 server_thread.c
"""

import socket
import threading


def send_socket(index):
    s = socket.socket()
    host = 'localhost'
    port = 3001
    # port = 443
    s.connect((host, port))

    http_request = 'GET / HTTP/1.1\r\nHost:{}\r\n\r\n'.format(host)
    request = http_request.encode()
    s.send(request)
    response = s.recv(1024)
    print("response", response, index, flush=True)


if __name__ == "__main__":
    threads = list()
    for index in range(5):
        th = threading.Thread(target=send_socket, args=[index,])
        threads.append(th)
        th.start()

    for index, thread in enumerate(threads):
        thread.join()