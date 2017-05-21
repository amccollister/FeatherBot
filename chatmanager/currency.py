import sqlite3 as sql
from chatmanager import bot

class Plugin(bot.ChatManager):
    def __init__(self):
        pass
    # TODO balance give lottery leaderboard slots

    def cmd_moneyping(self, *_):
        return "$$$ pong"
