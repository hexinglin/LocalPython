import socket
import json
import numpy as np


#创建socket对象
#SOCK_DGRAM    udp模式
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(("0.0.0.0",6000))  #绑定服务器的ip和端口
str = json.dumps({"mod": "homeCamera", "action": "regiter", "identity": "viviter", "NO": 0 })
bs = bytes(str, encoding="utf8")
print(s.sendto(bs, ('hecao.pw', 20001)))
stringData=s.recv(65500)  #一次接收1024字节
recvData = json.loads(stringData)
print(recvData)

str = json.dumps({"mod": "homeCamera", "action": "feedback", "identity": "viviter", "NO": 0, })
bs = bytes(str, encoding="utf8")
print(s.sendto(bs, (recvData['data']['ip'], recvData['data']['port'])))

print(s.sendto(bs, ('118.199.210.122', 8000)))
str = json.dumps({"mod": "homeCamera", "action": "feedback", "identity": "viviter", "NO": 0 })
bs = bytes(str, encoding="utf8")
s.sendto(bs, ('hecao.pw', 20001))

while True:
    print('wait')
    stringData=s.recv(65500)  #一次接收1024字节
    print(len(stringData))
    break
