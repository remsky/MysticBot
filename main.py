"""
Main entrypoint
"""
import os

import discord

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)


@bot.slash_command(
    name="repeatafterme",
    description="Test function that repeats your message backwards")
async def repeatafterme(ctx, message):
  await ctx.respond(message[::-1])


@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return


token = os.getenv("BOT_TOKEN")
# bot.load_extension("cogs.github_cog")
bot.load_extension("cogs.jira_cog")
bot.run(token)
