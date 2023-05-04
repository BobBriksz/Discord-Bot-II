import discord
from discord.ext import commands
import random
import os
import transformers
from transformers import pipeline
from transformers import Conversation

BOT_TOKEN = os.environ['BOT_TOKEN']



description = """My second attempt at a bot, I will try to implement GPT and llm to this to make 
it a fun bot to use in a variety of ways """

#loading pretrained language model
model = pipeline('conversational', model='facebook/blenderbot-400M-distill')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


bot = commands.Bot(command_prefix="?", description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'logged in as {bot.user} (ID: {bot.user.id})')
    print("---------")


@bot.command()
async def chat(ctx):
    await ctx.send("lets start a conversation! type your message or 'quit'")

    # create conversation object
    conversation = Conversation()

    #loop till user types quit

    while True:
        def check_message(message):
            return message.author == ctx.author and message.channel == ctx.channel
        user_input = await bot.wait_for('message',check=check_message)
        # add user input to conversation object
        conversation.add_user_input(user_input.content)

        if user_input.content.lower() =='quit':
            break
        bot_response = model(conversation).generated_responses[-1]
        await ctx.send(bot_response)


bot.run(BOT_TOKEN)