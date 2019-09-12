import discord
import random as r
import time as t
import datetime as dt
import DB
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
from operator import itemgetter

message_crime = ["Vous avez volé la Société Eltamar et vous êtes retrouvé dans un lac, mais vous avez quand même réussi à voler" #You robbed the Society of Schmoogaloo and ended up in a lake,but still managed to steal
,"Tu as volé une pomme qui vaut"
,"Tu as volé une carotte ! Prend tes"
, "Tu voles un bonbon ! Prend tes"
, "Tu as gangé au loto ! Prends tes"
, "J'ai plus d'idée prends ça:"]
# 4 phrases
message_gamble = ["Tu as remporté le pari ! Tu obtiens"
,"Une grande victoire pour toi ! Tu gagnes"
,"Bravo prends"
, "Heu...."
,"Pourquoi jouer à Fortnite quand tu peux gamble! Prends tes"]
# 4 phrases
# se sont les phrases prononcé par le bot pour plus de diversité
class Item:

	def __init__(self,nom,vente,achat,poids,idmoji,type):
		self.nom = nom
		self.vente = vente
		self.achat = achat
		self.poids = poids
		self.idmoji = idmoji
		self.type = type

objetItem = [Item("cobblestone",1,3,1,608748492181078131,"minerai")
,Item("iron",r.randint(9,11),30,5,608748195685597235,"minerai")
,Item("gold",r.randint(45, 56),100,10,608748194754723863,"minerai")
,Item("diamond",r.randint(98, 120),200,20,608748194750529548,"minerai")
,Item("emerald",r.randint(148, 175),320,30,608748194653798431,"minerai")
,Item("ruby",2000,3000,50,608748194406465557,"minerai")
,Item("fish",2,5,1,608762539605753868,"poisson")
,Item("tropicalfish",r.randint(25, 36),60,4,608762539030872079,"poisson")
,Item("blowfish",r.randint(25, 36),60,4,618058831863218176,"poisson")
,Item("octopus",50,90,8,618058832790421504,"poisson")
,Item("cookie",30,40,1,"","consommable")
,Item("grapes",15,25,1,"","consommable")
,Item("wine_glass",150,210,3,"","consommable")
,Item("backpack",1,5000,-100,616205834451550208,"special")]


class Outil:

	def __init__(self,nom,vente,achat,poids,durabilite,idmoji,type):
		self.nom = nom
		self.vente = vente
		self.achat = achat
		self.poids = poids
		self.durabilite = durabilite
		self.idmoji = idmoji
		self.type = type

objetOutil = [Outil("pickaxe",5,20,15,150,608748195291594792,"")
,Outil("iron_pickaxe",80,160,40,800,608748194775433256,"forge")
,Outil("fishingrod",5,15,25,200,608748194318385173,"")
,Outil("bank_upgrade",0,10000,10000,None,421465024201097237,"bank")]


class Recette:

	def __init__(self,nom,type, nb1,item1, nb2,item2, nb3,item3, nb4,item4):
		self.nom = nom
		self.type = type
		self.nb1 = nb1
		self.item1 = item1
		self.nb2 = nb2
		self.item2 = item2
		self.nb3 = nb3
		self.item3 = item3
		self.nb4 = nb4
		self.item4 = item4

objetRecette = [Recette("iron_pickaxe","forge",4,"iron",1,"pickaxe",0,"",0,"")]



class Trophy:

	def __init__(self,nom,desc,type,mingem):
		self.nom = nom
		self.desc = desc
		self.type = type
		self.mingem = mingem #nombre de gems minimum necessaire

objetTrophy = [Trophy("Gamble Jackpot", "`Gagner plus de 10000`:gem:` au gamble`","special",10000)
,Trophy("Super Jackpot :seven::seven::seven:", "`Gagner le super jackpot sur la machine à sous`", "special", 0)
,Trophy("Mineur de Merveilles", "`Trouvez un `<:gem_ruby:608748194406465557>`ruby`", "special", 0)
,Trophy("La Squelatitude", "`Avoir 2`:beer:` sur la machine à sous`", "special", 0)
,Trophy("Gems 500","`Avoir 500`:gem:","unique",500)
,Trophy("Gems 1k","`Avoir 1k`:gem:","unique",1000)
,Trophy("Gems 5k","`Avoir 5k`:gem:","unique",5000)
,Trophy("Gems 50k","`Avoir 50k`:gem:","unique",50000)
,Trophy("Gems 200k","`Avoir 200k`:gem:","unique",200000)
,Trophy("Gems 500k","`Avoir 500k`:gem:","unique",500000)
,Trophy("Gems 1M","`Avoir 1 Million`:gem:","unique",1000000)
,Trophy("Le Milliard !!!","`Avoir 1 Milliard`:gem:","unique",1000000000)]



class StatGems:

	def __init__(self,nom,desc):
		self.nom = nom
		self.desc = desc

objetStat = [StatGems("DiscordCop Arrestation","`Nombre d'arrestation par la DiscordCop`")
,StatGems("DiscordCop Amende","`Nombre d'ammende recue par la DiscordCop`")
,StatGems("Gamble Win", "`Nombre de gamble gagné`")
,StatGems("Super Jackpot :seven::seven::seven:", "`Nombre de super jackpot gagné sur la machine à sous`")
,StatGems("Mineur de Merveilles", "`Nombre de `<:gem_ruby:608748194406465557>`ruby` trouvé")
,StatGems("La Squelatitude", "`Avoir 2`:beer:` sur la machine à sous`")]

#anti-DB.spam
couldown_xxxl = 86400/6 # 4h
couldown_xl = 10
couldown_l = 8 # l pour long
couldown_c = 6 # c pour court
# nb de sec nécessaire entre 2 commandes


def get_idmogi(nameElem):
	"""
	Permet de connaitre l'idmoji de l'item
	"""
	test = False
	for c in objetItem:
		if c.nom == nameElem:
			test = True
			return c.idmoji

	for c in objetOutil:
		if c.nom == nameElem:
			test = True
			return c.idmoji
	if test == False:
		return 0



def addTrophy(ID, nameElem, nbElem):
	"""
	Permet de modifier le nombre de nameElem pour ID dans Trophy
	Pour en retirer mettez nbElemn en négatif
	"""
	trophy = DB.valueAt(ID, "trophy")
	if DB.nbElements(ID, nameElem, "trophy") > 0 and nbElem < 0:
		trophy[nameElem] += nbElem
	elif nbElem >= 0:
		if DB.nbElements(ID, nameElem, "trophy") == 0:
			trophy[nameElem] = nbElem
	else:
		# print("On ne peut pas travailler des élements qu'il n'y a pas !")
		return 404
	DB.updateField(ID, "trophy", trophy)



def testTrophy(ID, nameElem):
	"""
	Permet de modifier le nombre de nameElem pour ID dans les trophées
	Pour en retirer mettez nbElemn en négatif
	"""
	trophy = DB.valueAt(ID, "trophy")
	gems = DB.valueAt(ID, "gems")
	i = 2
	for c in objetTrophy:
		nbGemsNecessaire = c.mingem
		if c.type == "unique":
			if nameElem in trophy:
				i = 0
			elif gems >= nbGemsNecessaire:
				i = 1
				addTrophy(ID, c.nom, 1)
	return i



def addDurabilité(ID, nameElem, nbElem):
	"""
	"""
	durabilite = DB.valueAt(ID, "durabilite")
	if DB.nbElements(ID, nameElem, "inventory") > 0 and nbElem < 0:
		durabilite[nameElem] += nbElem
	elif nbElem >= 0:
		durabilite[nameElem] = nbElem
	else:
		# print("On ne peut pas travailler des élements qu'il n'y a pas !")
		return 404
	DB.updateField(ID, "durabilite", durabilite)



def get_durabilite(ID, nameElem):
	"""
	Permet de savoir la durabilite de nameElem dans l'inventaire de ID
	"""
	nb = DB.nbElements(ID, nameElem, "inventory")
	if nb > 0:
		durabilite = DB.valueAt(ID, "durabilite")
		for c in objetOutil:
			if nameElem == c.nom:
				if nameElem in durabilite:
					return durabilite[nameElem]
	else:
		return -1



def recette(ctx):
	"""Liste de toutes les recettes disponibles !"""
	d_recette="Permet de voir la liste de toutes les recettes disponible !\n\n"
	d_recette+="▬▬▬▬▬▬▬▬▬▬▬▬▬\n**Forge**\n"
	for c in objetOutil:
		for r in objetRecette :
			if c.type == "forge":
				if c.nom == r.nom:
					d_recette += "<:gem_{0}:{1}>`{0}`: ".format(c.nom,c.idmoji)
					if r.nb1 > 0:
						d_recette += "{0} <:gem_{1}:{2}>`{1}` ".format(r.nb1, r.item1, get_idmogi(r.item1))
					if r.nb2 > 0:
						d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb2, r.item2, get_idmogi(r.item2))
					if r.nb3 > 0:
						d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb3, r.item3, get_idmogi(r.item3))
					if r.nb4 > 0:
						d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb4, r.item4, get_idmogi(r.item4))
					d_recette += "\n"

	msg = discord.Embed(title = "Recettes",color= 15778560, description = d_recette)
	return msg


#===============================================================

class GemsBase(commands.Cog):

	def __init__(self,ctx):
		return(None)



	@commands.command(pass_context=True)
	async def begin(self, ctx):
		"""Pour t'ajouter dans la base de données !"""
		ID = ctx.author.id
		await ctx.channel.send(DB.newPlayer(ID))



	@commands.command(pass_context=True)
	async def bal(self, ctx, nom = None):
		"""**[nom]** | Êtes vous riche ou pauvre ?"""
		ID = ctx.author.id
		if DB.spam(ID,couldown_c, "bal"):
			#print(nom)
			if nom != None:
				ID = DB.nom_ID(nom)
				nom = ctx.guild.get_member(ID)
				nom = nom.name
			else:
				nom = ctx.author.name
			solde = DB.valueAt(ID, "gems")
			title = "Compte principale de {}".format(nom)
			msg = discord.Embed(title = title,color= 13752280, description = "")
			desc = "{} :gem:\n".format(solde)
			msg.add_field(name="Balance", value=desc, inline=False)

			DB.updateComTime(ID, "bal")
			await ctx.channel.send(embed = msg)
			return
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def baltop(self, ctx, n = 10):
		"""**[nombre]** | Classement des joueurs (10 premiers par défaut)"""
		ID = ctx.author.id
		if DB.spam(ID,couldown_c, "baltop"):
			UserList = []
			baltop = ""
			i = 0
			while i < DB.taille():
				user = DB.userID(i)
				gems = DB.userGems(i)
				UserList.append((user, gems))
				i = i + 1
			UserList = sorted(UserList, key=itemgetter(1),reverse=False)
			i = DB.taille() - 1
			j = 0
			while i >= 0 and j != n : # affichage des données trié
				baltop += "{2} | <@{0}> {1}:gem:\n".format(UserList[i][0], UserList[i][1], j+1)
				i = i - 1
				j = j + 1
			DB.updateComTime(ID, "baltop")
			msg = discord.Embed(title = "Classement des joueurs",color= 13752280, description = baltop)
			await ctx.channel.send(embed = msg)
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def buy (self, ctx,item,nb = 1):
		"""**[item] [nombre]** | Permet d'acheter les items vendus au marché"""
		ID = ctx.author.id
		if DB.spam(ID,couldown_c, "buy"):
			test = True
			nb = int(nb)
			for c in objetItem :
				if item == c.nom :
					test = False
					prix = 0 - (c.achat*nb)
					if DB.addGems(ID, prix) >= "0":
						DB.addInv(ID, c.nom, nb)
						if c.type != "consommable":
							msg = "Tu viens d'acquérir {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, c.idmoji)
						else:
							msg = "Tu viens d'acquérir {0} :{1}:`{1}` !".format(nb, c.nom)
					else :
						msg = "Désolé, nous ne pouvons pas executer cet achat, tu n'as pas assez de :gem: en banque"
					break
			for c in objetOutil :
				if item == c.nom :
					test = False
					if c.type == "bank":
						soldeMax = DB.nbElements(ID, "soldeMax", "banque")
						if soldeMax == 0:
							soldeMax = c.poids
							DB.addBank(ID, "soldeMax", c.poids)
						soldeMult = soldeMax/c.poids
						prix = 0
						i = 1
						while i <= nb:
							prix += c.achat*soldeMult
							soldeMult+=1
							i+=1
						prix = -1 * prix
						prix = int(prix)
					else:
						prix = -1 * (c.achat*nb)
					if DB.addGems(ID, prix) >= "0":
						if c.type == "bank":
							DB.addBank(ID, "soldeMax", nb*c.poids)
							msg = "Tu viens d'acquérir {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, c.idmoji)
							await ctx.channel.send(msg)
							return
						else:
							DB.addInv(ID, c.nom, nb)
							msg = "Tu viens d'acquérir {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, c.idmoji)
					else :
						msg = "Désolé, nous ne pouvons pas executer cet achat, tu n'as pas assez de :gem: en banque"
					break
			if test :
				msg = "Cet item n'est pas vendu au marché !"

			DB.updateComTime(ID, "buy")
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def sell (self, ctx,item,nb = 1):
		"""**[item] [nombre]** | Permet de vendre vos items !"""
		#cobble 1, iron 10, gold 50, diams 100
		ID = ctx.author.id
		# print(nb)
		# print(type(nb))
		if DB.spam(ID,couldown_c, "sell"):
			if int(nb) == -1:
				nb = DB.nbElements(ID, item, "inventory")
			nb = int(nb)
			if DB.nbElements(ID, item, "inventory") >= nb and nb > 0:
				test = True
				for c in objetItem:
					if item == c.nom:
						test = False
						gain = c.vente*nb
						DB.addGems(ID, gain)
						if c.type != "consommable":
							msg ="Tu as vendu {0} <:gem_{1}:{3}>`{1}` pour {2} :gem: !".format(nb,item,gain,c.idmoji)
						else:
							msg ="Tu as vendu {0} :{1}:`{1}` pour {2} :gem: !".format(nb,item,gain)
							if c.nom == "grapes" and int (nb/10) >= 1:
								nbwine = int(nb/10)
								DB.addInv(ID, "wine_glass", nbwine)
								msg+="\nTu gagne {}:wine_glass:`verre de vin`".format(nbwine)
						break
				for c in objetOutil:
					if item == c.nom:
						test = False
						gain = c.vente*nb
						DB.addGems(ID, gain)
						msg ="Tu as vendu {0} <:gem_{1}:{3}>`{1}` pour {2} :gem: !".format(nb,item,gain,c.idmoji)
						if DB.nbElements(ID, item, "inventory") == 1:
							addDurabilité(ID, item, -1)
						break

				DB.addInv(ID, item, -nb)
				if test:
					msg = "Cette objet n'existe pas"
			else:
				#print("Pas assez d'élement")
				msg = "Tu n'as pas assez de `{0}`. Il vous en reste : {1}".format(str(item),str(DB.nbElements(ID, item, "inventory")))

			DB.updateComTime(ID, "sell")
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def inv (self, ctx):
		"""Permet de voir ce que vous avez dans le ventre !"""
		ID = ctx.author.id
		nom = ctx.author.name
		if DB.spam(ID,couldown_c, "inv"):
			msg_inv = ""
			inv = DB.valueAt(ID, "inventory")
			tailletot = 0
			Titre = True
			for c in objetOutil:
				if Titre:
					msg_inv += "**Outils**\n"
					Titre = False
				for x in inv:
					if c.nom == str(x):
						if inv[x] > 0:
							msg_inv = msg_inv+"<:gem_{0}:{2}>`{0}`: `x{1}` | Durabilité: `{3}/{4}`\n".format(str(x), str(inv[x]), c.idmoji, get_durabilite(ID, c.nom), c.durabilite)
							tailletot += c.poids*int(inv[x])
			Titre = True
			for c in objetItem:
				if Titre:
					msg_inv += "\n**Items**\n"
					Titre = False
				for x in inv:
					if c.nom == str(x):
						if inv[x] > 0:
							if c.type != "consommable":
								msg_inv = msg_inv+"<:gem_{0}:{2}>`{0}`: `x{1}`\n".format(str(x), str(inv[x]), c.idmoji)
							else:
								msg_inv = msg_inv+":{0}:`{0}`: `x{1}`\n".format(str(x), str(inv[x]))
							tailletot += c.poids*int(inv[x])

			msg_inv += "\nTaille: `{}`".format(int(tailletot))
			msg_titre = "Inventaire de {}\n\n".format(nom)
			msg = discord.Embed(title = msg_titre,color= 6466585, description = msg_inv)
			DB.updateComTime(ID, "inv")
			await ctx.channel.send(embed = msg)
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def market (self, ctx):
		"""Permet de voir tout les objets que l'on peux acheter ou vendre !"""
		ID = ctx.author.id
		if DB.spam(ID,couldown_c, "market"):
			d_market="Permet de voir tout les objets que l'on peux acheter ou vendre !\n\n"
			Titre = True
			for c in objetOutil:
				if Titre:
					d_market += "**Outils**\n"
					Titre = False
				d_market += "<:gem_{0}:{3}>`{0}`: Vente **{1}** | Achat **{2}** ".format(c.nom,c.vente,c.achat,c.idmoji)
				if c.durabilite != None:
					d_market += "| Durabilité: **{}** ".format(c.durabilite)
				d_market += "| Poids **{}**\n".format(c.poids)
			Titre = True
			for c in objetItem :
				if Titre:
					d_market += "\n**Items**\n"
					Titre = False
				if c.type != "consommable":
					d_market += "<:gem_{0}:{4}>`{0}`: Vente **{1}** | Achat **{2}** | Poids **{3}**\n".format(c.nom,c.vente,c.achat,c.poids,c.idmoji)
				else:
					d_market += ":{0}:`{0}`: Vente **{1}** | Achat **{2}** | Poids **{3}**\n".format(c.nom,c.vente,c.achat,c.poids)

			msg = discord.Embed(title = "Le marché",color= 2461129, description = d_market)
			DB.updateComTime(ID, "market")
			await ctx.channel.send(embed = msg)
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def pay (self, ctx, nom, gain):
		"""**[nom] [gain]** | Donner de l'argent à vos amis !"""
		ID = ctx.author.id
		if DB.spam(ID,couldown_c, "pay"):
			try:
				if int(gain) > 0:
					gain = int(gain)
					don = -gain
					ID_recu = DB.nom_ID(nom)
					if int(DB.valueAt(ID, "gems")) >= 0:
						# print(ID_recu)
						DB.addGems(ID_recu, gain)
						DB.addGems(ID,don)
						msg = "<@{0}> donne {1}:gem: à <@{2}> !".format(ID,gain,ID_recu)
					else:
						msg = "<@{0}> n'a pas assez pour donner à <@{2}> !".format(ID,gain,ID_recu)

					DB.updateComTime(ID, "pay")
				else :
					msg = "Tu ne peux pas donner une somme négative ! N'importe quoi enfin !"
			except ValueError:
				msg = "La commande est mal formulée"
				pass
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def forge(self, ctx, item = None, nb = 1):
		"""**[item] [nombre]** | Permet de concevoir des items spécifiques"""
		ID = ctx.author.id
		if DB.spam(ID,couldown_c, "forge"):
			if item == None:
				msg = recette(ctx)
				await ctx.channel.send(embed = msg)
				return
			elif item == "iron_pickaxe":
				#print("iron: {}, pickaxe: {}".format(DB.nbElements(ID, "iron", "inventory"), DB.nbElements(ID, "pickaxe", "inventory")))
				nb = int(nb)
				nbIron = 4*nb
				nbPickaxe = 1*nb
				if DB.nbElements(ID, "iron", "inventory") >= nbIron and DB.nbElements(ID, "pickaxe", "inventory") >= nbPickaxe:
					DB.addInv(ID, "iron_pickaxe", nb)
					DB.addInv(ID, "pickaxe", -nbPickaxe)
					DB.addInv(ID, "iron", -nbIron)
					msg = "Bravo, tu as réussi à forger {0} <:gem_iron_pickaxe:608748194775433256>`iron_pickaxe` !".format(nb)
				elif DB.nbElements(ID, "iron", "inventory") < nbIron and DB.nbElements(ID, "pickaxe", "inventory") < nbPickaxe:
					msg = "tu n'as pas assez de <:gem_iron:{1}>`lingots de fer` et de <:gem_pickaxe:{2}>`pickaxe` pour forger {0} <:gem_iron_pickaxe:{3}>`iron_pickaxe` !".format(nb,get_idmogi("iron"), get_idmogi("pickaxe"), get_idmogi("iron_pickaxe"))
				elif DB.nbElements(ID, "iron", "inventory") < nbIron:
					nbmissing = (DB.nbElements(ID, "iron", "inventory") - nbIron)*-1
					msg = "Il te manque {0} <:gem_iron:{2}>`lingots de fer` pour forger {1} <:gem_iron_pickaxe:{3}>`iron_pickaxe` !".format(nbmissing, nb,get_idmogi("iron"), get_idmogi("iron_pickaxe"))
				else:
					nbmissing = (DB.nbElements(ID, "pickaxe", "inventory") - nbPickaxe)*-1
					msg = "Il te manque {0} <:gem_pickaxe:{2}>`pickaxe` pour forger {1} <:gem_iron_pickaxe:{3}>`iron_pickaxe` !".format(nbmissing, nb, get_idmogi("pickaxe"), get_idmogi("iron_pickaxe"))
			else:
				msg = "Impossible d'exécuter de forger cet item !"

			DB.updateComTime(ID, "forge")
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def trophy(self, ctx, nom = None):
		"""**[nom]** | Liste de vos trophées !"""
		ID = ctx.author.id
		if DB.spam(ID,couldown_c, "trophy"):
			if nom != None:
				ID = DB.nom_ID(nom)
			else:
				nom = ctx.author.mention
			d_trophy = ":trophy:Trophées de {}\n\n".format(nom)
			trophy = DB.valueAt(ID, "trophy")
			for c in objetTrophy:
				testTrophy(ID, c.nom)

			trophy = DB.valueAt(ID, "trophy")
			for c in objetTrophy:
				for x in trophy:
					if c.nom == str(x):
						if trophy[x] > 0:
							d_trophy += "•**{}**\n".format(c.nom)

			DB.updateComTime(ID, "trophy")
			msg = discord.Embed(title = "Trophées",color= 6824352, description = d_trophy)
			await ctx.channel.send(embed = msg)
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def trophylist(self, ctx):
		"""Liste de tout les trophées disponibles !"""
		ID = ctx.author.id
		d_trophy = "Liste des :trophy:Trophées\n\n"
		if DB.spam(ID,couldown_c, "trophylist"):
			for c in objetTrophy:
				if c.type != "unique" and c.type != "special":
					d_trophy += "**{}**: {}\n".format(c.nom, c.desc)
			d_trophy += "▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
			for c in objetTrophy:
				if c.type != "unique" and c.type == "special":
					d_trophy += "**{}**: {}\n".format(c.nom, c.desc)
			d_trophy += "▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
			for c in objetTrophy:
				if c.type == "unique" and c.type != "special":
					d_trophy += "**{}**: {}\n".format(c.nom, c.desc)

			DB.updateComTime(ID, "trophylist")
			msg = discord.Embed(title = "Trophées",color= 6824352, description = d_trophy)
			await ctx.channel.send(embed = msg)
		else:
			msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)

#===============================================================

class Gems(commands.Cog):

	def __init__(self,ctx):
		return(None)



	@commands.command(pass_context=True)
	async def daily(self, ctx):
		"""Récupère ta récompense journalière!"""
		ID = ctx.author.id
		DailyTime = DB.daily_data(ID, "dailytime")
		DailyMult = DB.daily_data(ID, "dailymult")
		jour = dt.date.today()
		if DailyTime == str(jour - dt.timedelta(days=1)):
			DB.updateDaily(ID, "dailytime", jour)
			DB.updateDaily(ID, "dailymult", DailyMult + 1)
			bonus = 125
			gain = 100 + bonus*DailyMult
			DB.addGems(ID, gain)
			msg = "Récompense journalière! Tu as gagné 100:gem:"
			msg += "\nNouvelle série: `{}`, Bonus: {}:gem:".format(DailyMult, bonus*DailyMult)

		elif DailyTime == str(jour):
			msg = "Tu as déja reçu ta récompense journalière aujourd'hui. Reviens demain pour gagner plus de :gem:"
		else:
			DB.updateDaily(ID, "dailytime", jour)
			DB.updateDaily(ID, "dailymult", 1)
			msg = "Récompense journalière! Tu as gagné 100 :gem:"
		if DailyTime != str(jour):
			for c in objetOutil:
				if c.type == "bank":
					Taille = c.poids
			solde = DB.nbElements(ID, "solde", "banque")
			soldeMax = DB.nbElements(ID, "soldeMax", "banque")
			if soldeMax == 0:
				soldeMax = Taille
			if solde > soldeMax:
				ARG2 = solde - soldeMax
				DB.addGems(ID, ARG2)
				nbgm = -1*ARG2
				DB.addBank(ID, "solde", nbgm)
				msg += "\n\nTon compte épargne a été débiter de {} :gem:\nCes :gem: ont été transférer sur ton compte principale".format(ARG2)
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def bank(self, ctx, ARG = None, ARG2 = None):
		"""
		Compte épargne
		"""
		ID = ctx.author.id
		if ARG != None:
			mARG = ARG.lower()
		else:
			mARG = "bal"
		msg = ""
		for c in objetOutil:
			if c.type == "bank":
				Taille = c.poids

		if mARG == "bal":
			if DB.spam(ID,couldown_c, "bank_bal"):
				if ARG2 != None:
					ID = DB.nom_ID(ARG2)
					nom = ctx.guild.get_member(ID)
					ARG2 = nom.name
					title = "Compte épargne de {}".format(ARG2)
				else:
					title = "Compte épargne de {}".format(ctx.author.name)
				solde = DB.nbElements(ID, "solde", "banque")
				soldeMax = DB.nbElements(ID, "soldeMax", "banque")
				if soldeMax == 0:
					soldeMax = Taille
				msg = discord.Embed(title = title,color= 13752280, description = "")
				desc = "{} / {} :gem:\n".format(solde, soldeMax)
				msg.add_field(name="Balance", value=desc, inline=False)

				desc = "**bank bal** *[name]* | Permet de connaitre la balance d'un utilisateur"
				desc += "\n**bank add** *[nombre]* | Permet d'ajouter ou d'enlever des :gem: de son compte épargne"
				desc += "\n**bank saving** | Permet de calculer son épargne (utilisable toute les 4h)"
				desc += "\n\nLe prix de la <:gem_{0}:{1}>`{0}` dépend du plafond du compte".format("bank_upgrade", get_idmogi("bank_upgrade"))
				msg.add_field(name="Commandes", value=desc, inline=False)
				await ctx.channel.send(embed = msg)
				DB.updateComTime(ID, "bank_bal")
				return
			else:
				msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)
			return

		elif mARG == "add":
			if DB.spam(ID,couldown_c, "bank_add"):
				if ARG2 != None:
					ARG2 = int(ARG2)
					gems = DB.valueAt(ID, "gems")
					solde = DB.nbElements(ID, "solde", "banque")
					soldeMax = DB.nbElements(ID, "soldeMax", "banque")
					if soldeMax == 0:
						soldeMax = Taille

					if ARG2 <= gems:
						soldeNew = solde + ARG2
						if soldeNew > soldeMax:
							ARG2 = ARG2 - (soldeNew - soldeMax)
							msg = "Plafond de {} :gem: du compte épargne atteint\n".format(soldeMax)
						elif soldeNew < 0:
							msg = "Le solde de ton compte épargne ne peux être négatif.\nSolde du compte: {} :gem:".format(solde)
							await ctx.channel.send(msg)
							return
						nbgm = -1*ARG2
						DB.addGems(ID, nbgm)
						DB.addBank(ID, "solde", ARG2)
						msg += "Ton compte épargne a été créditer de {} :gem:".format(ARG2)
						msg += "\nNouveau solde: {} :gem:".format(DB.nbElements(ID, "solde", "banque"))
						DB.updateComTime(ID, "bank_add")
					else:
						msg = "Tu n'as pas assez de :gem:`gems` pour épargner cette somme"
				else:
					msg = "Il manque le nombre de :gem: à ajouter sur votre compte épargne"
			else:
				msg = "Il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)
			return
		elif mARG == "saving":
			if DB.spam(ID,couldown_xxxl, "bank_saving"):
				if ARG2 != None:
					ID = DB.nom_ID(ARG2)
				else:
					solde = DB.nbElements(ID, "solde", "banque")
					soldeMax = DB.nbElements(ID, "soldeMax", "banque")
					if soldeMax == 0:
						soldeMax = Taille
					soldeMult = soldeMax/Taille
					soldeAdd = (0.20 + ( int(soldeMult)*0.01 ))*solde
					DB.addBank(ID, "solde", int(soldeAdd))
					msg = "Tu as épargné {} :gem:\nNouveau solde: {} :gem:".format(int(soldeAdd), DB.nbElements(ID, "solde", "banque"))

				DB.updateComTime(ID, "bank_saving")
			else:
				ComTime = DB.valueAt(ID, "com_time")
				if "bank_saving" in ComTime:
					time = ComTime["bank_saving"]
				time = time - (t.time()-couldown_xxxl)
				timeH = int(time / 60 / 60)
				time = time - timeH * 3600
				timeM = int(time / 60)
				timeS = int(time - timeM * 60)
				msg = "Il te faut attendre `{}h {}m {}s` avant d'épargner à nouveau !".format(timeH,timeM,timeS)
			await ctx.channel.send(msg)
			return




	@commands.command(pass_context=True)
	async def crime(self, ctx):
		"""Commets un crime et gagne des :gem: Attention au DiscordCop!"""
		ID = ctx.author.id
		if DB.spam(ID,couldown_l, "crime"):
			# si 10 sec c'est écoulé depuis alors on peut en  faire une nouvelle
			if r.randint(0,9) == 0:
				DB.addStatGems(ID, "DiscordCop Arrestation", 1)
				if int(DB.addGems(ID, -10)) >= 0:
					msg = "Vous avez été attrapés par un DiscordCop vous avez donc payé une amende de 10 :gem:"
				else:
					msg = "Vous avez été attrapés par un DiscordCop mais vous avez trop peu de :gem: pour payer une amende"
			else :
				gain = r.randint(2,8)
				msg = message_crime[r.randint(0,3)]+" "+str(gain)+":gem:"
				DB.addGems(ID, gain)

			DB.updateComTime(ID, "crime")
		else:
			msg = "Il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def gamble(self, ctx,valeur):
		"""**[valeur]** | Avez vous l'ame d'un parieur ?"""
		valeur = int(valeur)
		ID = ctx.author.id
		gems = DB.valueAt(ID, "gems")
		if valeur < 0:
			msg = "Je vous met un amende de 100 :gem: pour avoir essayé de tricher !"
			DB.addStatGems(ID, "DiscordCop Amende", 1)
			if gems > 100 :
				DB.addGems(ID, -100)
			else :
				DB.addGems(ID, 0-DB.valueAt(ID, "gems"))
			await ctx.channel.send(msg)
			return
		elif valeur > 0 and gems >= valeur:
			if DB.spam(ID,couldown_xl, "gamble"):
				if r.randint(0,3) == 0:
					gain = valeur*3
					# l'espérence est de 0 sur la gamble
					msg = message_gamble[r.randint(0,4)]+" "+str(gain)+":gem:"
					DB.addStatGems(ID, "Gamble Win", 1)
					for x in objetTrophy:
						if x.nom == "Gamble Jackpot":
							jackpot = x.mingem
					if gain >= jackpot:
						addTrophy(ID, "Gamble Jackpot", 1)
						msg += "Félicitation! Tu as l'ame d'un parieur, nous t'offrons le prix :trophy:`Gamble Jackpot`."
					DB.addGems(ID, gain)
				else:
					val = 0-valeur
					DB.addGems(ID,val)
					msg = "Dommage tu as perdu "+str(valeur)+":gem:"

				DB.updateComTime(ID, "gamble")
			else:
				msg = "Il faut attendre "+str(couldown_xl)+" secondes entre chaque commande !"
		elif gems < valeur:
			msg = "Tu n'as pas assez de :gem:`gems` en banque"
		else:
			msg = "La valeur rentré est incorrect"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def mine(self, ctx):
		"""Minez compagnons !!"""
		ID = ctx.author.id
		if DB.spam(ID,couldown_l, "mine"):
			#print(DB.nbElements(ID, "pickaxe", "inventory"))
			nbrand = r.randint(0,99)
			#----------------- Pioche en fer -----------------
			if DB.nbElements(ID, "iron_pickaxe", "inventory") >= 1:
				if get_durabilite(ID, "iron_pickaxe") == 0:
					addDurabilité(ID, "iron_pickaxe", -1)
					DB.addInv(ID,"iron_pickaxe", -1)
					if DB.nbElements(ID,"iron_pickaxe", "inventory") > 0:
						for c in objetOutil:
							if c.nom == "iron_pickaxe":
								addDurabilité(ID, c.nom, c.durabilite)
					msg = "Pas de chance tu as cassé ta <:gem_iron_pickaxe:{}>`pioche en fer` !".format(get_idmogi("iron_pickaxe"))
				else :
					if get_durabilite(ID,"iron_pickaxe") == None or get_durabilite(ID,"iron_pickaxe") < 0:
						for c in objetOutil:
							if c.nom == "iron_pickaxe":
								addDurabilité(ID, c.nom, c.durabilite)
					addDurabilité(ID, "iron_pickaxe", -1)
					if nbrand < 5:
						DB.addInv(ID, "emerald", 1)
						msg = "Tu as obtenu 1 <:gem_emerald:{}>`émeraude`".format(get_idmogi("emerald"))
					elif nbrand > 5 and nbrand < 15:
						DB.addInv(ID, "diamond", 1)
						msg = "Tu as obtenu 1 <:gem_diamond:{}>`diamant brut`".format(get_idmogi("diamond"))
						nbcobble = r.randint(0,5)
						if nbcobble != 0 :
							DB.addInv(ID, "cobblestone", nbcobble)
							msg += "\nTu as obtenu {} bloc de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble,get_idmogi("cobblestone"))
					elif nbrand > 15 and nbrand < 30:
						DB.addInv(ID, "gold", 1)
						msg = "Tu as obtenu 1 <:gem_gold:{}>`lingot d'or`".format(get_idmogi("gold"))
						nbcobble = r.randint(0,5)
						if nbcobble != 0 :
							DB.addInv(ID, "cobblestone", nbcobble)
							msg += "\nTu as obtenu {} bloc de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble,get_idmogi("cobblestone"))
					elif nbrand > 30 and nbrand < 60:
						DB.addInv(ID, "iron", 1)
						msg = "Tu as obtenu 1 <:gem_iron:{}>`lingot de fer`".format(get_idmogi("iron"))
						nbcobble = r.randint(0,5)
						if nbcobble != 0 :
							DB.addInv(ID, "cobblestone", nbcobble)
							msg += "\nTu as obtenu {} bloc de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble,get_idmogi("cobblestone"))
					elif nbrand >= 95:
						if r.randint(0,10) == 10:
							DB.addInv(ID, "ruby", 1)
							DB.addStatGems(ID, "Mineur de Merveilles", 1)
							addTrophy(ID, "Mineur de Merveilles", 1)
							msg = "En trouvant ce <:gem_ruby:{}>`ruby` tu deviens un Mineur de Merveilles".format(get_idmogi("ruby"))
						else:
							msg = "La pioche n'est pas très efficace pour miner la `dirt`"
					else:
						nbcobble = r.randint(1,10)
						DB.addInv(ID, "cobblestone", nbcobble)
						if nbcobble == 1 :
							msg = "Tu as obtenu 1 bloc de <:gem_cobblestone:{}>`cobblestone`".format(get_idmogi("cobblestone"))
						else :
							msg = "Tu as obtenu {} blocs de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble, get_idmogi("cobblestone"))

			#----------------- Pioche normal -----------------
			elif DB.nbElements(ID, "pickaxe", "inventory") >= 1:
				if get_durabilite(ID, "pickaxe") == 0:
					addDurabilité(ID, "pickaxe", -1)
					DB.addInv(ID,"pickaxe", -1)
					if DB.nbElements(ID,"pickaxe", "inventory") > 0:
						for c in objetOutil:
							if c.nom == "pickaxe":
								addDurabilité(ID, c.nom, c.durabilite)
					msg = "Pas de chance tu as cassé ta <:gem_pickaxe:{}>`pioche` !".format(get_idmogi("pickaxe"))
				else :
					if get_durabilite(ID,"pickaxe") == None or get_durabilite(ID,"pickaxe") < 0:
						for c in objetOutil:
							if c.nom == "pickaxe":
								addDurabilité(ID, c.nom, c.durabilite)
					addDurabilité(ID, "pickaxe", -1)
					if nbrand < 20:
						DB.addInv(ID, "iron", 1)
						msg = "Tu as obtenu 1 <:gem_iron:{}>`lingot de fer`".format(get_idmogi("iron"))
						nbcobble = r.randint(0,5)
						if nbcobble != 0 :
							DB.addInv(ID, "cobblestone", nbcobble)
							msg += "\nTu as obtenu {} bloc de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble,get_idmogi("cobblestone"))
					else:
						nbcobble = r.randint(1,10)
						DB.addInv(ID, "cobblestone", nbcobble)
						if nbcobble == 1 :
							msg = "Tu as obtenu 1 bloc de <:gem_cobblestone:{}>`cobblestone`".format(get_idmogi("cobblestone"))
						else :
							msg = "Tu as obtenu {} blocs de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble, get_idmogi("cobblestone"))
			else:
				msg = "Il faut acheter ou forger une pioche pour miner!"

			DB.updateComTime(ID, "mine")
		else:
			msg = "Il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def fish(self, ctx):
		"""Péchons compagnons !!"""
		ID = ctx.author.id
		if DB.spam(ID,couldown_l, "fish"):
			nbrand = r.randint(0,99)
			#print(DB.nbElements(ID, "fishingrod", "inventory"))
			if DB.nbElements(ID, "fishingrod", "inventory") >= 1:
				if get_durabilite(ID, "fishingrod") == 0:
					addDurabilité(ID, "fishingrod", -1)
					DB.addInv(ID,"fishingrod", -1)
					if DB.nbElements(ID,"fishingrod", "inventory") > 0:
						for c in objetOutil:
							if c.nom == "fishingrod":
								addDurabilité(ID, c.nom, c.durabilite)
					msg = "Pas de chance tu as cassé ta <:gem_fishingrod:{}>`canne à peche` !".format(get_idmogi("fishingrod"))
				else :
					if get_durabilite(ID,"fishingrod") == None or get_durabilite(ID,"fishingrod") < 0:
						for c in objetOutil:
							if c.nom == "fishingrod":
								addDurabilité(ID, c.nom, c.durabilite)
					addDurabilité(ID, "fishingrod", -1)

					if nbrand < 15:
						DB.addInv(ID, "tropicalfish", 1)
						msg = "Tu as obtenu 1 <:gem_tropicalfish:{}>`tropicalfish`".format(get_idmogi("tropicalfish"))
						nbfish = r.randint(0,3)
						if nbfish != 0:
							DB.addInv(ID, "fish", nbfish)
							msg += "\nTu as obtenu {} <:gem_fish:{}>`fish`".format(nbfish, get_idmogi("fish"))

					elif nbrand >= 15 and nbrand < 30:
						DB.addInv(ID, "blowfish", 1)
						msg = "Tu as obtenu 1 <:gem_blowfish:{}>`blowfish`".format(get_idmogi("blowfish"))
						nbfish = r.randint(0,3)
						if nbfish != 0:
							DB.addInv(ID, "fish", nbfish)
							msg += "\nTu as obtenu {} <:gem_fish:{}>`fish`".format(nbfish, get_idmogi("fish"))

					elif nbrand >= 30 and nbrand < 40:
						DB.addInv(ID, "octopus", 1)
						msg = "Tu as obtenu 1 <:gem_octopus:{}>`octopus`".format(get_idmogi("octopus"))

					elif nbrand >= 40 and nbrand < 95:
						nbfish = r.randint(1,7)
						DB.addInv(ID, "fish", nbfish)
						msg = "Tu as obtenu {} <:gem_fish:{}>`fish`".format(nbfish, get_idmogi("fish"))
					else:
						msg = "Pas de poisson pour toi aujourd'hui :cry: "
			else:
				msg = "Il te faut une <:gem_fishingrod:{}>`canne à pèche` pour pécher, tu en trouvera une au marché !".format(get_idmogi("fishingrod"))

			DB.updateComTime(ID, "fish")
		else:
			msg = "Il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def slots(self, ctx, imise = None):
		"""**[mise]** | La machine à sous, la mise minimum est de 10 :gem:"""
		ID = ctx.author.id

		if imise != None:
			if int(imise) < 0:
				msg = "Je vous met un amende de 100 :gem: pour avoir essayé de tricher !"
				DB.addStatGems(ID, "DiscordCop Amende", 1)
				if DB.valueAt(ID, "gems") > 100 :
					DB.addGems(ID, -100)
				else :
					DB.addGems(ID, 0-DB.valueAt(ID, "gems"))
				await ctx.channel.send(msg)
				return
			elif int(imise) < 10:
				mise = 10
			elif int(imise) > 100:
				mise = 100
			else:
				mise = int(imise)
		else:
			mise = 10

		if DB.spam(ID,couldown_xl, "slots"):
			tab = []
			result = []
			msg = "Votre mise: {} :gem:\n\n".format(mise)
			val = 0-mise
			for i in range(0,9):
				if i == 3:
					msg+="\n"
				elif i == 6:
					msg+=" :arrow_backward:\n"
				tab.append(r.randint(0,344))
				if tab[i] < 15 :
					result.append("zero")
				elif tab[i] >= 15 and tab[i] < 30:
					result.append("one")
				elif tab[i] >=  30 and tab[i] < 45:
					result.append("two")
				elif tab[i] >=  45 and tab[i] < 60:
					result.append("three")
				elif tab[i] >=  60 and tab[i] < 75:
					result.append("four")
				elif tab[i] >=  75 and tab[i] < 90:
					result.append("five")
				elif tab[i] >=  90 and tab[i] < 105:
					result.append("six")
				elif tab[i] >=  105 and tab[i] < 120:
					result.append("seven")
				elif tab[i] >=  120 and tab[i] < 135:
					result.append("eight")
				elif tab[i] >=  135 and tab[i] < 150:
					result.append("nine")
				elif tab[i] >=  150 and tab[i] < 170:
					result.append("gem")
				elif tab[i] >=  170 and tab[i] < 190:
					result.append("ticket")
				elif tab[i] >=  190 and tab[i] < 210:
					result.append("boom")
				elif tab[i] >=  210 and tab[i] < 220:
					result.append("apple")
				elif tab[i] >=  220 and tab[i] < 230:
					result.append("green_apple")
				elif tab[i] >=  230 and tab[i] < 240:
					result.append("cherries")
				elif tab[i] >=  240 and tab[i] < 250:
					result.append("tangerine")
				elif tab[i] >=  250 and tab[i] < 260:
					result.append("banana")
				elif tab[i] >=  260 and tab[i] < 280:
					result.append("grapes")
				elif tab[i] >=  280 and tab[i] < 310:
					result.append("cookie")
				elif tab[i] >=  310 and tab[i] < 340:
					result.append("beer")
				elif tab[i] >= 340 and tab[i] < 343:
					result.append("backpack")
				elif tab[i] >= 343:
					result.append("ruby")
				if tab[i] < 340:
					msg+=":{}:".format(result[i])
				else:
					msg+="<:gem_{}:{}>".format(result[i], get_idmogi(result[i]))
			msg += "\n"
			#===================================================================
			#Ruby (hyper rare)
			if result[3] == "ruby" or result[4] == "ruby" or result[5] == "ruby":
				DB.addInv(ID, "ruby", 1)
				DB.addStatGems(ID, "Mineur de Merveilles", 1)
				addTrophy(ID, "Mineur de Merveilles", 1)
				gain = 42
				msg += "\nEn trouvant ce <:gem_ruby:{}>`ruby` tu deviens un Mineur de Merveilles".format(get_idmogi("ruby"))
			#===================================================================
			#Super gain, 3 chiffres identique
			elif result[3] == "seven" and result[4] == "seven" and result[5] == "seven":
				gain = 1000
				DB.addStatGems(ID, "Super Jackpot :seven::seven::seven:", 1)
				addTrophy(ID, "Super Jackpot :seven::seven::seven:", 1)
				botplayer = discord.utils.get(ctx.guild.roles, id=532943340392677436)
				msg += "\n{} Bravo <@{}>! Le Super Jackpot :seven::seven::seven: est tombé :tada: ".format(botplayer.mention,ID)
			elif result[3] == "one" and result[4] == "one" and result[5] == "one":
				gain = 100
			elif result[3] == "two" and result[4] == "two" and result[5] == "two":
				gain = 150
			elif result[3] == "three" and result[4] == "three" and result[5] == "three":
				gain = 200
			elif result[3] == "four" and result[4] == "four" and result[5] == "four":
				gain = 250
			elif result[3] == "five" and result[4] == "five" and result[5] == "five":
				gain = 300
			elif result[3] == "six" and result[4] == "six" and result[5] == "six":
				gain = 350
			elif result[3] == "eight" and result[4] == "eight" and result[5] == "eight":
				gain = 400
			elif result[3] == "nine" and result[4] == "nine" and result[5] == "nine":
				gain = 450
			elif result[3] == "zero" and result[4] == "zero" and result[5] == "zero":
				gain = 500
			#===================================================================
			#Beer
			elif (result[3] == "beer" and result[4] == "beer") or (result[4] == "beer" and result[5] == "beer") or (result[3] == "beer" and result[5] == "beer"):
				DB.addStatGems(ID, "La Squelatitude", 1)
				addTrophy(ID, "La Squelatitude", 1)
				gain = 4
				msg += "\n<@{}> paye sa tournée :beer:".format(ID)
			#===================================================================
			#Explosion de la machine
			elif result[3] == "boom" and result[4] == "boom" and result[5] == "boom":
				gain = -50
			elif (result[3] == "boom" and result[4] == "boom") or (result[4] == "boom" and result[5] == "boom") or (result[3] == "boom" and result[5] == "boom"):
				gain = -10
			elif result[3] == "boom" or result[4] == "boom" or result[5] == "boom":
				gain = -2
			#===================================================================
			#Gain de gem
			elif result[3] == "gem" and result[4] == "gem" and result[5] == "gem":
				gain = 50
			elif (result[3] == "gem" and result[4] == "gem") or (result[4] == "gem" and result[5] == "gem") or (result[3] == "gem" and result[5] == "gem"):
				gain = 15
			elif result[3] == "gem" or result[4] == "gem" or result[5] == "gem":
				gain = 5
			#===================================================================
			#Tichet gratuit
			elif result[3] == "ticket" and result[4] == "ticket" and result[5] == "ticket":
				gain = 10
			elif (result[3] == "ticket" and result[4] == "ticket") or (result[4] == "ticket" and result[5] == "ticket") or (result[3] == "ticket" and result[5] == "ticket"):
				gain = 5
			elif result[3] == "ticket" or result[4] == "ticket" or result[5] == "ticket":
				gain = 2
			else:
				gain = 0
			#===================================================================
			#Cookie
			if result[3] == "cookie" and result[4] == "cookie" and result[5] == "cookie":
				DB.addInv(ID, "cookie", 3)
				msg += "\nTu a trouvé 3 :cookie:`cookies`"
			elif (result[3] == "cookie" and result[4] == "cookie") or (result[4] == "cookie" and result[5] == "cookie") or (result[3] == "cookie" and result[5] == "cookie"):
				DB.addInv(ID, "cookie", 2)
				msg += "\nTu a trouvé 2 :cookie:`cookies`"
			elif result[3] == "cookie" or result[4] == "cookie" or result[5] == "cookie":
				DB.addInv(ID, "cookie", 1)
				msg += "\nTu a trouvé 1 :cookie:`cookie`"
			#===================================================================
			#grappe
			if result[3] == "grapes" and result[4] == "grapes" and result[5] == "grapes":
				DB.addInv(ID, "grapes", 3)
				msg += "\nTu a trouvé 3 :grapes:`grapes`"
			elif (result[3] == "grapes" and result[4] == "grapes") or (result[4] == "grapes" and result[5] == "grapes") or (result[3] == "grapes" and result[5] == "grapes"):
				DB.addInv(ID, "grapes", 2)
				msg += "\nTu a trouvé 2 :grapes:`grapes`"
			elif result[3] == "grapes" or result[4] == "grapes" or result[5] == "grapes":
				DB.addInv(ID, "grapes", 1)
				msg += "\nTu a trouvé 1 :grapes:`grapes`"
			#===================================================================
			#Backpack (hyper rare)
			if result[3] == "backpack" or result[4] == "backpack" or result[5] == "backpack":
				DB.addInv(ID, "backpack", 1)
				p = 0
				for c in objetItem:
					if c.nom == "backpack":
						p = c.poids * (-1)
				msg += "\nEn trouvant ce <:gem_backpack:{0}>`backpack` tu gagne {1} points d'inventaire".format(get_idmogi("backpack"),p)

			#Calcul du prix
			prix = gain * mise
			if gain != 0 and gain != 1:
				if prix > 0:
					msg += "\nJackpot, vous venez de gagner {} :gem:".format(prix)
				else:
					msg += "\nLa machine viens d'exploser :boom:\nTu as perdu {} :gem:".format(-1*prix)
				DB.addGems(ID, prix)
			elif gain == 1:
				msg += "\nBravo, voici un ticket gratuit pour relancer la machine à sous"
				DB.addGems(ID, prix)
			else:
				msg += "\nLa machine à sous ne paya rien ..."
				DB.addGems(ID, val)
			DB.updateComTime(ID, "slots")
		else:
			msg = "Il faut attendre "+str(couldown_xl)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)


def setup(bot):
	bot.add_cog(GemsBase(bot))
	bot.add_cog(Gems(bot))
	open("fichier_txt/cogs.txt","a").write("GemsBase\n")
	open("fichier_txt/cogs.txt","a").write("Gems\n")
