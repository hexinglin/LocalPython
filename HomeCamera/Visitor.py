#coding=UTF-8

class Visitor:
    NO = None
    IP = None
    PORT = None

    COUNT = None

    def __init__(self,jsonData:'dict'):
        if jsonData.get('NO') == None:
            raise Exception("NO can not found")
        self.NO =jsonData['NO']

        if jsonData.get('data') == None:
            raise Exception("data can not found")
        dataContent = jsonData['data']

        if dataContent.get('ip') == None:
            raise Exception("ip can not found")
        self.IP =dataContent['ip']

        if dataContent.get('port') == None:
            raise Exception("port can not found")
        self.PORT =dataContent['port']

        self.COUNT = 5