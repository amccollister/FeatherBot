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
BOT_TOKEN = os.environ.get("DISCORD_TOKEN")
PLUGINS = cfg["Plugins"]["EnabledPlugins"].split(" ")
PREFIX = chat["CommandPrefix"]
WHITELIST = chat["BindToChannels"].split(" ")
BLACKLIST = chat["RestrictFromChannels"].split(" ")

# CURRENCY CONFIGS
CURRENCY_CHANNEL = currency["CurrencyChannel"]
PAYCHECK = int(currency["Payout"])
