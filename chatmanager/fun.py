from chatmanager import bot

class Plugin(bot.ChatManager):
    async def cmd_testfun(self, message, *_):
        await self.send_message(message.channel, "This is a test from the Fun Plugin")

    def test(self):
        print("fun test")
