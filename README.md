# ShockBot
A plugin-based discord bot developed for ease of use and modification.

# Installation
ShockBot is relatively simple to install and set up. All that is necessary is to edit shockbot2.py
and make the following changes:

1. Fill out TOKEN with your bot's user token
2. Fill out administrators with the discord usernames (without the trailing #number) of users
   who will be allowed to issue administrative commands for the bot.

## Requirements
ShockBot itself has minimal requirements:

1. discord.py >= 1.0 (ie. post-rewrite)
2. Python >= 3.7

It should be noted that the default ShockBot plugins may require additional libraries in order
to function, however it is not necessary to satisfy dependencies for plugins that you do not intend
to use.
