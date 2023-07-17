import discord
import responses
import asyncio
import time
from datetime import datetime


Bot_Enabled = True

async def send_message(message, user_message, is_private):
    global Bot_Enabled
    if user_message == 'disable': Bot_Enabled = False; print('disabled')
    if user_message == 'enable': Bot_Enabled = True; print('enabled')
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


async def send_raw_message(message, channel):
    try:
        await channel.send(message)
        print('message sent')
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = 'OTY3OTkyODg2NDU5MjYwOTY4.GHWME5.vfyS_ecd8xBqSPzACFBgIVhtY1PGVEsQDSGzKs'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    #production delay  2 hours
    target_delay = 7200
    #testing delay 15 seconds
    #target_delay = 15
    last_message_time = time.time()
    cricket_time_target = last_message_time + (target_delay)
    timezoneOffset = 6


    async def cricket_timer():
        while True:
            while True:
                nonlocal cricket_time_target
                nonlocal last_message_time
                nonlocal target_delay
                nonlocal timezoneOffset
                global Bot_Enabled
                print('cricket loop')
                print(f'delay {target_delay}')
                if not Bot_Enabled:
                    await asyncio.sleep(30)
                    break
                if ((int(datetime.utcnow().strftime("%H"))-timezoneOffset) >= 22) or ((int(datetime.utcnow().strftime("%H"))-timezoneOffset) < 6):
                    print('Bot is no longer in service time. Modifying last message time to enable bot in service time.')
                    last_message_time = 6 - target_delay
                cricket_time_target = last_message_time + target_delay
                print(f'Activation time {cricket_time_target}. Current time {time.time()}')
                if cricket_time_target <= time.time():
                    print("Cricket timer expired")
                    #production channel id
                    channel_id = client.get_channel(1098802300039999592)
                    #testing channel id
                    #channel_id = client.get_channel(1129296068434202698)
                    await send_raw_message(
                    'https://tenor.com/view/crickets-crickets-chirping-silence-awkward-silence-gif-5319192', channel_id)
                    last_message_time = time.time()
                    cricket_time_target = last_message_time + target_delay
                print(f'waiting {cricket_time_target - time.time()} seconds')
                await asyncio.sleep(cricket_time_target - time.time()) #if ((cricket_time_target - time.time()) > 0) else await asyncio.sleep(1)

    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Game(f'*chirp*'))
        print(f'{client.user} is now running!')
        loop = asyncio.get_event_loop()
        loop.create_task(cricket_timer())
        #this caused a warning of loop already running.(aka ignored error)
        #loop.run_forever()
        print("loop created")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        if user_message[0] == '!':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=False)
        nonlocal last_message_time
        last_message_time = time.time()

    @client.event
    async def on_disconnect():
        print('Discord Client has been disconnected.')

    client.run(TOKEN)
