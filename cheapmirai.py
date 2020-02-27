import requests,json
import time
from operator import methodcaller

class BOT:
    def __init__(self,url,qq,authKey):
        self.qq = qq
        self.sessionKey = None
        self.url = url
        self.authKey = authKey
    def connect(self):
        self.disconnect()
        print("request:","auth",{"authKey": self.authKey})
        res = requests.post(url = self.url+"/auth",json = {"authKey": self.authKey})
        print("response:","auth",res.text)
        res = res.json()
        if res['code'] != 0:
            print("error log:","get session failed")
        else:
            print("request:","verify",{"sessionKey": res['session'],"qq": self.qq})
            ress = requests.post(url = self.url+"/verify",json = {"sessionKey": res['session'],"qq": self.qq})
            print("response:","verify",ress.text)
            ress = ress.json()
            if ress['code'] == 0:
                self.sessionKey = res['session']
                return True
            else:
                print("error log:","verify session failed")
        return False
    def disconnect(self):
        if self.sessionKey != None:
            print("request:","release",{"sessionKey": self.sessionKey,"qq": self.qq})
            res = requests.post(url = self.url+"/release",json = {"sessionKey": self.sessionKey,"qq": self.qq})
            print("response:","release",res.text)
            self.sessionKey = None
    def __del__(self):
        self.disconnect()
    def sendFriendMessage(self,target,messageChain,quote = None):
        req = {"sessionKey": self.sessionKey,"target": target,"messageChain":messageChain}
        if quote != None:
            req["quote"] = quote
        print("request:","sendFriendMessage",req)
        res = requests.post(url = self.url+"/sendFriendMessage",json = req)
        ret = res.content
        print("response:","sendFriendMessage",str(ret))
        return ret
    def sendGroupMessage(self,target,messageChain,quote = None):
        req = {"sessionKey": self.sessionKey,"target": target,"messageChain":messageChain}
        if quote != None:
            req["quote"] = quote
        print("request:","sendGroupMessage",req)
        res = requests.post(url = self.url+"/sendGroupMessage",json = req)
        ret = res.content
        print("response:","sendGroupMessage",str(ret))
        return ret
    def sendImageMessage(self,urls,target = None,qq = None,group = None):
        req = {"sessionKey": self.sessionKey,"urls":urls}
        if target != None:
            req["target"] = target
        if qq != None:
            req["qq"] = qq
        if group != None:
            req["group"] = group
        print("request:","sendImageMessage",req)
        res = requests.post(url = self.url+"/sendImageMessage",json = req)
        ret = res.content
        print("response:","sendImageMessage",str(ret))
        return ret
    
    def uploadImage(self,type,img):
        '''未检验'''
        print("request:","uploadImage",{"type":type,"img":"..."})
        res=requests.request("POST",url, data=None, files=img)
        ret = res.content
        print("response:","uploadImage",str(ret))
        return ret

    def recall(self,target):
        '''未检验'''
        req = {"sessionKey": self.sessionKey,"target":target}
        print("request:","recall",req)
        res = requests.post(url = self.url+"/recall",json = req)
        ret = res.content
        print("response:","recall",str(ret))
        return ret

    def _fetchMessage(self,count = 10):
        res = requests.get(url = self.url+"/fetchMessage?sessionKey="+self.sessionKey+"&count="+str(count))
        ret = res.content
        return ret
    def wait(self,timescale = 0.5):
        while True:
            msgarr = []
            try:
                ret = self._fetchMessage()
                msgarr = json.loads(ret)
            except:
                pass
            for msg in msgarr:
                msgtype = msg['type']
                print("msgtype:",msgtype)
                try:
                    getattr(self,msgtype)(self,msg)
                except:
                    pass
            time.sleep(timescale)
    def setEventFun(self,msgtype,func):
        exec("self."+ msgtype + "=func")
