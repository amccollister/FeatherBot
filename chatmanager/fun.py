import random
import string
import urllib.request

from chatmanager import bot

class Plugin(bot.ChatManager):
    def __init__(self, *_):
        pass

    def cmd_coolest(self, message, *_):
        return "{0} is the coolest!".format(self.get_name(message))

    def cmd_choose(self, _, *choice):
        return "I choose \"{0}\" this time.".format(random.choice(choice))

    def cmd_rps(self, message, *throw):
        choices = ["rock", "paper", "scissors"]
        ai_choice = random.choice(choices)
        if not throw[0] or throw[0][0].lower() not in choices:
            return "Come on, {0}... That's not a valid throw!".format(self.get_name(message))
        ply_choice = throw[0][0].lower()
        if (ply_choice == "rock" and ai_choice == "paper") or\
           (ply_choice == "paper" and ai_choice == "scissors") or\
           (ply_choice == "scissors" and ai_choice == "rock"):
            return "I chose {0} and that beats {1}. I WIN!".format(ai_choice, ply_choice)
        if ai_choice == ply_choice:
            return "Looks like we both picked {0}. Everyone loses!".format(ply_choice)
        return "I chose {0}, but {1} beats {0}. You win this time...".format(ai_choice, ply_choice)

    def cmd_flip(self, _, *flip_args):
        flips = ["heads", "tails"]
        result = random.choice(flips)
        win_loss = "LOSER"
        if not flip_args[0] or flip_args[0][0].lower() not in flips:
            return "What kind of coin are you flipping? It's \"heads\" or \"tails\"."
        if result.lower() == flip_args[0][0].lower():
            win_loss = "WINNER"
        return "{0}! {1}!".format(result.upper(), win_loss)

    def cmd_8ball(self, message, *args):
        answers = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it",
                   "As I see it, yes", "Most likely", "Very doubtful", "Yes", "Signs point to yes", "Ask again later",
                   "Reply hazy try again", "Better not tell you now", "Cannot predict it now", "My reply is no",
                   "Concentrate and ask again", "Don't count on it", "My sources say no", "Outlook not so good"]
        fate = random.choice(answers)
        if not args[0]:
            return "It's blank. You didn't ask it anything."
        return "{0} looks into the Magic 8 Ball. The die pops up and reads: **\"{1}\"**".format(self.get_name(message), fate)

    def cmd_emotetext(self, _, *args):
        if len(args[0]) < 5:
            return "Do it yourself you lazy bum."
        emote = " {0} ".format(args[0].pop(0))
        return "{0}{1}{0}".format(emote, emote.join(args[0]))

    def cmd_roll(self, message, *args):
        try:
            dice = args[0][0].split("d")
            if not dice[0] or dice[0] == "1":
                roll = random.randint(1, int(dice[1]))
                return "The d{0} landed on {1}".format(dice[1], str(roll))
            else:
                rolls = []
                roll_total = 0
                for i in range(int(dice[0])):
                    roll = random.randint(1, int(dice[1]))
                    roll_total += roll
                    rolls.append(roll)
                return "{0} rolled {1}d{2} for a total of {3}.```{4}```".format(self.get_name(message), dice[0], dice[1],
                                                                           roll_total, " + ".join(str(r)for r in rolls))
        except:
            return "Please roll again. The dice landed on the floor. :("

    def cmd_imgur(self, *_):
        prefix = "https://i.imgur.com/"
        chars = string.ascii_letters + string.digits
        attempts = 1
        while True:
            suffix = (random.choice(chars) for x in range(random.choice([5, 7])))
            link = prefix + "".join(suffix)
            try:
                with urllib.request.urlopen(link) as response:
                    if response.getcode() == 200:
                        return "Found {0} after **{1}** attempts.".format(link, attempts)
            except Exception as e:
                attempts += 1
                continue

    def cmd_fact(self, *_):
        with urllib.request.urlopen("https://www.reddit.com/r/funfacts/random") as response:
            return response.geturl()

    def cmd_joke(self, *_):
        with urllib.request.urlopen("https://www.reddit.com/r/jokes/random") as response:
            return response.geturl()

    def cmd_wiki(self, message, *args):
        if not args[0]:
            link = "https://en.wikipedia.org/wiki/Special:Random"
        else:
            link = "https://en.wikipedia.org/wiki/" + "_".join(args[0])
        with urllib.request.urlopen(link) as response:
            return response.geturl()
