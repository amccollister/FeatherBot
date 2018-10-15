import re
import random
import string
import urllib.error
import urllib.request

from discord.ext import commands
import extensions.utils as util


class FunCog:
    @commands.command()
    async def magic8ball(self, ctx, *arg):
        answers = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it",
                   "As I see it, yes", "Most likely", "Very doubtful", "Yes", "Signs point to yes", "Ask again later",
                   "Reply hazy try again", "Better not tell you now", "Cannot predict it now", "My reply is no",
                   "Concentrate and ask again", "Don't count on it", "My sources say no", "Outlook not so good"]
        text = random.choice(answers)
        if not arg:
            text = "It's blank. You didn't ask it anything."
        await util.send(ctx, text)

    @commands.command()
    async def coolest(self, ctx):
        text = "{0.author.name} is the coolest.".format(ctx)
        await util.send(ctx, text)

    @commands.command()
    async def choose(self, ctx, *args):
        text = "I pick {0}".format(random.choice(args))
        await util.send(ctx, text)

    @commands.command()
    async def rps(self, ctx, arg):
        choice = ["rock", "paper", "scissors"]
        ai_choice = random.choice(choice)
        if arg not in choice:
            text = "That's not a valid choice. Try again."
            await util.send(ctx, text); return
        result = choice.index(arg) - choice.index(ai_choice)
        text = "You chose **{0}**.\nI chose **{1}**.\n".format(arg, ai_choice)
        if result == -1 or result == 2:
            text += "You lose!"
        elif result == 0:
            text += "We tied. Let's try again."
        else:
            text += "You win!"
        await util.send(ctx, text)

    @commands.command()
    async def emoter(self, ctx, arg1, arg2):
        emote = " {0} ".format(arg1)
        sentence = arg2.split(" ")
        text = "{0}{1}{0}".format(emote, emote.join(sentence))
        await util.send(ctx, text)

    @commands.command()
    async def roll(self, ctx, arg):
        roll = re.split("[d+]", arg)
        total = 0
        text = "Rolled a "
        try:
            if len(roll[0]) > 3 or arg[0] not in string.digits: raise Exception
            count = int(roll[0])
            sides = int(roll[1])
            for i in range(count):
                r = random.randint(1, sides)
                total += r
                text += "{} + ".format(r)
            if len(roll) > 2:
                add = int(roll[2])
                total += add
                text += "{}".format(add)
            else:
                text = text[:-2]
            text += " for a total of **{}!**".format(total)
        except:
            text = "The dice landed on the floor. Please try again!"
        await util.send(ctx, text)

    @commands.command()
    async def imgur(self, ctx):
        prefix = "https://i.imgur.com/"
        chars = string.ascii_letters + string.digits
        attempts = 1
        while True:
            suffix = (random.choice(chars) for x in range(random.choice([5, 7])))
            link = prefix + "".join(suffix)
            try:
                with urllib.request.urlopen(link) as response:
                    if response.getcode() == 200:
                        text = "Found {0} after **{1}** attempts.".format(link, attempts)
                        await util.send(ctx, text, link+".png"); break  # add .png to adjust for proxy_url
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    attempts += 1; continue
                else: raise

    @commands.command()
    async def wiki(self, ctx, *arg):
        """
        Usage:
                !wiki [thing]

        Displays an article for a specific thing based on the parameter.
        If no arguments are provided, a random link is displayed.
        """
        if not arg:
            link = "https://en.wikipedia.org/wiki/Special:Random"
        else:
            link = "https://en.wikipedia.org/wiki/" + str(arg[0]).replace(" ", "_")
            print("Testing {}".format(link))
        with urllib.request.urlopen(link) as response:
            text = response.geturl()
            await util.send(ctx, text)

def setup(bot):
    bot.add_cog(FunCog())


'''
class Plugin(bot.ChatManager):
    def __init__(self, bot):
        self.bot = bot

    async def cmd_coolest(self, message, *_):
        """
        Usage:
                !coolest

        Gives the coolest user on the server.
        """
        await self.bot.send_msg(message.channel, "{0} is the coolest!".format(self.get_name(message)))

    async def cmd_choose(self, message, *choice): # Choose nothing?
        """
        Usage:
                !choose <arg1 arg2, [arg3, etc.]>

        Lets the bot choose from a list of options.
        """
        await self.bot.send_msg(message.channel, "I choose \"{0}\" this time.".format(random.choice(choice[0])))

    async def cmd_rps(self, message, *throw):
        """
        Usage:
                !rps <rock | paper | scissors>

        Play a game of rock, paper, scissors with the bot. It usually doesn't cheat.
        """
        choices = ["rock", "paper", "scissors"]
        ai_choice = random.choice(choices)
        if not throw[0] or throw[0][0].lower() not in choices:
            await self.bot.send_msg(message.channel, "Come on, {0}... That's not a valid throw!".format(self.get_name(message)))
        ply_choice = throw[0][0].lower()
        if (ply_choice == "rock" and ai_choice == "paper") or\
           (ply_choice == "paper" and ai_choice == "scissors") or\
           (ply_choice == "scissors" and ai_choice == "rock"):
            await self.bot.send_msg(message.channel, "I chose {0} and that beats {1}. I WIN!".format(ai_choice, ply_choice))
        if ai_choice == ply_choice:
            await self.bot.send_msg(message.channel, "Looks like we both picked {0}. Everyone loses!".format(ply_choice))
            await self.bot.send_msg(message.channel, "I chose {0}, but {1} beats {0}. You win this time...".format(ai_choice, ply_choice))

    async def cmd_flip(self, message, *flip_args):
        """
        Usage:
                !flip <heads | tails>

        Flip a coin. Call it in the air.
        """
        flips = ["heads", "tails"]
        result = random.choice(flips)
        win_loss = "LOSER"
        if not flip_args[0] or flip_args[0][0].lower() not in flips:
            await self.bot.send_msg(message.channel, "What kind of coin are you flipping? It's \"heads\" or \"tails\".")
        else:
            if result.lower() == flip_args[0][0].lower():
                win_loss = "WINNER"
            await self.bot.send_msg(message.channel, "{0}! {1}!".format(result.upper(), win_loss))

    async def cmd_8ball(self, message, *args):
        """
        Usage:
                !8ball <question>

        Ask the Magic 8 Ball a question and see what it says.
        """
        answers = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it",
                   "As I see it, yes", "Most likely", "Very doubtful", "Yes", "Signs point to yes", "Ask again later",
                   "Reply hazy try again", "Better not tell you now", "Cannot predict it now", "My reply is no",
                   "Concentrate and ask again", "Don't count on it", "My sources say no", "Outlook not so good"]
        fate = random.choice(answers)
        if not args[0]:
            await self.bot.send_msg(message.channel, "It's blank. You didn't ask it anything.")
            await self.bot.send_msg(message.channel,
                                    "{0} looks into the Magic 8 Ball. The die pops up and reads: **\"{1}\"**".format(self.get_name(message), fate))

    async def cmd_emotetext(self, message, *args):
        """
        Usage:
                !emotetext <emote> <text>

        Easily create sentences with emotes in between each word.
        """
        if len(args[0]) < 5:
            await self.bot.send_msg(message.channel, "Do it yourself you lazy bum.")
        emote = " {0} ".format(args[0].pop(0))
        await self.bot.send_msg(message.channel, "{0}{1}{0}".format(emote, emote.join(args[0])))

    async def cmd_roll(self, message, *args):
        """
        Usage:
                !roll 10d20

        Rolls any type of die some number of times (Limit 100), i.e. 1d20, 10d8, 4d6, etc.
        """
        try:
            dice = args[0][0].split("d")
            if not dice[0] or dice[0] == "1":
                roll = random.randint(1, int(dice[1]))
                await self.bot.send_msg(message.channel, "The d{0} landed on {1}".format(dice[1], str(roll)))
            else:
                rolls = []
                roll_total = 0
                dice_count = int(dice[0])
                if dice_count > 100 or dice_count < 1: raise Exception
                for i in range(dice_count):
                    roll = random.randint(1, int(dice[1]))
                    roll_total += roll
                    rolls.append(roll)
                await self.bot.send_msg(message.channel, "{0} rolled {1}d{2} for a total of {3}.```{4}```"
                                        .format(self.get_name(message), dice[0], dice[1], roll_total, " + ".join(str(r)for r in rolls)))
        except:
            await self.bot.send_msg(message.channel, "Please roll again. The dice landed on the floor. :(")

    async def cmd_imgur(self, message, *_):
        """
        Usage:
                !imgur

        Generates random imgur links and displays the first one that exists and how many attempts it took.
        """
        prefix = "https://i.imgur.com/"
        chars = string.ascii_letters + string.digits
        attempts = 1
        while True:
            suffix = (random.choice(chars) for x in range(random.choice([5, 7])))
            link = prefix + "".join(suffix)
            try:
                with urllib.request.urlopen(link) as response:
                    if response.getcode() == 200:
                        await self.bot.send_msg(message.channel, "Found {0} after **{1}** attempts.".format(link, attempts))
                        break
            except Exception as e:
                attempts += 1
                continue

    async def cmd_fact(self, message, *_): # TOO MANY REQUESTS?
        """
        Usage:
                !fact

        Displays a random fact it found on reddit. Hopefully it's interesting.
        """
        with urllib.request.urlopen("https://www.reddit.com/r/funfacts/random") as response:
            await self.bot.send_msg(message.channel, response.geturl())

    async def cmd_joke(self, message, *_):
        """
        Usage:
                !joke

        Displays a random joke it found on reddit. Hopefully it's funny.
        """
        with urllib.request.urlopen("https://www.reddit.com/r/jokes/random") as response:
            await self.bot.send_msg(message.channel, response.geturl())

    async def cmd_wiki(self, message, *args):
        """
        Usage:
                !wiki [thing]

        Displays an article for a specific thing based on the parameter. 
        If no arguments are provided, a random link is displayed.
        """
        if not args[0]:
            link = "https://en.wikipedia.org/wiki/Special:Random"
        else:
            link = "https://en.wikipedia.org/wiki/" + "_".join(args[0])
        with urllib.request.urlopen(link) as response:
            await self.bot.send_msg(message.channel, response.geturl())
'''