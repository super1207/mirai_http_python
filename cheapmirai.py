import requests,json
import time
from operator import methodcaller
import traceback

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
        print("request:","uploadImage",{"type":type,"img":"..."})
        res=requests.post(self.url+"/uploadImage", data = {"sessionKey": self.sessionKey,'type':type}, files={"img":img})
        ret = res.content
        print("response:","uploadImage",str(ret))
        return ret

    def recall(self,target):
        '''未检验,缺少target(messaeId)'''
        req = {"sessionKey": self.sessionKey,"target":target}
        print("request:","recall",req)
        res = requests.post(url = self.url+"/recall",json = req)
        ret = res.content
        print("response:","recall",str(ret))
        return ret

    def friendList(self):
        req = "/friendList?sessionKey="+self.sessionKey
        print("request:","friendList",req)
        res = requests.get(self.url + req)
        ret = res.content
        print("response:","friendList",str(ret))
        return ret

    def groupList(self):
        req = "/groupList?sessionKey="+self.sessionKey
        print("request:","groupList",req)
        res = requests.get(self.url + req)
        ret = res.content
        print("response:","groupList",str(ret))
        return ret
    
    def memberList(self,target):
        req = "/memberList?sessionKey="+self.sessionKey+"&target=" + str(target)
        print("request:","memberList",req)
        res = requests.get(self.url + req)
        ret = res.content
        print("response:","memberList",str(ret))
        return ret

    def muteAll(self,target):
        req = {"sessionKey": self.sessionKey,"target": target}
        print("request:","muteAll",req)
        res = requests.post(url = self.url+"/muteAll",json = req)
        ret = res.content
        print("response:","muteAll",str(ret))
        return ret
    
    def unmuteAll(self,target):
        req = {"sessionKey": self.sessionKey,"target": target}
        print("request:","unmuteAll",req)
        res = requests.post(url = self.url+"/unmuteAll",json = req)
        ret = res.content
        print("response:","unmuteAll",str(ret))
        return ret

    def mute(self,target,memberId,time = 0):
        req = {
            "sessionKey": self.sessionKey,
            "target": target,
            "memberId": memberId,
            "time": time
            }
        print("request:","mute",req)
        res = requests.post(url = self.url+"/mute",json = req)
        ret = res.content
        print("response:","mute",str(ret))
        return ret

    def unmute(self,target,memberId):
        req = {
            "sessionKey": self.sessionKey,
            "target": target,
            "memberId": memberId,
            }
        print("request:","unmute",req)
        res = requests.post(url = self.url+"/unmute",json = req)
        ret = res.content
        print("response:","unmute",str(ret))
        return ret

    def kick(self,target,memberId,msg = None):
        '''未测试'''
        req = {
            "sessionKey": self.sessionKey,
            "target": target,
            "memberId": memberId,
            }
        if msg != None:
            req["msg"] = msg
        print("request:","kick",req)
        res = requests.post(url = self.url+"/kick",json = req)
        ret = res.content
        print("response:","kick",str(ret))
        return ret

    def groupConfigSet(self,target,config):
        req = {
            "sessionKey": self.sessionKey,
            "target": target,
            "config": config
            }
        print("request:","groupConfig",req)
        res = requests.post(url = self.url+"/groupConfig",json = req)
        ret = res.content
        print("response:","groupConfig",str(ret))
        return ret

    def groupConfigGet(self,target):
        req = "/groupConfig?sessionKey="+self.sessionKey+"&target=" + str(target)
        print("request:","groupConfig",req)
        res = requests.get(self.url + req)
        ret = res.content
        print("response:","groupConfig",str(ret))
        return ret

    def memberInfoSet(self,target,memberId,info):
        req = {
            "sessionKey": self.sessionKey,
            "target": target,
            "memberId": memberId,
            "info": info
            }
        print("request:","memberInfo",req)
        res = requests.post(url = self.url+"/memberInfo",json = req)
        ret = res.content
        print("response:","memberInfo",str(ret))
        return ret

    def memberInfoGet(self,target,memberId):
        req = "/memberInfo?sessionKey="+self.sessionKey+"&target=" + str(target)+"&memberId=" + str(memberId)
        print("request:","memberInfo",req)
        res = requests.get(self.url + req)
        ret = res.content
        print("response:","memberInfo",str(ret))
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
                print("message:",msg)
                msgtype = msg['type']
                f = None
                try:
                    f = getattr(self,msgtype)
                except:
                    pass
                try:
                    if f != None:
                        f(self,msg)
                except:
                    traceback.print_exc()
            time.sleep(timescale)
    def setEventFun(self,msgtype,func):
        exec("self."+ msgtype + "=func")
