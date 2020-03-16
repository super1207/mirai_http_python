# mirai_http_python
一个简单的用于和[mirai](https://github.com/mamoe/mirai)QQ机器人框架的HTTP接口对接的python框架
* [x] 认证相关API
* [x] 消息相关API  
* [x] 事件相关EVENT
* [x] 管理相关
* [ ] 简化、封装调用方式

A simple code:
```python3
from cheapmirai import BOT
import json
from io import BytesIO
import requests
import traceback


# 根据QQ号获取头像图片
def getQQImg(qq):
    url = 'http://q1.qlogo.cn/g?b=qq&nk={0}&s=640'.format(qq)
    file_like = BytesIO(requests.get(url).content)
    return file_like


# 好友消息处理函数
def do_FriendMessage(bot,msg):
    if(msg['messageChain'][1]['text'] == '我的头像'):
        print("Hello World")
        # 获取好友头像的imageId
        imageId = json.loads(
            bot.uploadImage(
                'friend',  # 如果是群聊，则为group
                getQQImg(msg['sender']['id'])
            )
        )['imageId']
        # 发送好友消息
        bot.sendFriendMessage(
            msg['sender']['id'], #要发送的好友
            # 消息内容
            [
                { "type": "Image", "imageId":imageId},
                { "type": "Plain", "text":"头像哦~" }
            ]
        )

if __name__ == "__main__":
    # 登录
    bot = BOT("http://localhost:8080",1736293901,"INITKEYKEXAqf1o")
    # 绑定消息处理函数
    bot.addEventFun("FriendMessage",do_FriendMessage)
    if bot.connect():
        bot.wait() #进入消息循环
        bot.disconnect()

```

reference [https://github.com/mamoe/mirai-api-http/blob/master/README.md](https://github.com/mamoe/mirai-api-http/blob/master/README.md)

开源协议： AGPL-3.0
