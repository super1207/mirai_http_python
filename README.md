# mirai_http_python
一个简单的用于和[mirai](https://github.com/mamoe/mirai)QQ机器人框架的HTTP接口对接的python框架
* [x] 认证相关API
* [x] 消息相关API  
* [x] 事件相关EVENT
* [ ] 管理相关(TODO)

A simple code:
```python3
from cheapmirai import BOT

def do_GroupMessage(bot,msg):
    if msg['sender']['group'] == 987654321:
        bot.sendGroupMessage(msg['sender']['group']['id'], [
            { "type": "Plain", "text":"hello\n" },
            { "type": "Plain", "text":"world" }
        ])

def do_FriendMessage(bot,msg):
    bot.sendFriendMessage(
        msg['sender']['id'],
        [
            { "type": "Plain", "text":"hello\n" },
            { "type": "Plain", "text":"world" }
        ]
    )

if __name__ == "__main__":
    bot = BOT("http://localhost:8080",123456789,"InitKeyG9EnAitj")
    bot.setEventFun("FriendMessage",do_FriendMessage)
    bot.setEventFun("GroupMessage",do_GroupMessage)
    if bot.connect():
        bot.wait()
        bot.disconnect()
```

reference [https://github.com/mamoe/mirai/blob/master/mirai-api-http/README_CH.md](https://github.com/mamoe/mirai/blob/master/mirai-api-http/README_CH.md)

开源协议： AGPL-3.0
