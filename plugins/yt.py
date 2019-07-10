import discord
import asyncio
import importlib
import urllib
import re

NAME="yt"
ytrerollcache={}


def doYT(arg):
    query_string = urllib.parse.urlencode({"search_query" : arg})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    return search_results


class YouTube:
    def __init__(self, logger, client, pluginSet):
        self.NAME="yt"
        logger(NAME, "Initializing YouTube plugin")
        self.pluginSet=pluginSet
    
    def canHandle(self, cmd, fullmessage):
        return cmd=="!yt" or cmd=="!ytreroll" or cmd=="!ytplay"
    
    async def handle(self, message, channel, args, cmd):
        arg=args
        #print("In handle()")
        if cmd=="!ytreroll":
            try:
                ytresults=ytrerollcache[message.author.name]
                idx=randint(1, len(ytresults)-1)
                yt=ytresults[idx]
                ytresults.remove(yt)
                ytrerollcache[message.author.name]=ytresults
                await channel.send("http://www.youtube.com/watch?v=" + yt)
            except:
                await channel.send("Out of cache entries or no query found, %s." % message.author.mention)
        elif cmd=="!yt" or cmd=="!ytplay":
            if len(arg)==0:
                    await channel.send("Usage: !yt search-query")
            else:
                ytresults=doYT(arg)
                yt=ytresults[0]
                ytresults.remove(yt)
                ytrerollcache[message.author.name]=ytresults
                if cmd=="!ytplay":
                    for p in self.pluginSet.plugins:
                        if p.canHandle("!play", None):
                            await p.handle(message, channel, "http://www.youtube.com/watch?v=%s" % yt, "!play")
                            break
                await channel.send("Found %d results:\n http://www.youtube.com/watch?v=%s" % (len(ytresults), yt))
            
    
    def getHelp(self):
        return "!yt searches for a YouTube video\n!ytreroll displays the next searched YouTube video\n!ytplay plays first youtube result if play.py plugin is installed"

INST=YouTube
