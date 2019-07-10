import discord
import os
import sys
import subprocess
import multiprocessing
import asyncio

NAME="cowsay"
CMDSTR="!cowsay"

def doCowsay(text):
    arr=[]
    command=['cowsay', text]
    proc=subprocess.Popen(command, bufsize=1, stdout=subprocess.PIPE)
    for elem in proc.stdout:
        arr.append(elem.decode("utf-8"))
    
    msg="```"
    for elem in arr:
        msg+=elem
    msg+="```"
    
    return msg

class CowSay:
    def __init__(self, logger, client, pluginSet):
        self.NAME=NAME
        logger(NAME, "Initializing cowsay plugin")
    
    def canHandle(self, cmdStr, fullmessage):
        return cmdStr.lower()==CMDSTR
    
    async def handle(self, message, channel, args, cmd):
        if len(args)==0 or args.find('-')!=-1:
            await channel.send("Cowsay needs an argument")
        else:
            await channel.send(doCowsay(args))
        return True
    
    def getHelp(self):
        return "%s greets a user." % CMDSTR

INST=CowSay
