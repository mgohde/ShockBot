import discord
import asyncio

class Role:
    def __init__(self, logger, client, pluginSet):
        self.NAME="role"
        self.client=client
        logger(self.NAME, "Initializing role management plugin")
    
    def canHandle(self, cmd, fullMessage):
        return cmd=="!setrole" or cmd=="!listroles" or cmd=="!removerole"
    
    async def handle(self, message, channel, args, cmd):
        arg=args.strip().lower()
        server=message.guild
        user=message.author
        
        if cmd=="!listroles":
            outStr="Available roles:\n```"
            for elem in server.roles:
                # roles[0] is defined as @everyone, thus this bot will not set roles requiring special
                # permissions unless this check is removed:
                if elem.permissions==server.roles[0].permissions:
                    outStr+=elem.name+"\n"
            outStr+="```"
            
            await channel.send(outStr)
        
        elif cmd=="!setrole":
            # attempt to find the role in question:
            try:
                for elem in server.roles:
                    if elem.permissions==server.roles[0].permissions and elem.name.lower()==arg:
                        await user.add_roles(elem)
                        await channel.send("Role updated.")
                        break
            except:
                await channel.send("I'm either unable to set roles or this role doesn't exist.")
        
        elif cmd=="!removerole":
            try:
                for elem in server.roles:
                    if elem.permissions==server.roles[0].permissions and elem.name.lower()==arg:
                        await user.remove_roles(elem)
                        await channel.send("Role updated.")
                        break
            except:
                await channel.send("I'm either unable to set roles or this role doesn't exist.")
        
        return True
    
    def getHelp(self):
        return "!setrole role\n!listroles\n!removerole role"

INST=Role
