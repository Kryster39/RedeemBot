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


# =========================
# upload (原 update)
# =========================
@bot.command()
async def upload(ctx, *args):
    valid = [c for c in args if CODE_PATTERN.match(c)]
    new_codes = add_codes(valid)

    if new_codes:
        await ctx.send("新增兌換碼: " + " ".join(new_codes))
    else:
        await ctx.send("沒有新增有效兌換碼")


# =========================
# viewall (原 viewed)
# =========================
@bot.command()
async def viewall(ctx):
    user_id = str(ctx.author.id)

    all_codes = get_all_codes()
    viewed = set(get_viewed(user_id))

    if not all_codes:
        await ctx.send("目前沒有兌換碼")
        return

    output = []
    new_unseen = []

    for code in all_codes:
        if code in viewed:
            output.append(code)
        else:
            output.append(f"{code}(new)")
            new_unseen.append(code)

    # 新看到的標記為已看過
    if new_unseen:
        mark_viewed(user_id, new_unseen)

    await ctx.send(" ".join(output))