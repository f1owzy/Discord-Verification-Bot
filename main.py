import discord
import json

with open('config.json', 'r') as f:
    config = json.load(f)

unverified_role_id = config['unverified_role_id']
verified_role_id = config['verified_role_id']

command_prefix = config['command_prefix']

client = discord.Client()

verified_count = 0

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(command_prefix):
        command = message.content.split()[0].lstrip(command_prefix)
        args = message.content.split()[1:]

        if command == 'access':
            user = message.author
            server = message.guild

            unverified_role = server.get_role(unverified_role_id)
            verified_role = server.get_role(verified_role_id)

            if verified_role in user.roles:
                embed = discord.Embed(title="", description="You already have access", color=0xFF0000)
                await message.channel.send(embed=embed)
            else:
                await user.remove_roles(unverified_role)
                await user.add_roles(verified_role)

                global verified_count
                verified_count += 1

                embed = discord.Embed(title="", description="Gave Users Role!", color=0x00FF00)
                await message.channel.send(embed=embed)

        elif command == 'help':
            embed = discord.Embed(title="setup", description="To Gain Access Type .access", color=0x008000)
            embed.add_field(name="Verified Count", value=str(verified_count), inline=False)
            await message.channel.send(embed=embed)

        elif command == 'verifycount':
            embed = discord.Embed(title="", description="Verified count: {}".format(verified_count), color=0x008000)
            await message.channel.send(embed=embed)

client.run(config['token'])
