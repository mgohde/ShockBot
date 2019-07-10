import discord
import os
import sys
import subprocess
import multiprocessing
import asyncio

NAME="units"
CMDSTR="!units"

def doUnits(uargs):
    arr=[]
    command=['units']
    command.extend(uargs)
    
    proc=subprocess.Popen(command, bufsize=1, stdout=subprocess.PIPE)
    for elem in proc.stdout:
        arr.append(elem.decode("utf-8"))
    
    msg="```"
    for elem in arr:
        msg+=elem
    msg+="```"
    
    return msg

class Units:
    def __init__(self, logger, client, pluginSet):
        self.NAME=NAME
        logger(NAME, "Initializing cowsay plugin")
    
    def canHandle(self, cmdStr, fullmessage):
        return cmdStr.lower()==CMDSTR
    
    async def handle(self, message, channel, args, cmd):
        args=args.strip()
        if len(args)==0 or args.find('-')!=-1:
            await channel.send("!units requires args. Usage: !units value unittype conversiontype")
        else:
            uargs=args.split()
            if len(uargs)==3:
                uargs=[uargs[0]+uargs[1], uargs[2]]
            if len(uargs)!=2:
                await channel.send("Sorry, I couldn't parse that. Usage: !units value unittype conversiontype")
            else:
                await channel.send(doUnits(uargs))
        return True
    
    def getHelp(self):
        return "!units [value] [unit] [unit to convert to]"

INST=Units
