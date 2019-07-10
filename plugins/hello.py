import discord
import asyncio

class Hello:
    def __init__(self, logger, client, pluginSet):
        self.NAME="hello"
        logger(self.NAME, "Initializing hello plugin")
    
    def canHandle(self, cmdStr, fullMessage):
        return cmdStr.lower()=="!hello"
    
    async def handle(self, message, channel, args, cmd):
        await channel.send('Hello {0.author.mention}'.format(message))
        return True
    
    def getHelp(self):
        return "!hello greets a user."

INST=Hello
