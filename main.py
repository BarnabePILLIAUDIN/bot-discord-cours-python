import discord
import requests
import time
import	random



#fonctionalités :
#Répond feur aux "quoi"
#Message de bienvenue
#Message quand il est prêt
#!Blague
#!nick & nick-bot
#!roullette-russe

intents = discord.Intents.all()
intents.bans=True
client = discord.Client(intents=intents)

#constantes qui permettent de changer le bot de server
HELLO_MESSAGE="La team roquette est de retour pour vous jouer un mauvais tours"
#id of the welcome chanel
WELCOME_ID = 1042750176219119687
BOT_ID= 1042716464991440956
#id of the server owner
OWNER_ID = 326795337190735872
#server id
GUILD_ID = 1042714931969151026
#Y mettre le token
TOKEN = "insérer un token ici"
#Toute les commandes et leurs descrition
COMMANDS=["- !blague te raconte un blague","- !nick te changes ton pseudo par un pseudo aléatoire","- !roulette-russe exclue un menbre au hazard",
"- !commandes Pas besoins de t'expliquer tu viens de le faire"]


#Quand le bot est prêt il le dit dans la console et envoie un message dans le channel

@client.event
async def on_ready():
  welcome_chanel = client.get_channel(WELCOME_ID)
  await welcome_chanel.send(HELLO_MESSAGE)
  print("Je suis prêt")

#quand un message est envoyé il vérifie si c'est une commande ou s'il finit par quoi
@client.event
async def on_message(message):
  #s'il finit par quoi il répond feur
  if "quoi" in message.content.lower()[-6:]:
    await message.channel.send("feur")
  
  #si l'utilisateur entre la commande blague il va faire un requette à une api que va retourner un blague et un chute
  if message.content.startswith("!blague"):
    response = requests.get('https://api.blablagues.net/?rub=blagues').json()
    joke_data =  response["data"]["content"]
    joke= joke_data["text_head"]+ "\n" 
    await message.channel.send(joke)
    punchline = joke_data["text"]+joke_data["text_hidden"]
    #la chute arrive au bout de 3 secondes
    time.sleep(3)
    await message.channel.send(punchline)
  
  #la commande nick permet de se renomer avec un nom aléatoir. Le bot fera une requette à une api qui renvera un nom aléatoire
  if message.content[:6].startswith("!nick "):
    response = requests.get("https://randomuser.me/api/?results=1").json()
    name_data = response["results"][0]["name"]
    name= name_data["first"] + " "+name_data["last"]
    author = client.get_guild(GUILD_ID).get_member(message.author.id)
    author_name = author.name
    await author.edit(nick=name)
    await message.channel.send(f"{author_name} s'appel désormais {name}")

  #permet de demander au bot de se renomer
  if message.content.startswith("nick-bot"):
    await message.channel.send("!nick")

  #commande de la roulette russe. Un menbre du serveur (connecté ou non pas de moyense de se protéger) choisit de manière aléatoir est expulsé du serveur
  if message.content.startswith("!roulette-russe"):
    members = client.get_all_members()
    ids=[]
    #cette chaine de caractère contiendra tout les noms et servira à indiquer à tout le monde qu'une roulette russe à été lancée
    names= ""
    #On parcours la liste des utilisateurs
    for member in members:
      #le bot ne peut ni bannir le fondateur du serveur ni lui même
      if member.id == BOT_ID or member.id == OWNER_ID : 
        continue
      else :
        #Si l'utilisateur n'est ni le bot ni le fondateur son id est ajouté à un tableau 
        names+= member.name+", "
        ids.append(member.id)
    names= names[:-2]
    await message.channel.send("Qui de "+names+" va être expulser du serveur")
    #le dernier id du tableau permet de choisir un élément du tableu aléatoire sans risquer d'avoir un index trop grand
    last_id = len(ids)-1
    victim_id = random.randint(0,last_id)
    #représente l'utilisateur qui va être expulsé
    victim = client.get_guild(GUILD_ID).get_member(ids[victim_id])
    time.sleep(5)
    await message.channel.send("Et la foudre s'abattit sur "+victim.mention)
    #Aprés 5 secondes de suspence le nom de la victime est révélé et la sentence tombe
    await victim.kick(reason="La foudre s'est abattue sur toi!")

    #Donne toute les commandes
  if message.content.startswith("!commandes"):
    await message.channel.send(f"{message.author.mention}Les commande sont:")
    print("commandes")
    for cmd in COMMANDS:
      await message.channel.send(cmd)

#Message de bienvenue quand quelqu'un rejoins le server
@client.event
async def on_member_join(member):
  welcome_chanel = client.get_channel(1042750176219119687)
  await welcome_chanel.send(f"Bienvenue {member.mention}!")


client.run(TOKEN)
