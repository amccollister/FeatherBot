import os
import configparser
# CONSTANTS FROM CONFIG AND PERMISSIONS

cfg = configparser.ConfigParser()
cfg.read("config/config.ini")
chat = cfg["Chat"]
currency = cfg["Currency"]
DISCORD_MSG_LIMIT = 2000

# CHAT CONFIGS
OWNER_ID = cfg["Owner"]["OwnerID"]
BOT_TOKEN = os.environ["DISCORD_TOKEN"]
PLUGINS = cfg["Plugins"]["EnabledPlugins"].split(" ")
PREFIX = chat["CommandPrefix"]
MOTD = chat["MOTD"]
WHITELIST = chat["BindToChannels"].split(" ")
BLACKLIST = chat["RestrictFromChannels"].split(" ")

# CURRENCY CONFIGS
LOTTERY_CHANNEL = currency["LotteryChannel"]
LOTTERY_PRICE = int(currency["TicketPrice"])
PAYCHECK = int(currency["Payout"])
PAY_TIME = int(currency["PayoutTime"])
DRAW_TIME = int(currency["LotteryDrawTime"])
SLOTS_PAYOUT = currency["SlotsPayout"].split(" ")
RANK_LIST = currency["Rankups"].split(" ")
RANK_COST = currency["RankCost"].split(" ")
