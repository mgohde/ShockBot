 #/usr/bin/env python3
 # This is the main module for the new ShockValueBot. Hopefully it will feature substantial improvements over the old shockbot.
 
# Set of global imports:
import discord
import os
import sys
import subprocess
import multiprocessing
import asyncio
import importlib.util
import importlib

TOKEN = 'your token here'
administrators=['your discord username or usernames here']
pluginSet=None
helpStr=""
client=discord.Client()


def checkAdmin(userName):
    """Determines whether a given username matches an administrative whitelist."""
    for a in administrators:
        if userName==a:
            return True
    return False


def logFun(modName, message):
    """Logger function passed to plugins on init. This can be used to implement file-based logging."""
    print("(%s)\t%s" % (modName, message))


class Plugins:
    """Represents a set of loaded and instantiated plugins, as well as their associated python modules."""
    pluginMods=[]
    plugins=[]
    pluginNames="```"
    helpStr="```"
    
    def __init__(self, pluginDir):
        """Attempts to discover and load a set of plugins in the specified directory."""
        
        # Search for every possible plugin in the specified plugin directory:
        for elem in os.listdir(pluginDir):
            if elem.split('.')[-1]=='py':
                try:
                    self.pluginNames+="%s\n" % elem
                    modspec = importlib.util.spec_from_file_location("%s" % elem.rstrip('.py'), os.path.join(pluginDir, elem))
                    mod = importlib.util.module_from_spec(modspec)
                    modspec.loader.exec_module(mod)
                    self.pluginMods.append(mod)
                except:
                    print("[Plugins]\tUnable to load plugin module %s" % elem)
        
        self.pluginNames+="```"
        if not len(self.pluginMods):
            print("[Plugins]\tWarning: no plugins found!")
        
        # Attempt to instantiate those plugins by using the class reference contained in each properly
        # implemented module.
        for elem in self.pluginMods:
            try:
                p=elem.INST(logFun, client, self)
                print("[Plugins]\tInstantiating plugin %s" % p.NAME)
                self.helpStr+="%s\n" % p.getHelp()
                self.plugins.append(p)
            except:
                print("Plugin failed to init")
        self.helpStr+='```'


# discord.py tends to have problems with properly passing shared resources to event functions
# without implementing the entire bot as a class. As such, these are global for convenience.
# In the future, shockbot should be "properly" implemented
pluginList=Plugins('plugins')
pluginSet=pluginList.plugins
helpStr=pluginList.helpStr
pluginNames=pluginList.pluginNames

@client.event
async def on_message(message):
    # Yeaaaaaah, this bot should really be subclassed:
    global pluginList
    global pluginSet
    global helpStr
    global pluginNames
    
    channel=message.channel
    content=message.content
    
    if message.author == client.user:
        return
    
    else:
        contentToks=content.split()
        if len(contentToks):
            cmd=contentToks[0].lower()
            for p in pluginSet:
                if p.canHandle(cmd, message):
                    try:
                        await p.handle(message, channel, content.lstrip(cmd), cmd)
                    except:
                        e = sys.exc_info()[0]
                        print("[on_message]\t%s thrown by plugin %s." % (e, p.NAME))
                    break
            
            # There are a few internal commands that shouldn't need plugins:
            if cmd=="!help":
                await channel.send(helpStr)
                
            elif cmd=="!plugins":
                await channel.send(pluginList.pluginNames)
            
            elif cmd=="!reload":
                if checkAdmin(message.author.name.lower()):
                    for c in client.voice_clients:
                        #await c.stop()
                        await c.disconnect()
                    if message.author.dm_channel is None:
                        await message.author.create_dm()
                    await message.author.dm_channel.send("About to restart...\n")
                    python = sys.executable
                    os.execl(python, python, *sys.argv)
            
            elif cmd=="!shutdown":
                if checkAdmin(message.author.name.lower()):
                    if message.author.dm_channel is None:
                        await message.author.create_dm()
                    await message.author.dm_channel.send("Shutting down...\n")
                    for c in client.voice_clients:
                        await c.disconnect()
                    await client.logout()
                    sys.exit(0)
                    return


async def doPluginUpdates():
    """This gives allows each plugin to update or perform regularly scheduled work.
    """
    await client.wait_until_ready()
    while not client.is_closed():
        await asyncio.sleep(2)
        for p in pluginSet:
            try:
                await p.update()
            except:
                pass

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
    # Add our plugin update task:
    client.loop.create_task(doPluginUpdates())

client.run(TOKEN)
