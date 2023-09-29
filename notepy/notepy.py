import pronotepy
import discord
import datetime
import asyncio
from discord.ext import commands
from pronotepy.ent import ent_auvergnerhonealpe # exemple de région

sent_homework_ids = []

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

pronote = pronotepy.Client('https://lien-pronote.com',
                          username='surnom',
                          password='motdepasse',
                          ent=pronotepy.ent.ent_auvergnerhonealpe)

today = datetime.date.today()

# vérification de connection à pronote et au robot discord

if pronote.logged_in:
    print("CONNECTÉ À PRONOTE")
else:
    exit(1)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')

# commande !homework pour voir les devoirs non faits
@bot.command()
async def homework(ctx):
    homework = pronote.homework(today)
    unfinished_homework = [home for home in homework if not home.done]

    if unfinished_homework:
        embed = discord.Embed(title="Devoirs non faits", color=discord.Color.green())
        for home in unfinished_homework:
            subject = home.subject.name
            description = home.description

            embed.add_field(name=subject, value=f"**Description:** {description} `{home.date}`", inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send("Aucun devoir non fait trouvé dans Pronote.")
        print("Aucun nouveau devoir trouvé dans Pronote.")

# commande pour recevoir automatiquement le dernier nouveau message non lu/vu
@bot.command()
async def check_new_messages(ctx):
    messages = pronote.get_messages()

    if not messages:
        await ctx.send("Aucun nouveau message trouvé dans Pronote.")
        print("Aucun nouveau message trouvé dans Pronote.")
    else:
        target_channel = ctx.guild.get_channel(votre_canal_id)  # Remplacez 'votre_canal_id'
        if target_channel:
            for message in messages:
                if not message.seen:
                    await target_channel.send(f"Nouveau message de {message.author}: {message.content}")
                    message.mark_as_seen()

#commande pour recevoir automatiquement le.s dernier.s devoir.s non fait.s
@bot.command()
async def check_new_homeworks(ctx):
    homework_list = pronote.homework(datetime.date.today())

    if not homework_list:
        await ctx.send("Aucun nouveau devoir trouvé dans Pronote.")
        print("Aucun nouveau devoir trouvé dans Pronote.")
    else:
        target_channel = ctx.guild.get_channel(votre_canal_id)  # Remplacez 'votre_canal_id'
        if target_channel:
            for homework in homework_list:
                if homework.id not in sent_homework_ids:
                    message = await target_channel.send(f"Nouveau devoir pour {homework.subject}: {homework.description}")
                    await message.add_reaction("\U00002705")
                    sent_homework_ids.append(homework.id)

async def main():
    await bot.start('votre_token_bot')  # Remplacez 'votre_token_bot'

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
