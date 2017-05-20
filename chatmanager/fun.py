import random
from chatmanager import bot

class Plugin(bot.ChatManager):
    def __init__(self):
        pass

    def cmd_funping(self, *_):
        return "Fun pong"

    def cmd_coolest(self, message, *_):
        return "{0} is the coolest!".format(message.author.name)

    def cmd_choose(self, *choice):
        return "I choose \"{0}\" this time.".format(random.choice(choice[1]))
