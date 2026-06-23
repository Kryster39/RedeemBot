import discord
from discord.ext import commands
import os
import re
from database import *

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

CODE_PATTERN = re.compile(r'^[A-Z0-9]+$')


@bot.event
async def on_ready():
    init_db()
    print(f"Bot online: {bot.user}")


# update
@bot.command()
async def update(ctx, *args):
    valid = [c for c in args if CODE_PATTERN.match(c)]
    new_codes = add_codes(valid)

    if new_codes:
        await ctx.send("新增: " + " ".join(new_codes))
    else:
        await ctx.send("沒有新增任何code")


# view
@bot.command()
async def view(ctx):
    user_id = str(ctx.author.id)
    unread = get_unread(user_id)

    if not unread:
        await ctx.send("沒有未讀")
        return

    mark_viewed(user_id, unread)
    await ctx.send(" ".join(unread))


# viewed
@bot.command()
async def viewed(ctx):
    user_id = str(ctx.author.id)
    data = get_user_codes(user_id, "viewed")

    if not data:
        await ctx.send("沒有已讀")
        return

    await ctx.send(" ".join(data))


# redeem
@bot.command()
async def redeem(ctx):
    user_id = str(ctx.author.id)
    viewed = get_user_codes(user_id, "viewed")

    if not viewed:
        await ctx.send("沒有可兌換")
        return

    await ctx.send("確定兌換？ yes/no")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", timeout=30, check=check)
    except:
        await ctx.send("逾時")
        return

    if msg.content.lower() != "yes":
        await ctx.send("取消")
        return

    mark_redeemed(user_id)
    await ctx.send("已兌換")


# redeemed
@bot.command()
async def redeemed(ctx):
    user_id = str(ctx.author.id)
    data = get_user_codes(user_id, "redeemed")

    if not data:
        await ctx.send("沒有已兌換")
        return

    await ctx.send(" ".join(data))


bot.run(TOKEN)