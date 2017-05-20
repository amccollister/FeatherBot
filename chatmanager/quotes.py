from chatmanager import bot

class Plugin(bot.ChatManager):
    def __init__(self):
        pass

    def cmd_quoteping(self, *_):
        return "\"\" pong"
