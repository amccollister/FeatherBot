import random
from chatmanager import bot

class Plugin(bot.ChatManager):
    def __init__(self):
        pass
    # TODO: EmoteText Fact ROCKPAPERSCISSORS D20 8Ball rngImage randomWiki strawpoll joke Cleverbot
    def cmd_funping(self, *_):
        return "Fun pong"

    def cmd_coolest(self, message, *_):
        return "{0} is the coolest!".format(message.author.name)

    def cmd_choose(self, *choice):
        return "I choose \"{0}\" this time.".format(random.choice(choice[1]))
