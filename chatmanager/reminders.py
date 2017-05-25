import sqlite3 as sql
import random
from datetime import datetime
from chatmanager import bot

class Plugin(bot.ChatManager):
    con = c = None  # Defining connection and cursor for sql DB
    pass