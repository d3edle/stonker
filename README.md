# Stonker
# 📈Stonker

A discord bot that notifies you whenever a stock you've inputted reaches a specified price.

## ⚙️ Installing

### User install link:

https://discord.com/oauth2/authorize?client_id=1400561530159763586&response_type=code&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3D1400561530159763586%26scope%3Dbot&integration_type=1&scope=dm_channels.messages.read+dm_channels.messages.write+applications.commands+dm_channels.read

### Guild install link:

https://discord.com/oauth2/authorize?client_id=1400561530159763586

## Commands:

Use /add [ticker] [price] [over/under] to add a stock

- The ticker is not case-sensitive and must be traded on either NASDAQ, NYSE, or TSX
- The price is your target price
- "Over/under" is for specifying if you want to be notified for when the price goes over or under your specified price. 
Every half-hour, if a stock reaches your target price, you will be notified via DM.

Use /all to view all of your stocks, your target prices, and what prices they currrently trade at

Use /edit [ticker] [price] [over/under] to edit a stock's tracking.

Use /delete [ticker] to delete a stock. 

Use /clear to clear all of your stocks.

