from chatmanager import bot

class Plugin(bot.ChatManager):
    def cmd_testcur(self, *_):
        return "This is a test of the currency function"