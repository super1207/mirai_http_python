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
    bot.addEventFun("FriendMessage",do_FriendMessage)
    bot.addEventFun("GroupMessage",do_GroupMessage)
    if bot.connect():
        bot.wait()
        bot.disconnect()
