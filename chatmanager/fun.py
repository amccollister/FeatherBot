from chatmanager import bot

class Plugin(bot.ChatManager):
     def cmd_testfun(self, *_):
        return "This is a test from the Fun Plugin"

