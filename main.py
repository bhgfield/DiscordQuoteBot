import discord
import logging
import random
import traceback
from bot import ResponseBot

RANDOM_RESPONSE_CHANCE = 400


# Init discord client

token = ""
with open("token.txt", "r") as file:
    token = file.readline()

log_handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(log_handler=log_handler, intents=intents)    


# Load response bot quotes
bot = ResponseBot("quote_bank.tsv")


# Define discord client event handlers

@client.event
async def on_ready(self):
    bot.log("Logged in.")


@client.event
async def on_message(message: discord.Message):

    # Ignore own messages
    if message.author == client.user:
        return

    bot.log(f"[{message.author}] {message.content}")

    try:
        # Reply to bot
        if (message.type == discord.MessageType.reply
              and message.reference.cached_message
              and message.reference.cached_message.author == client.user):
            bot.log("Reply to bot detected. Getting reaction...")
            response = bot.get_response(message.content)
            
        # Mention bot
        elif client.user.mentioned_in(message):
            bot.log("Mention of bot detected. Getting reaction...")
            response = bot.get_response(message.content)
            
        # Random chance
        elif random.randint(0, RANDOM_RESPONSE_CHANCE) == 0:
            bot.log(f"Random chance activated. Getting reaction...")
            response = bot.get_response(message.content)
        
        # Check for word match
        else:
            bot.log("Searching for word-match...")
            response = bot.get_response(message.content, require_match=True)
        
        if not response: 
            bot.log(f"No response generated. Done.")
            return
        
        # Post response
        bot.log(f"Replying with \"{response}\"")
        await message.reply(response)
        bot.log("Done replying.")
        
    except Exception as exc:
        bot.log("Threw exception:")
        bot.log(traceback.format_exc())
            

client.run(token=token, log_handler=log_handler)


