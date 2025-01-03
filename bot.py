import discord
import responses
import asyncio
import time
from datetime import datetime
from random import randrange
import settings


Bot_Enabled = True
loop_running = False
targetChannel = 0

async def send_message(message, user_message, is_private):
    global Bot_Enabled
    if user_message == 'disable': Bot_Enabled = False; print('disabled')
    if user_message == 'enable': Bot_Enabled = True; print('enabled')
    try:
        response = responses.handle_response(user_message)
        if (not Bot_Enabled) and (user_message != 'disable' and user_message != 'enable'):
            return
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
    settings.check_settings()
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
                global targetChannel
                print('cricket loop')
                print(f'delay {target_delay}')
                if not Bot_Enabled or targetChannel == 0:
                    await asyncio.sleep(30)
                    break
                if ((int(datetime.utcnow().strftime("%H"))-timezoneOffset) >= 22) or ((int(datetime.utcnow().strftime("%H"))-timezoneOffset) < 6):
                    print('Bot is no longer in service time. Modifying last message time to enable bot in service time.')
                    last_message_time = last_message_time + 1800
                cricket_time_target = last_message_time + target_delay
                print(f'Activation time {cricket_time_target}. Current time {time.time()}')
                if cricket_time_target <= time.time():
                    print("Cricket timer expired")
                    channel_id = client.get_channel(targetChannel)
                    easter_egg = (randrange(0, 1000) == 100)
                    if easter_egg:
                        await send_raw_message(
                            'https://tenor.com/view/dancing-cricket-gif-24701537',
                            channel_id)
                    else:
                        await send_raw_message(
                            'https://tenor.com/view/crickets-crickets-chirping-silence-awkward-silence-gif-5319192',
                            channel_id)
                    last_message_time = time.time()
                    cricket_time_target = last_message_time + target_delay
                print(f'waiting {cricket_time_target - time.time()} seconds')
                await asyncio.sleep(cricket_time_target - time.time()) if ((cricket_time_target - time.time()) > 0) else await asyncio.sleep(1)

    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Game(f'*chirp*'))
        print(f'{client.user} is now running!')
        global loop_running
        if not loop_running:
            loop = asyncio.get_event_loop()
            loop.create_task(cricket_timer())
            #this caused a warning of loop already running.(aka ignored error)
            #loop.run_forever()
            loop_running = True
            print('loop created')
        else:
            print('loop already running')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        nonlocal last_message_time
        global targetChannel
        if message.channel.id == targetChannel:
            last_message_time = time.time()
        print(f'recived message: {message.content}')
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        if user_message[0] == '!':
            user_message = user_message[1:]
            if user_message == 'Set channel':
                targetChannel = message.channel.id
                await send_raw_message('Channel Set', message.channel)
                return
            await send_message(message, user_message, is_private=False)

    @client.event
    async def on_disconnect():
        print('Discord Client has been disconnected.')

    client.run(settings.DISCORD_TOKEN)
