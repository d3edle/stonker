from typing import Optional
import json
import csv 
import asyncio
import yfinance as yf

''
import discord
from discord import app_commands


# MY_GUILD = discord.Object(id=929836210644463718)  # replace with your guild id


#Setup variables----------------------------------------------------------------
global allStonkDict
allStonkDict = {}
with open('log.csv', 'r') as file_in:
    dictReader = csv.DictReader(file_in)
    for line in dictReader:
        allStonkDict[line['ticker']] = (line['price'], line['id'], line['specifier'])


stonkList = []

with open('nasdaq.csv', 'r') as file_in:
    dictReader = csv.DictReader(file_in)
    for line in dictReader:
        stonkList.append(line['Symbol'])

class MyClient(discord.Client):
    # Suppress error on the User attribute being None since it fills up later
    user: discord.ClientUser

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    # async def setup_hook(self):
    #     # This copies the global commands over to your guild.
    #     self.tree.copy_global_to(guild=MY_GUILD)
    #     await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)


#Helpers----------------------------------------------------------------


def floatable(x: str) -> Optional[float]:
    try:
        float(x)
        return True
    except ValueError:
        return False
    
def delete_key(key):
    del allStonkDict[key]
    rewrite()

def rewrite():
    with open('log.csv', 'w') as file_out:
        writer = csv.writer(file_out)
        writer.writerow(['ticker', 'price', 'id', 'specifier'])
        for ticker in allStonkDict:
            (price, id, specifier) = allStonkDict[ticker]
            writer.writerow([ticker, price, id, specifier])



#Events-----------------------------------------------------------------

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    client.loop.create_task(price_watcher())



def get_current_price(ticker: str) -> float:
    stock = yf.Ticker(ticker)
    todays_data = stock.history(period='1d')
    return todays_data['Close'].iloc[0]



async def price_watcher():
    await client.wait_until_ready()
    # user_id = 754118250719084584  # Replace with your user ID
    while not client.is_closed():
        remove_keys = []
        for ticker in allStonkDict.keys():
            current = get_current_price(ticker)
            if allStonkDict[ticker][2] == 'over':
                if current >= float(allStonkDict[ticker][0]):
                    user = await client.fetch_user(int(allStonkDict[ticker][1]))
                    await user.send(f'{ticker} has reached your target price of {allStonkDict[ticker][0]} (current: {current})!')
                    remove_keys.append(ticker)
            elif allStonkDict[ticker][2] == 'under':
                if current <= float(allStonkDict[ticker][0]):
                    user = await client.fetch_user(int(allStonkDict[ticker][1]))
                    await user.send(f'{ticker} has reached your target price of {allStonkDict[ticker][0]} (current: {current})!')
                    remove_keys.append(ticker)       
        for key in remove_keys:
            delete_key(key) 

        await asyncio.sleep(1800)  # Check every 30 minutes


# prop = await client.fetch_user(allStonkDict['a'][1])
# await prop.send('hi')




#Commands----------------------------------------------------------------

@client.tree.command()
async def all(interaction: discord.Interaction):
    """To view all stocks you are tracking, their target prices, and their current prices."""
    string = ""
    embed = discord.Embed(title=f'All stocks for {interaction.user.name}', color=discord.Color.blurple())
    for ticker in allStonkDict:
        if str(allStonkDict[ticker][1]) == str(interaction.user.id):
            current_price = get_current_price(ticker)
            (price, id, specifier) = allStonkDict[ticker]

            embed.add_field(name=ticker, value=f'Target Price: {price} Current Price: {current_price} Specifier: {specifier}', inline=False)
    await interaction.response.send_message(embed=embed)

@client.tree.command()
@app_commands.describe(
    ticker='The ticker symbol of the stock you want to delete',
)
async def delete(interaction: discord.Interaction, ticker: str):
    """To delete a stock."""
    ticker = ticker.upper()
    for stock in allStonkDict:
        if stock == ticker:
            if str(allStonkDict[stock][1] == str(interaction.user.id)):
                delete_key(ticker)
                embed = discord.Embed(
                    title=f'{ticker} has been deleted.',
                    color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
                )
                await interaction.response.send_message(embed=embed)
                return
    embed = discord.Embed(title=f'{ticker} was not found in your list.',)
    await interaction.response.send_message(embed=embed)


@client.tree.command()
@app_commands.describe(
    price='The price you want to buy the stock at',
    specifier='For wanting to be notified if the stock goes over or under the price'
)
@app_commands.choices(specifier=[app_commands.Choice(name='over', value='over'),
                                app_commands.Choice(name='under', value='under')])
async def edit(interaction: discord.Interaction, ticker: str, price: str, specifier: app_commands.Choice[str]):
    """To edit a stock's tracking."""
    ticker = ticker.upper()
    specifier = specifier.value

    # Checks if the ticker is valid
    if ticker not in stonkList:
        embed = discord.Embed(
        description= f'{ticker} is not a valid ticker symbol. Please try again.',
        color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
        )  
        await interaction.response.send_message(embed=embed)
        return

    # Checks if the price is valid
    if not floatable(price) or float(price) <= 0:
        embed = discord.Embed(
        description= f'{price} is not a valid price. Please try again.',
        color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
        )   
        await interaction.response.send_message(embed=embed)
        return

    for stock in allStonkDict:
        if stock == ticker:
            if str(allStonkDict[stock][1] == str(interaction.user.id)):
                # delete_key(ticker)
                allStonkDict[ticker] = (price, interaction.user.id, specifier)
                (allStonkDict)

                embed = discord.Embed(
                    description=f'{ticker} has been edited to track for when it goes {specifier} {price}.',
                    color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
                )
                await interaction.response.send_message(embed=embed)
                rewrite()
                return
    embed = discord.Embed(title=f'{ticker} was not found in your list.',)
    await interaction.response.send_message(embed=embed)

    
    
@client.tree.command()
@app_commands.describe(
    ticker='The ticker symbol of the stock you want to add',
    price='The price you want to buy the stock at',
    specifier='For wanting to be notified if the stock goes over or under the price'
)
@app_commands.choices(specifier=[app_commands.Choice(name='over', value='over'),
                                app_commands.Choice(name='under', value='under')])
async def add(interaction: discord.Interaction, ticker: str, price: str, specifier: app_commands.Choice[str]):
    """For adding a stock."""

    specifier = specifier.value
    ticker = ticker.upper()

    # Checks if the ticker is valid
    if ticker not in stonkList:
        embed = discord.Embed(
        description= f'{ticker} is not a valid ticker symbol. Please try again.',
        color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
        )   
        await interaction.response.send_message(embed=embed)
        return
    
    # Check if the ticker is already in the user's list
    for stock in allStonkDict:
        if stock == ticker:
            if str(allStonkDict[stock][1] == str(interaction.user.id)):
                embed = discord.Embed(
                    description=f'{ticker} is already in your list. Use /edit to change the target price.',
                    color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
                )
                await interaction.response.send_message(embed=embed)
                return
    
    # Checks if the price is valid
    if not floatable(price) or float(price) <= 0:
        embed = discord.Embed(
        description= f'{price} is not a valid price. Please try again.',
        color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
        )   
        await interaction.response.send_message(embed=embed)
        return

    allStonkDict[ticker] = (price, interaction.user.id, specifier)

    embed = discord.Embed(
            description=f'Added {ticker}, will notify when the price reaches or goes {specifier} {price}.',
            color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
    )
    await interaction.response.send_message(embed=embed)
    rewrite()



with open('config.json', 'r') as cfg:
# Deserialize the JSON data (essentially turning it into a Python dictionary object so we can use it in our code) 
    data = json.load(cfg) 
TOKEN = data["token"]
#token goes here
client.run(TOKEN)

