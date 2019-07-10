import discord
import os
import sys
import asyncio
import urllib
from bs4 import BeautifulSoup

specsAllowed=['Engine', 'Exterior', 'Fuel', 'Cylinder', 'Curb', 'Drive']#, 'Transmission']

def isAllowed(s):
    for spec in specsAllowed:
        if s.startswith(spec):
            return True
    return False

class Specs:
    def __init__(self, logger, client, pluginSet):
        self.NAME="specs"
        logger(self.NAME, "Initializing car specs plugin")
        self.pluginSet=pluginSet
    
    def canHandle(self, cmd, fullmessage):
        return cmd=="!specs"
    
    async def handle(self, message, channel, args, cmd):
        arg=args
        argToks=arg.split()
        
        if cmd=='!specs':
            if len(argToks)<3:
                await channel.send("Usage: !specs year make model")
            else:
                try:
                    make=argToks[1].lower()
                    model=argToks[2].lower()
                    if len(argToks)>3:
                        model+="-%s" % argToks[3].lower()
                    year=argToks[0]
                    html=urllib.request.urlopen("https://www.autobytel.com/%s/%s/%s/specifications/" % (make, model, year)).read().decode()
                    parsed=BeautifulSoup(html)
                    lines=parsed.find_all('li')
                    filteredLines=[]
                    for l in lines:
                        if len(l)==5:
                            filteredLines.append(l)
                    outstr='```'
                    
                    for l in filteredLines:
                        toks=l.text.strip().split('\n')
                        # there are exactly two entries in a useful row:
                        if len(toks)==2 and isAllowed(toks[0]):
                            outstr+="%s %s\n" % (toks[0], toks[1])
                    
                    outstr+='```'
                    
                    await channel.send(outstr)
                except:
                    await channel.send("Unable to find information for a %s %s %s on Autobytel." % (year, make, model))
            
    
    def getHelp(self):
        return "!specs make model year"

INST=Specs
