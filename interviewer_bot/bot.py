import discord
from dotenv import load_dotenv
import os
from discord.enums import ChannelType
from interviewer_bot.interviewer import Interviewer
import asyncio

load_dotenv()

bot = discord.Bot()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL1 = os.getenv('CHANNEL1')
CHANNEL2 = os.getenv('CHANNEL2')

threads = {}
interviewers = {}

def make_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = discord.Bot(intents=intents)

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')

    return bot

class InterviewerCog(discord.Cog):

    def __init__(self, bot:discord.Bot):
        self._bot = bot
        self.thread = None
        self.interviewer = None

    @bot.slash_command(description = 'fuck', name = 'work')
    async def work(ctx): # a slash command will be created with the name "ping"
        await ctx.respond(f"Pong! Latency is {bot.latency}")

    @discord.slash_command(description = 'practice new interview', name = 'interview')
    async def work(self, ctx, role: discord.Option(str)): # a slash command will be created with the name "ping"

        self.interviewer = Interviewer(role, verbose=True)
        self.thread = await ctx.channel.create_thread(name="new interview", type=ChannelType.public_thread)
        await ctx.respond('created new interview thread')
        await self.thread.send(f'Commencing {role} interview, say hi!')

    

    @discord.Cog.listener()
    async def on_message(self, message):
        # Make sure we won't be replying to ourselves.
        if message.author.id == self._bot.user.id:
            return

        if not message.channel.id == self.thread.id:
            return

        response = self.interviewer.process_message(message.content)
        await message.channel.send(response)


async def main():
    bot = make_bot()
    bot.add_cog(InterviewerCog(bot))
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())