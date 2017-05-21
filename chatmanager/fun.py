import random
from chatmanager import bot

class Plugin(bot.ChatManager):
    def __init__(self):
        pass
    # TODO: Fact D20 rngImage randomWiki strawpoll joke Cleverbot

    def cmd_coolest(self, message, *_):
        return "{0} is the coolest!".format(message.author.name)

    def cmd_choose(self, *choice):
        return "I choose \"{0}\" this time.".format(random.choice(choice[1]))

    def cmd_rps(self, message, *throw):
        choices = ["rock", "paper", "scissors"]
        ai_choice = random.choice(choices)
        if not throw[0] or throw[0][0].lower() not in choices:
            return "Come on, {0}... That's not a valid throw!".format(message.author.name)
        ply_choice = throw[0][0].lower()
        if (ply_choice == "rock" and ai_choice == "paper") or\
           (ply_choice == "paper" and ai_choice == "scissors") or\
           (ply_choice == "scissors" and ai_choice == "rock"):
            return "I chose {0} and that beats {1}. I WIN!".format(ai_choice, ply_choice)
        if ai_choice == ply_choice:
            return "Looks like we both picked {0}. Everyone loses!".format(ply_choice)
        return "I chose {0}, but {1} beats {0}. You win this time...".format(ai_choice, ply_choice)

    def cmd_flip(self, _, *flip):
        flips = ["heads", "tails"]
        result = random.choice(flips)
        win_loss = "LOSER"
        if not flip[0] or flip[0][0].lower() not in flips:
            return "What kind of coin are you flipping? It's \"heads\" or \"tails\"."
        if result.lower() == flip[0][0].lower():
            win_loss = "WINNER"
        return "{0}! {1}!".format(result.upper(), win_loss)

    def cmd_8ball(self, message, *args):
        answers = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it"
                   "As I see it, yes", "Most likely", "Very doubtful", "Yes", "Signs point to yes", "Ask again later",
                   "Reply hazy try again", "Better not tell you now", "Cannot predict it now", "My reply is no",
                   "Concentrate and ask again", "Don't count on it", "My sources say no", "Outlook not so good"]
        fate = random.choice(answers)
        if not args[0]:
            return "It's blank. You didn't ask it anything."
        return "{0} looks into the Magic 8 Ball. The die pops up and reads: \"{1}\"".format(message.author.name, fate)

    def cmd_emotetext(self, message, *args):
        if len(args[0]) < 4:
            return "Do it yourself you lazy bum."
        emote = " {0} ".format(args[0].pop(0))
        return "{0}{1}{0}".format(emote, emote.join(args[0]))

    def cmd_d20(self, message, *args):
        pass