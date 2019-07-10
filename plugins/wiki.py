import discord
import asyncio
import wikipedia

NAME="wiki"
CMDSTR="!wiki"

class Wiki:
    def __init__(self, logger, client, pluginSet):
        self.NAME=NAME
        logger(NAME, "Initializing wikipedia search plugin")
    
    def canHandle(self, cmdStr, fullmessage):
        return cmdStr.lower()==CMDSTR
    
    async def handle(self, message, channel, args, cmd):
        arg=args.strip()
        if len(args)==0:
            await channel.send("!wiki requires args. Usage: !wiki query")
        else:
            try:
                await channel.send("```"+wikipedia.summary(arg, sentences=2)+"```")
            except wikipedia.exceptions.DisambiguationError as e:
                msg="```"
                for elem in e.options:
                    msg+=elem+"\n"
                msg+="```"
                await channel.send("Disambiguation error. Try one of the following: %s" % msg)
        return True
    
    def getHelp(self):
        return "!wiki query"

INST=Wiki
