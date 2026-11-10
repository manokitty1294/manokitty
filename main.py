import os
import random
import discord
from discord.ext import commands

# Configure bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Simple XP storage for leveling system: {user_id: xp}
user_xp = {}


@bot.event
async def on_ready():
  print(f"✨ {bot.user.name} is online, flawless, and ruling the server! ✨")
  await bot.change_presence(
      activity=discord.Activity(
          type=discord.ActivityType.watching,
          name="over my aesthetic empire ✨",
      )
  )


@bot.event
async def on_member_join(member):
  # Bratty & welcoming greeting
  channel = member.guild.system_channel
  if channel:
    embed = discord.Embed(
        title="Ugh, a new newcomer? 💅",
        description=(
            f"Look who finally decided to show up: {member.mention}! Don't"
            " touch my setup, keep the chat aesthetic, and grab your roles"
            " before I lose my patience."
        ),
        color=0xFFB6C1,  # Aesthetic light pink
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text="Stay clean or get muted ✨ — manokitty")
    await channel.send(embed=embed)


@bot.event
async def on_message(message):
  if message.author.bot:
    return

  # Simple XP / Leveling tracker
  user_id = message.author.id
  user_xp[user_id] = user_xp.get(user_id, 0) + random.randint(5, 15)

  await bot.process_commands(message)


@bot.command(name="rank", help="Check your current aesthetic rank and XP.")
async def rank(ctx):
  user_id = ctx.author.id
  xp = user_xp.get(user_id, 0)
  level = xp // 100

  embed = discord.Embed(
      title=f"👑 {ctx.author.name}'s Aesthetic Status",
      description=(
          f"Ugh, let's see how much effort you've put in...\n\n✨ **XP:**"
          f" `{xp}`\n✨ **Level:** `{level}`"
      ),
      color=0xFFC0CB,
  )
  embed.set_footer(text="At least you're trying to look good.")
  await ctx.send(embed=embed)


@bot.command(
    name="pat", help="Give someone a headpat (or get patted if you're lucky)."
)
async def pat(ctx, member: discord.Member = None):
  if member is None:
    member = ctx.author

  responses = [
      (
          f"*{bot.user.name} reluctantly gives {member.mention} a gentle"
          " headpat.* Don't ruin my hair, okay?"
      ),
      (
          f"*{bot.user.name} pats {member.mention} patronizingly.* Well, you're"
          " almost aesthetic enough to deserve that."
      ),
      (
          f"*{bot.user.name} gently pats {member.mention}.* Ugh, fine! You"
          " behaved nicely today."
      ),
  ]

  embed = discord.Embed(
      description=random.choice(responses), color=0xFFC0CB
  )
  await ctx.send(embed=embed)


@bot.command(name="kick", help="Kick a messy member out of the server.")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Being totally unaesthetic."):
  await member.kick(reason=reason)
  embed = discord.Embed(
      title="🧹 Swept Away!",
      description=(
          f"Bye-bye, {member.mention}! They couldn't handle the standards."
          f" Reason: `{reason}`"
      ),
      color=0xFF69B4,
  )
  await ctx.send(embed=embed)


@kick.error
async def kick_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send(
        "Nice try, peasant! You don't have permission to use my kick command."
        " 💅"
    )


@bot.command(name="ban", help="Permanently ban a chaotic member.")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Zero aesthetic value."):
  await member.ban(reason=reason)
  embed = discord.Embed(
      title="🚫 Permanently Banned!",
      description=(
          f"Out of my sight, {member.mention}! Cleaned them right out of my"
          f" database. Reason: `{reason}`"
      ),
      color=0xFF0000,
  )
  await ctx.send(embed=embed)


@ban.error
async def ban_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send(
        "You think you have the power to ban people here? Cute, but no. 💅"
    )


# Run the bot using the environment variable TOKEN on Render
TOKEN = os.getenv("TOKEN")
if TOKEN:
  bot.run(TOKEN)
else:
  print(
      "Error: No TOKEN found! Make sure to add your TOKEN environment variable"
      " on Render."
  )
  
