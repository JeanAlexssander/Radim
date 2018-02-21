import discord
import asyncio
import requests
import logging
import codecs
from config import Config


client = discord.Client()

logging.basicConfig(filename='example.log',level=logging.DEBUG)

@client.event
async def on_ready():
    logging.info('Logged in as')
    logging.info(client.user.name)
    logging.info(client.user.id)
    logging.info('So should this')

@client.event
async def on_message(message):
    if message.content.startswith('+test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    elif message.content.startswith('+sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

    elif message.content.startswith('+play'):
        file = codecs.open('procura.txt', 'w', 'UTF-8')

        yt_url = message.content[6:]
        busca = yt_url.replace(" ", "%20")

        link = str.format('https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={0}&type=\
        video&key={1}',busca,Config.KEY)
        

        search = requests.get(link)

        file.write(search.text)
        file.close()


        await client.send_message(message.channel, link)

client.run(Config.TOKEN)