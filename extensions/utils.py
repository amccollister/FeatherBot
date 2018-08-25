'''
you'd use these later like my_embed = self.bot.make_embed("some text"), in a cog at least(edited)
Else you can make some utility script, which i'd do at least

July 17, 2018 3:02 AM Python Discord
Chibli#0001
'''

import discord


def make_embed(ctx, text):
    # https://cog-creators.github.io/discord-embed-sandbox/
    # https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#context
    bot = ctx.bot
    embed = discord.Embed()
    embed.set_author(name=ctx.author.name, url="https://github.com/amccollister/FeatherBot", icon_url=ctx.author.avatar_url)
    embed.set_footer(text="FeatherBot v0.0.1")
    embed.add_field(name=ctx.command, value=text, inline=True)
    return embed

# Make a send_msg() method
# send message on its own
async def send(ctx, text):
    embed = make_embed(ctx, text)
    await ctx.send(embed=embed)
