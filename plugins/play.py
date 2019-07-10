import discord
import os
import sys
import asyncio
import youtube_dl

NAME="play"

class ShockPlayer:
    def __init__(self, logger, client, pluginSet):
        self.NAME="play"
        self.client=client
        self.logger=logger
        self.playQueue=[]
        logger(NAME, "Initializing YouTube VC Player")
    
    def canHandle(self, cmd, fullmessage):
        return cmd=="!play" or cmd=="!stop" or cmd=="!playdir"
    
    async def handle(self, message, channel, args, cmd):
        arg=args
        arg=arg.strip()
        server=message.guild
        vcchannel=None
        for c in server.voice_channels:
            if c.name.lower()=="shockbot-radio":
                vcchannel=c
                break
        vc=None
        if vcchannel is not None:
            for c in self.client.voice_clients:
                if c.channel.id==vcchannel.id:
                    vc=c
                    break
        
        if vc is None:
            vc=await vcchannel.connect()
            
        if cmd=="!play":
            if vc.is_playing() and len(arg)!=0:
                self.playQueue.append((message, channel, args, cmd, vc))
                await channel.send("Added to play queue. The queue now has %d song(s)" % len(self.playQueue))
                
            else:
                if len(arg)!=0:
                    if os.path.isfile("song.flac"):
                        os.remove("song.flac")
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'flac',
                            'preferredquality': '192',
                        }],
                    }
                    
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        print("Arg=%s" % arg)
                        ydl.download([arg])
                        for file in os.listdir("./"):
                            if file.endswith(".flac"):
                                os.rename(file, 'song.flac')
                        vc.play(discord.FFmpegPCMAudio("song.flac"), after=lambda e: self.logger(self.NAME, "Finished playing song"))
                    else:
                        await channel.send("Usage: !play [song link]")
            
        elif cmd=="!stop":
            vc.stop()
            await vc.disconnect()
            await channel.send("%d items remaining in the song queue" % len(self.playQueue))
    
    def getHelp(self):
        return "!play plays a song\n!stop stops a currently playing song"
    
    async def update(self):
        newPQ=[]
        for elem in self.playQueue:
            message, channel, args, cmd, vc=elem
            if not vc.is_playing():
                await channel.send("Preparing to play the next song...")
                await self.handle(message, channel, args, cmd)
            else:
                newPQ.append(elem)
        self.playQueue=newPQ

INST=ShockPlayer
