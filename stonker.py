import discord
from discord import app_commands
import csv
import json

global allStonkDict
allStonkDict = {}
intents = discord.Intents.default()
stonkerBot = discord.Client(intents=intents)
tree = app_commands.CommandTree(stonkerBot)


# intents.message_content = True
description = 'a bot for notfiying you via discord pings whenever your stocks reach a specified price'



try: 
    with open('log.csv', 'r') as file_in:
        dictReader = csv.DictReader(file_in)
        for line in dictReader:
            if int(line['user_id']) not in allStonkDict:
                allStonkDict[int(line['user_id'])] = {}
            allStonkDict[int(line['user_id'])][line['ticker_symbol']] = (line['price'])
            # allStonkDict[int(line['user_id'])][int(line['attempt_number'])] = (line['attempt_duration'], datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(timeofDay[0]), int(timeofDay[1]), int(float(timeofDay[2])//1)), int(line['total_seconds']))
except Exception as e:
    print(e, 1)    




@stonkerBot.event
async def on_ready():
    print(f'{stonkerBot.user} is now running!')

@tree.command(name = 'diff',description="For adding a stock.",guild=discord.Object(id=929836210644463718))
@app_commands.describe(ticker='Stock\'s ticker symbol')
async def diff(interaction: discord.Interaction, ticker: str):
    await interaction.response.send_message(ticker)
    
    
with open('config.json', 'r') as cfg:
# Deserialize the JSON data (essentially turning it into a Python dictionary object so we can use it in our code) 
    data = json.load(cfg) 
TOKEN = data["token"]
#token goes here
stonkerBot.run(TOKEN)

    
    

# @stonkerBot.slash_command(description="For adding a stock.", name="add", intents=intents ,guild_ids=[929836210644463718, 126102372 1561264148])

# def to_upper(string): 
#     return string.upper()

# async def add(ctx, ticker: to_upper, price: float): 
#     if ctx.author.id not in list(allStonkDict.keys()):
        
#         allStonkDict[ctx.author.id] = {}
#         embed = discord.Embed(
#             description="added [ticker], will notify when the price reaches [price].",
#             color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
#         )

#         await ctx.respond(embed = embed)
#     else:
#         inputKey = list(allStonkDict[ctx.author.id].keys())[-1] + 1
#         print(inputKey)
#         embed = discord.Embed(
#             description=f'Ah, sorry to hear that. You went for',
#             color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
#         )
#         await ctx.respond(embed=embed)
#         allStonkDict[ctx.author.id][inputKey] = (datetime.datetime.now())
        
#     with open('log.csv', 'w') as file_out:
#         writer = csv.writer(file_out)
#         writer.writerow(['user_id', 'attempt_number', 'attempt_duration', 'timestamp', 'total_seconds'])
#         for userid in allStonkDict:
#             for attempt in allStonkDict[userid]:
#                 writer.writerow([userid, attempt, allStonkDict[userid][attempt][0], allStonkDict[userid][attempt][1], allStonkDict[userid][attempt][2]])
            
# @stonkerBot.slash_command(description="To view all your attempts.",
#   name="viewall",
# #   guild_ids=[929836210644463718, 1261023721561264148]
# )
# async def viewall(ctx):    
#     message = ''
#     with open('log.csv', 'r') as file_in:
#         dict = csv.DictReader(file_in)
#         for line in dict: 
#             if int(line['user_id']) == ctx.author.id:
#                 date = line['timestamp'].split()[0]
#                 if int(line['attempt_number']) == 1:
#                     message += f'First attempt: started on {date}.\n\n' 
#                 else:
#                     message += f'Attempt {line['attempt_number']}: Had a length of {line['attempt_duration'][:-1]} and ended on {date}.\n\n'
#     embed = discord.Embed(
#         title=f'{ctx.author}: All attempts',
#         description=f'{message}',
#         color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
#     )
#     await ctx.respond(embed=embed)
    
        
# @stonkerBot.slash_command(description="To view your longest attempt.",
#   name="longestattempt",
# #   guild_ids=[929836210644463718, 1261023721561264148]
# )
# async def longestattempt(ctx):    
#     max = 1 #Index by attempt number later
#     for attempt in allStonkDict[ctx.author.id]:
#         if allStonkDict[ctx.author.id][attempt][2] > allStonkDict[ctx.author.id][max][2]:
#             max = attempt
#     length = allStonkDict[ctx.author.id][max][0][:-1] #Cuts off the period at the end
#     date = f'{allStonkDict[ctx.author.id][max][1].month}-{allStonkDict[ctx.author.id][max][1].day}-{allStonkDict[ctx.author.id][max][1].year}'
            
            
#     embed = discord.Embed(
#         title=f'{ctx.author}\'s Longest attempt:',
#         color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
#     )
#     await ctx.respond(embed=embed)

# with open('config.json', 'r') as cfg:
# # Deserialize the JSON data (essentially turning it into a Python dictionary object so we can use it in our code) 
#     data = json.load(cfg)
    
# stonkerBot.run(data["token"])  

# #not able to take multiple, needs to be hosted somewhere
# # import os
# #rhi,monday, 4:30pm
# #rhi,1/5/24, 2pm
# # async def send_message(message, user_message, guilds, is_private):
# #     # try:
# #         # if 
# #     for guild in guilds: 
# #         if guild.name == 'King DeedleP\'s server':
#             # await message.channel.send(f'{message.author.mention} set a reminder to do {acc_mesage} at {timeofday}')


#             # text_log = await guild.fetch_channel(1247378604321538129)    
#             # textLogMsg = f'{message.author.mention} / {message.author} set up a reminder to {acc_mesage}'
#             # await text_log.send(textLogMsg)

#             # if seconds > 18000:
#             #     sleeptime = seconds-18000
#             #     time.sleep(sleeptime)
#             #     seconds -= sleeptime
#             #     await message.author.send(f'{message.author.mention} Hey, 5 hours until you need to do {acc_mesage}...remember, it\'s at {timeofday}')

#             # if seconds > 7200:
#             #     sleeptime = seconds-7200 
#             #     time.sleep(sleeptime)
#             #     seconds -= sleeptime
#             #     await message.author.send(f'{message.author.mention} Hey, 2 hours until you need to do {acc_mesage}...remember, it\'s at {timeofday}')

#             # if seconds > 3600:
#             #     sleeptime = seconds-3600
#             #     time.sleep(sleeptime)
#             #     seconds -= sleeptime
#             #     await message.author.send(f'{message.author.mention} Hey, 1 hour until you need to do {acc_mesage}...remember, it\'s at {timeofday}')

#             # if seconds > 300:
#             #     sleeptime = seconds-300
#             #     time.sleep(sleeptime)
#             #     seconds -= sleeptime
#             #     await message.author.send(f'{message.author.mention} Hey, 5 minutes until you need to do {acc_mesage}...remember, it\'s at {timeofday}')
#             # if seconds > 60:
#             #     sleeptime = seconds-60
#             #     time.sleep(sleeptime)
#             #     seconds -= sleeptime
#             #     await message.author.send(f'{message.author.mention} Hey, one minute until you need to do {acc_mesage}...remember, it\'s at {timeofday}')

#             # if seconds > 5:
#             #     sleeptime = seconds-5
#             #     time.sleep(sleeptime)
#             #     seconds -= sleeptime
#             #     for i in range(20):
#             #         await message.author.send(f'{message.author.mention} Hey, it\'s happening RIGHT NOW! You need to do {acc_mesage.upper()} right NOW at {timeofday}!!!!')
#             #         time.sleep(.5)
        
#     # except Exception as e:
#     #     print(e, 1)




#     # @client.event
#     # async def on_message(message):
#     #     if message.author != client.user: #client.user is the FUCKING BOT bruh
#     #         username = str(message.author)
#     #         user_message = str(message.content).lower()
#     #         channel = str(message.channel)
#     #         split = user_message.split()
#     #         if split[0][0] == 'r':
#     #             user_message = user_message[1:]
#     #             await send_message(message, user_message, client.guilds, is_private=True)
                    
    
