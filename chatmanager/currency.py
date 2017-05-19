from chatmanager import bot

class Plugin(bot.ChatManager):
    async def cmd_testcur(self, message, *_):
        await self.send_message(message.channel, "This is a test from the Currency Plugin")

    def test(self):
        print("cur test")