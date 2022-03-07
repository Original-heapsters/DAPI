import os
import io
from dotenv import load_dotenv
import discord
import requests
from discord.ext import commands

load_dotenv()
SERVER = os.environ.get('SERVER') or 'localhost:5001'
TOKEN = os.environ.get('TOKEN') or 'no_token'
PREFIX = os.environ.get('PREFIX') or '>'
bot = commands.Bot(command_prefix=PREFIX)


class Airfry(object):
    def __init__(self, server, token, prefix):
        self.server = server
        self.token = token
        self.prefix = prefix

    def start_bot(self):
        bot.run(self.token)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')
        print('------')

    @bot.command()
    async def ping(ctx):
        await ctx.send('pong')

    @bot.command()
    async def swaggy(ctx):
        await ctx.send('beans')

    @bot.command()
    async def fry(ctx, filter_id=None):
        attachment_url = ctx.message.attachments[0].url
        # file_request = requests.get(attachment_url)
        # with tempfile.NamedTemporaryFile(mode="wb") as img:
        #     img.write(file_request.content)
        param_config = {'asApi': True, 'file_url': attachment_url}
        rand_fry = '/home'
        iso_fry = '/filters/{}'.format(filter_id)

        target_route = rand_fry if not filter_id else iso_fry
        endpoint = '{}{}'.format(SERVER, target_route)

        fried = requests.post(endpoint, params=param_config)
        output_file = discord.File(io.BytesIO(fried.content),
                                   filename='fried.png')
        await ctx.send("toooasttyyyyy", file=output_file)


if __name__ == '__main__':
    airfryer = Airfry(SERVER, TOKEN, '>')
    airfryer.start_bot()
