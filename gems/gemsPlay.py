import discord
import random as r
import time as t
import datetime as dt
from DB import TinyDB as DB, SQLite as sql
from gems import gemsFonctions as GF
from core import welcome as wel, level as lvl
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
from operator import itemgetter


class GemsPlay(commands.Cog):

	def __init__(self,ctx):
		return(None)



	@commands.command(pass_context=True)
	async def daily(self, ctx):
		"""Récupère ta récompense journalière!"""
		#=======================================================================
		# Initialisation des variables générales de la fonction
		#=======================================================================
		ID = ctx.author.id
		DailyTime = sql.valueAt(ID, "DailyTime", "daily")
		if DailyTime != 0:
			DailyTime = DailyTime[0]
		DailyMult = sql.valueAt(ID, "DailyMult", "daily")
		if DailyMult != 0:
			DailyMult = DailyMult[0]
		jour = dt.date.today()
		#=======================================================================
		# Détermination du daily
		#=======================================================================
		if DailyTime == str(jour - dt.timedelta(days=1)):
			sql.updateField(ID, "DailyTime", str(jour), "daily")
			sql.updateField(ID, "DailyMult", DailyMult + 1, "daily")
			if DailyMult >= 60:
				bonus = 500
			elif DailyMult >= 30:
				bonus = 200
			else:
				bonus = 125
			gain = 100 + bonus*DailyMult
			sql.addGems(ID, gain)
			msg = "Récompense journalière! Tu as gagné 100:gem:`gems`"
			msg += "\nNouvelle série: `{}`, Bonus: {} :gem:`gems`".format(DailyMult, bonus*DailyMult)
			lvl.addxp(ID, 10*(DailyMult/2), "gems")
			if DailyMult%30 == 0:
				m = (DailyMult//30)*5
				sql.addSpinelles(ID, m)
				msg+="\nBravo pour c'est {0} jours consécutifs :confetti_ball:! Tu as mérité {1}<:spinelle:{2}>`spinelles`".format(DailyMult, m, GF.get_idmoji("spinelle"))

		elif DailyTime == str(jour):
			msg = "Tu as déja reçu ta récompense journalière aujourd'hui. Reviens demain pour gagner plus de :gem:`gems`"
		else:
			sql.add(ID, "DailyMult", 1, "daily")
			sql.add(ID, "DailyTime", str(jour), "daily")
			msg = "Récompense journalière! Tu as gagné 100 :gem:`gems`"
			lvl.addxp(ID, 10, "gems")
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def bank(self, ctx, ARG = None, ARG2 = None):
		"""Compte épargne"""
		#=======================================================================
		# Initialistation des variables générales de la fonction
		#=======================================================================
		ID = ctx.author.id
		if ARG != None:
			mARG = ARG.lower()
		else:
			mARG = "bal"
		for c in GF.objetOutil:
			if c.type == "bank":
				Taille = c.poids
		msg = ""
		solde = sql.valueAt(ID, "Solde", "bank")
		if solde == 0:
			sql.add(ID, "SoldeMax", Taille, "bank")
		#=======================================================================
		# Affiche le menu principal de la banque
		# !bank bal <nom d'un joueur> permet de visualiser l'état de la banque de ce joueur
		#=======================================================================
		if mARG == "bal":
			if sql.spam(ID,GF.couldown_4s, "bank_bal", "gems"):
				if ARG2 != None:
					ID = sql.nom_ID(ARG2)
					nom = ctx.guild.get_member(ID)
					ARG2 = nom.name
					title = "Compte épargne de {}".format(ARG2)
				else:
					title = "Compte épargne de {}".format(ctx.author.name)
				solde = sql.valueAt(ID, "Solde", "bank")
				if solde != 0:
					solde = solde[0]
				soldeMax = sql.valueAt(ID, "SoldeMax", "bank")
				if soldeMax != 0:
					soldeMax = soldeMax[0]
				if soldeMax == 0:
					soldeMax = Taille
				msg = discord.Embed(title = title,color= 13752280, description = "")
				desc = "{} / {} :gem:`gems`\n".format(solde, soldeMax)
				msg.add_field(name="Balance", value=desc, inline=False)

				desc = "bank **bal** *[name]* | Permet de connaitre la balance d'un utilisateur"
				desc += "\nbank **add** *[+/- nombre]* | Permet d'ajouter ou d'enlever des :gem:`gems` de son compte épargne"
				desc += "\nbank **saving** | Permet de calculer son épargne (utilisable toute les 4h)"
				desc += "\n\nLe prix de la <:gem_{0}:{1}>`{0}` dépend du plafond du compte".format("bank_upgrade", GF.get_idmoji("bank_upgrade"))

				msg.add_field(name="Commandes", value=desc, inline=False)
				await ctx.channel.send(embed = msg)
				sql.updateComTime(ID, "bank_bal", "gems")
				return
			else:
				msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)
			return
		#=======================================================================
		# Ajoute ou enlève des Gems sur le compte épargne
		# un nombre positif ajoute des Gems
		# un nombre négatif enlève des Gems
		#=======================================================================
		elif mARG == "add":
			if sql.spam(ID,GF.couldown_4s, "bank_add", "gems"):
				if ARG2 != None:
					ARG2 = int(ARG2)
					gems = sql.valueAt(ID, "gems", "gems")[0]
					solde = sql.valueAt(ID, "Solde", "bank")
					if solde != 0:
						solde = solde[0]
					soldeMax = sql.valueAt(ID, "SoldeMax", "bank")
					if soldeMax != 0:
						soldeMax = soldeMax[0]
					if soldeMax == 0:
						soldeMax = Taille

					if ARG2 <= gems:
						soldeNew = solde + ARG2
						if soldeNew > soldeMax:
							ARG2 = ARG2 - (soldeNew - soldeMax)
							msg = "Plafond de {} :gem:`gems` du compte épargne atteint\n".format(soldeMax)
						elif soldeNew < 0:
							msg = "Le solde de ton compte épargne ne peux être négatif.\nSolde du compte: {} :gem:`gems`".format(solde)
							await ctx.channel.send(msg)
							return
						nbgm = -1*ARG2
						sql.addGems(ID, nbgm)
						sql.add(ID, "solde", ARG2, "bank")
						solde = sql.valueAt(ID, "Solde", "bank")
						if solde != 0:
							solde = solde[0]
						msg += "Ton compte épargne a été crédité de {} :gem:`gems`".format(ARG2)
						msg += "\nNouveau solde: {} :gem:`gems`".format(solde)
						sql.updateComTime(ID, "bank_add", "gems")
					else:
						msg = "Tu n'as pas assez de :gem:`gems` pour épargner cette somme"
				else:
					msg = "Il manque le nombre de :gem:`gems` à ajouter sur votre compte épargne"
			else:
				msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)
			return
		#=======================================================================
		# Fonction d'épargne
		# L'intéret est de 20% avec un bonus de 1% pour chanque bank_upgrade possédée
		#=======================================================================
		elif mARG == "saving":
			if sql.spam(ID,GF.couldown_4h, "bank_saving", "gems"):
				if ARG2 != None:
					ID = sql.nom_ID(ARG2)
				else:
					solde = sql.valueAt(ID, "Solde", "bank")
					if solde != 0:
						solde = solde[0]
					soldeMax = sql.valueAt(ID, "SoldeMax", "bank")
					if soldeMax != 0:
						soldeMax = soldeMax[0]
					if soldeMax == 0:
						soldeMax = Taille
					soldeMult = soldeMax/Taille
					pourcentage = 0.200 + soldeMult*0.002
					soldeAdd = pourcentage*solde
					soldeTaxe = GF.taxe(soldeAdd, 0.1)
					soldeAdd = soldeTaxe[1]
					sql.add(ID, "solde", int(soldeAdd), "bank")
					msg = "Tu as épargné {} :gem:`gems`\n".format(int(soldeAdd))
					soldeNew = solde + soldeAdd
					if soldeNew > soldeMax:
						soldeMove = soldeNew - soldeMax
						nbgm = -1 * soldeMove
						sql.addGems(ID, int(soldeMove))
						sql.add(ID, "solde", int(nbgm), "bank")
						msg += "Plafond de {} :gem:`gems` du compte épargne atteint\nTon épargne a été tranférée sur ton compte principal\n\n".format(soldeMax)
					solde = sql.valueAt(ID, "Solde", "bank")
					if solde != 0:
						solde = solde[0]
					msg += "Nouveau solde: {} :gem:`gems`".format(solde)

					D = r.randint(0,20)
					if D == 20 or D == 0:
						sql.add(ID, "lootbox_raregems", 1, "inventory")
						msg += "\nTu as trouvé une **Loot Box Gems Rare**! Utilise la commande `boxes open raregems` pour l'ouvrir"
					elif D >= 9 and D <= 11:
						sql.add(ID, "lootbox_commongems", 1, "inventory")
						msg += "\nTu as trouvé une **Loot Box Gems Common**! Utilise la commande `boxes open commongems` pour l'ouvrir"

					sql.addGems(wel.idBaBot,int(soldeTaxe[0]))

				sql.updateComTime(ID, "bank_saving", "gems")
				lvl.addxp(ID, 0.4, "gems")
			else:
				ComTime = sql.valueAt(ID, "bank_saving", "gems")
				if ComTime != 0:
					ComTime = float(ComTime[0])
				time = time - (t.time()-GF.couldown_4h)
				timeH = int(time / 60 / 60)
				time = time - timeH * 3600
				timeM = int(time / 60)
				timeS = int(time - timeM * 60)
				msg = "Il te faut attendre :clock2:`{}h {}m {}s` avant d'épargner à nouveau !".format(timeH,timeM,timeS)
			await ctx.channel.send(msg)
			return




	@commands.command(pass_context=True)
	async def crime(self, ctx):
		"""Commets un crime et gagne des :gem:`gems` Attention au DiscordCop!"""
		ID = ctx.author.id
		if sql.spam(ID,GF.couldown_6s, "crime", "gems"):
			# si 10 sec c'est écoulé depuis alors on peut en  faire une nouvelle
			if r.randint(0,9) == 0:
				sql.add(ID, "DiscordCop Arrestation", 1, "statgems")
				if int(sql.addGems(ID, -10)) >= 0:
					msg = "Vous avez été attrapés par un DiscordCop vous avez donc payé une amende de 10 :gem:`gems`"
				else:
					msg = "Vous avez été attrapés par un DiscordCop mais vous avez trop peu de :gem:`gems` pour payer une amende"
			else :
				gain = r.randint(2,8)
				jour = dt.date.today()
				if (jour.month == 10 and jour.day >= 23) or (jour.month == 11 and jour.day <= 10): #Special Halloween
					msg = "**Halloween** | Des bonbons ou un sort ?\n"
					msg += GF.message_crime[r.randint(0,3)]+" "+str(gain)
					if r.randint(0,1) == 0:
						msg += " :candy:`candy`"
						sql.add(ID, "candy", gain, "inventory")
					else:
						msg += " :lollipop:`lollipop`"
						sql.add(ID, "lollipop", gain, "inventory")
				else:
					msg = "{1} {0} :gem:`gems`".format(gain, GF.message_crime[r.randint(0,3)])
					sql.addGems(ID, gain)
			sql.updateComTime(ID, "crime", "gems")
			lvl.addxp(ID, 1, "gems")
		else:
			msg = "Il faut attendre "+str(GF.couldown_6s)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def gamble(self, ctx,valeur):
		"""**[valeur]** | Avez vous l'ame d'un parieur ?"""
		valeur = int(valeur)
		ID = ctx.author.id
		gems = sql.valueAt(ID, "gems", "gems")[0]
		if valeur < 0:
			msg = ":no_entry: Anti-cheat! Je vous met un amende de 100 :gem:`gems` pour avoir essayé de tricher !"
			slq.add(ID, "DiscordCop Amende", 1, "statgems")
			if gems > 100 :
				sql.addGems(ID, -100)
			else :
				sql.addGems(ID, -gems)
			await ctx.channel.send(msg)
			return
		elif valeur > 0 and gems >= valeur:
			if sql.spam(ID,GF.couldown_8s, "gamble", "gems"):
				if r.randint(0,3) == 0:
					gain = valeur*3
					# l'espérence est de 0 sur la gamble
					msg = "{1} {0} :gem:`gems`".format(gain, GF.message_gamble[r.randint(0,4)])
					sql.add(ID, "Gamble Win", 1, "statgems")
					for x in GF.objetTrophy:
						if x.nom == "Gamble Jackpot":
							jackpot = x.mingem
						elif x.nom == "Super Gamble Jackpot":
							superjackpot = x.mingem
						elif x.nom == "Hyper Gamble Jackpot":
							hyperjackpot = x.mingem
					if gain >= jackpot:
						sql.add(ID, "Gamble Jackpot", 1, "trophy")
						msg += "Félicitation! Tu as l'ame d'un parieur, nous t'offrons le prix :trophy:`Gamble Jackpot`."
					elif gain >= superjackpot:
						sql.add(ID, "Super Gamble Jackpot", 1, "trophy")
						msg += "Félicitation! Tu as l'ame d'un parieur, nous t'offrons le prix :trophy::trophy:`Super Gamble Jackpot`."
					elif gain >= hyperjackpot:
						sql.add(ID, "Hyper Gamble Jackpot", 1, "trophy")
						msg += "Félicitation! Tu as l'ame d'un parieur, nous t'offrons le prix :trophy::trophy::trophy:`Hyper Gamble Jackpot`."
					sql.addGems(ID, gain)
					D = r.randint(0,20)
					if D == 0:
						sql.add(ID, "lootbox_legendarygems", 1, "inventory")
						msg += "\nTu as trouvé une **Loot Box Gems Légendaire**! Utilise la commande `boxes open legendarygems` pour l'ouvrir"
					elif D >= 19:
						sql.add(ID, "lootbox_raregems", 1, "inventory")
						msg += "\nTu as trouvé une **Loot Box Gems Rare**! Utilise la commande `boxes open raregems` pour l'ouvrir"
					elif D >= 8 and D <= 12:
						sql.add(ID, "lootbox_commongems", 1, "inventory")
						msg += "\nTu as trouvé une **Loot Box Gems Common**! Utilise la commande `boxes open commongems` pour l'ouvrir"
				else:
					val = 0-valeur
					sql.addGems(ID,val)
					sql.addGems(wel.idBaBot, int(valeur))
					msg = "Dommage tu as perdu {} :gem:`gems`".format(valeur)

				sql.updateComTime(ID, "gamble", "gems")
				lvl.addxp(ID, 1, "gems")
			else:
				msg = "Il faut attendre "+str(GF.couldown_8s)+" secondes entre chaque commande !"
		elif gems < valeur:
			msg = "Tu n'as pas assez de :gem:`gems` en banque"
		else:
			msg = "La valeur rentré est incorrect"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def mine(self, ctx):
		"""Minez compagnons !!"""
		ID = ctx.author.id
		if sql.spam(ID,GF.couldown_6s, "mine", "gems"):
			if GF.testInvTaille(ID):
				nbrand = r.randint(0,99)
				nbDP = sql.valueAt(ID, "diamond_pickaxe", "inventory")
				if nbDP != 0:
					nbDP = nbDP[0]
				nbIP = sql.valueAt(ID, "iron_pickaxe", "inventory")
				if nbIP != 0:
					nbIP = nbIP[0]
				nbP = sql.valueAt(ID, "pickaxe", "inventory")
				if nbP != 0:
					nbP = nbP[0]
				#----------------- Pioche en diamant -----------------
				if nbDP >= 1:
					Durability = sql.valueAt(ID, "diamond_pickaxe", "durability")
					if Durability != 0:
						Durability = Durability[0]
					if Durability == 0:
						sql.add(ID, "diamond_pickaxe", -1, "inventory")
						if nbDP > 1:
							for c in GF.objetOutil:
								if c.nom == "diamond_pickaxe":
									sql.add(ID, c.nom, c.durabilite, "durability")
						msg = "Pas de chance tu as cassé ta <:gem_diamond_pickaxe:{}>`pioche en diamant` !".format(GF.get_idmoji("diamond_pickaxe"))
					else :
						sql.add(ID, "diamond_pickaxe", -1, "durability")
						if nbrand < 15:
							nbrand = r.randint(1,2)
							sql.add(ID, "emerald", nbrand, "inventory")
							msg = "Tu as obtenu {} <:gem_emerald:{}>`émeraude`".format(nbrand, GF.get_idmoji("emerald"))
							D = r.randint(0,20)
							if D < 2:
								sql.add(ID, "lootbox_legendarygems", 1, "inventory")
								msg += "\nTu as trouvé une **Loot Box Gems Légendaire**! Utilise la commande `boxes open legendarygems` pour l'ouvrir"
							elif D >= 17:
								sql.add(ID, "lootbox_raregems", 1, "inventory")
								msg += "\nTu as trouvé une **Loot Box Gems Rare**! Utilise la commande `boxes open raregems` pour l'ouvrir"

						elif nbrand > 15 and nbrand < 25:
							nbrand = r.randint(1,4)
							sql.add(ID, "diamond", nbrand, "inventory")
							msg = "Tu as obtenu {} <:gem_diamond:{}>`diamant brut`".format(nbrand, GF.get_idmoji("diamond"))
							nbcobble = r.randint(0,5)
							if nbcobble != 0 :
								sql.add(ID, "cobblestone", nbcobble, "inventory")
								msg += "\nTu as obtenu {} bloc de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble,GF.get_idmoji("cobblestone"))

						elif nbrand > 25 and nbrand < 50:
							nbrand = r.randint(1,6)
							sql.add(ID, "gold", nbrand, "inventory")
							msg = "Tu as obtenu {} <:gem_gold:{}>`lingot d'or`".format(nbrand, GF.get_idmoji("gold"))
							nbcobble = r.randint(0,5)
							if nbcobble != 0 :
								sql.add(ID, "cobblestone", nbcobble, "inventory")
								msg += "\nTu as obtenu {} bloc de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble,GF.get_idmoji("cobblestone"))

						elif nbrand > 50 and nbrand < 80:
							nbrand = r.randint(1,10)
							sql.add(ID, "iron", nbrand, "inventory")
							msg = "Tu as obtenu {} <:gem_iron:{}>`lingot de fer`".format(nbrand, GF.get_idmoji("iron"))
							nbcobble = r.randint(0,5)
							if nbcobble != 0 :
								sql.add(ID, "cobblestone", nbcobble, "inventory")
								msg += "\nTu as obtenu {} bloc de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble,GF.get_idmoji("cobblestone"))

						elif nbrand >= 90:
							nbrand =  r.randint(0,10)
							if nbrand >= 7:
								sql.add(ID, "ruby", 1, "inventory")
								sql.add(ID, "Mineur de Merveilles", 1, "statgems")
								sql.add(ID, "Mineur de Merveilles", 1, "trophy")
								msg = "En trouvant ce <:gem_ruby:{}>`ruby` tu deviens un Mineur de Merveilles".format(GF.get_idmoji("ruby"))
							elif nbrand < 2:
								msg = "La pioche n'est pas très efficace pour miner la `dirt`"
							else:
								nbcobble = r.randint(1,20)
								sql.add(ID, "cobblestone", nbcobble, "inventory")
								if nbcobble == 1 :
									msg = "Tu as obtenu 1 bloc de <:gem_cobblestone:{}>`cobblestone`".format(GF.get_idmoji("cobblestone"))
								else :
									msg = "Tu as obtenu {} blocs de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble, GF.get_idmoji("cobblestone"))
						else:
							nbcobble = r.randint(1,20)
							sql.add(ID, "cobblestone", nbcobble, "inventory")
							if nbcobble == 1 :
								msg = "Tu as obtenu 1 bloc de <:gem_cobblestone:{}>`cobblestone`".format(GF.get_idmoji("cobblestone"))
							else :
								msg = "Tu as obtenu {} blocs de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble, GF.get_idmoji("cobblestone"))

				#----------------- Pioche en fer -----------------
				elif nbIP >= 1:
					Durability = sql.valueAt(ID, "iron_pickaxe", "durability")
					if Durability != 0:
						Durability = Durability[0]
					if Durability == 0:
						sql.add(ID, "iron_pickaxe", -1, "inventory")
						if nbIP > 1:
							for c in GF.objetOutil:
								if c.nom == "iron_pickaxe":
									sql.add(ID, c.nom, c.durabilite, "durability")
						msg = "Pas de chance tu as cassé ta <:gem_iron_pickaxe:{}>`pioche en fer` !".format(GF.get_idmoji("iron_pickaxe"))
					else :
						sql.add(ID, "iron_pickaxe", -1, "durability")
						if nbrand < 5:
							sql.add(ID, "emerald", 1, "inventory")
							msg = "Tu as obtenu 1 <:gem_emerald:{}>`émeraude`".format(GF.get_idmoji("emerald"))
							D = r.randint(0,20)
							if D == 0:
								sql.add(ID, "lootbox_legendarygems", 1, "inventory")
								msg += "\nTu as trouvé une **Loot Box Gems Légendaire**! Utilise la commande `boxes open legendarygems` pour l'ouvrir"
							elif D >= 19:
								sql.add(ID, "lootbox_raregems", 1, "inventory")
								msg += "\nTu as trouvé une **Loot Box Gems Rare**! Utilise la commande `boxes open raregems` pour l'ouvrir"
							elif D >= 8 and D <= 12:
								sql.add(ID, "lootbox_commongems", 1, "inventory")
								msg += "\nTu as trouvé une **Loot Box Gems Common**! Utilise la commande `boxes open commongems` pour l'ouvrir"

						elif nbrand > 5 and nbrand < 15:
							sql.add(ID, "diamond", 1, "inventory")
							msg = "Tu as obtenu 1 <:gem_diamond:{}>`diamant brut`".format(GF.get_idmoji("diamond"))
							nbcobble = r.randint(0,5)
							if nbcobble != 0 :
								sql.add(ID, "cobblestone", nbcobble, "inventory")
								msg += "\nTu as obtenu {} bloc de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble,GF.get_idmoji("cobblestone"))

						elif nbrand > 15 and nbrand < 30:
							nbrand = r.randint(1,2)
							sql.add(ID, "gold", nbrand, "inventory")
							msg = "Tu as obtenu {} <:gem_gold:{}>`lingot d'or`".format(nbrand, GF.get_idmoji("gold"))
							nbcobble = r.randint(0,5)
							if nbcobble != 0 :
								sql.add(ID, "cobblestone", nbcobble, "inventory")
								msg += "\nTu as obtenu {} bloc de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble,GF.get_idmoji("cobblestone"))

						elif nbrand > 30 and nbrand < 60:
							nbrand = r.randint(1,4)
							sql.add(ID, "iron", nbrand, "inventory")
							msg = "Tu as obtenu {} <:gem_iron:{}>`lingot de fer`".format(nbrand, GF.get_idmoji("iron"))
							nbcobble = r.randint(0,5)
							if nbcobble != 0 :
								sql.add(ID, "cobblestone", nbcobble, "inventory")
								msg += "\nTu as obtenu {} bloc de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble,GF.get_idmoji("cobblestone"))

						elif nbrand >= 95:
							if r.randint(0,10) == 10:
								sql.add(ID, "ruby", 1, "inventory")
								sql.add(ID, "Mineur de Merveilles", 1, "statgems")
								sql.add(ID, "Mineur de Merveilles", 1, "trophy")
								msg = "En trouvant ce <:gem_ruby:{}>`ruby` tu deviens un Mineur de Merveilles".format(GF.get_idmoji("ruby"))
							else:
								msg = "La pioche n'est pas très efficace pour miner la `dirt`"
						else:
							nbcobble = r.randint(1,10)
							sql.add(ID, "cobblestone", nbcobble, "inventory")
							if nbcobble == 1 :
								msg = "Tu as obtenu 1 bloc de <:gem_cobblestone:{}>`cobblestone`".format(GF.get_idmoji("cobblestone"))
							else :
								msg = "Tu as obtenu {} blocs de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble, GF.get_idmoji("cobblestone"))

				#----------------- Pioche normal -----------------
				elif nbP >= 1:
					Durability = sql.valueAt(ID, "pickaxe", "durability")
					if Durability != 0:
						Durability = Durability[0]
					if Durability == 0:
						sql.add(ID, "pickaxe", -1, "inventory")
						if nbP > 1:
							for c in GF.objetOutil:
								if c.nom == "pickaxe":
									sql.add(ID, c.nom, c.durabilite, "durability")
						msg = "Pas de chance tu as cassé ta <:gem_pickaxe:{}>`pioche` !".format(GF.get_idmoji("pickaxe"))
					else :
						sql.add(ID, "pickaxe", -1, "durability")
						if nbrand < 20:
							sql.add(ID, "iron", 1, "inventory")
							msg = "Tu as obtenu 1 <:gem_iron:{}>`lingot de fer`".format(GF.get_idmoji("iron"))
							nbcobble = r.randint(0,5)
							if nbcobble != 0 :
								sql.add(ID, "cobblestone", nbcobble, "inventory")
								msg += "\nTu as obtenu {} bloc de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble,GF.get_idmoji("cobblestone"))
						else:
							nbcobble = r.randint(1,10)
							sql.add(ID, "cobblestone", nbcobble, "inventory")
							if nbcobble == 1 :
								msg = "Tu as obtenu 1 bloc de <:gem_cobblestone:{}>`cobblestone`".format(GF.get_idmoji("cobblestone"))
							else :
								msg = "Tu as obtenu {} blocs de <:gem_cobblestone:{}>`cobblestone`".format(nbcobble, GF.get_idmoji("cobblestone"))
				else:
					msg = "Il faut acheter ou forger une pioche pour miner!"

				sql.updateComTime(ID, "mine", "gems")
				lvl.addxp(ID, 1, "gems")
			else:
				msg = "Ton inventaire est plein"
		else:
			msg = "Il faut attendre "+str(GF.couldown_6s)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def fish(self, ctx):
		"""Péchons compagnons !!"""
		ID = ctx.author.id
		if sql.spam(ID,GF.couldown_6s, "fish", "gems"):
			if GF.testInvTaille(ID):
				nbrand = r.randint(0,99)
				nbfishingrod = sql.valueAt(ID, "fishingrod", "inventory")
				if nbfishingrod != 0:
					nbfishingrod = nbfishingrod[0]
				if nbfishingrod >= 1:
					Durability = sql.valueAt(ID, "fishingrod", "durability")
					if Durability != 0:
						Durability = Durability[0]
					if Durability == 0:
						sql.add(ID, "fishingrod", -1, "inventory")
						if nbfishingrod > 1:
							for c in GF.objetOutil:
								if c.nom == "fishingrod":
									sql.add(ID, c.nom, c.durabilite, "durability")
						msg = "Pas de chance tu as cassé ta <:gem_fishingrod:{}>`canne à peche` !".format(GF.get_idmoji("fishingrod"))
					else :
						sql.add(ID, "fishingrod", -1, "durability")
						nbfishhook = sql.valueAt(ID, "fishhook", "inventory")
						if nbfishhook != 0:
							nbfishhook = nbfishhook[0]
						if nbfishhook >= 1:
							mult = r.randint(-1, 5)
							if mult < 2:
								mult = 2
							sql.add(ID, "fishhook", -1, "inventory")
						else:
							mult = 1

						if nbrand < 15:
							nb = mult*1
							sql.add(ID, "tropicalfish", nb, "inventory")
							msg = "Tu as obtenu {} <:gem_tropicalfish:{}>`tropicalfish`".format(nb, GF.get_idmoji("tropicalfish"))
							nbfish = r.randint(0,3)*mult
							if nbfish != 0:
								sql.add(ID, "fish", nbfish, "inventory")
								msg += "\nTu as obtenu {} <:gem_fish:{}>`fish`".format(nbfish, GF.get_idmoji("fish"))

						elif nbrand >= 15 and nbrand < 30:
							nb = mult*1
							sql.add(ID, "blowfish", nb, "inventory")
							msg = "Tu as obtenu {} <:gem_blowfish:{}>`blowfish`".format(nb, GF.get_idmoji("blowfish"))
							nbfish = r.randint(0,3)*mult
							if nbfish != 0:
								sql.add(ID, "fish", nbfish, "inventory")
								msg += "\nTu as obtenu {} <:gem_fish:{}>`fish`".format(nbfish, GF.get_idmoji("fish"))

						elif nbrand >= 30 and nbrand < 40:
							nb = mult*1
							sql.add(ID, "octopus", nb, "inventory")
							msg = "Tu as obtenu {} <:gem_octopus:{}>`octopus`".format(nb, GF.get_idmoji("octopus"))
							D = r.randint(0,20)
							if D == 0:
								sql.add(ID, "lootbox_legendarygems", 1, "inventory")
								msg += "\nTu as trouvé une **Loot Box Gems Légendaire**! Utilise la commande `boxes open legendarygems` pour l'ouvrir"
							elif D >= 19:
								sql.add(ID, "lootbox_raregems", 1, "inventory")
								msg += "\nTu as trouvé une **Loot Box Gems Rare**! Utilise la commande `boxes open raregems` pour l'ouvrir"
							elif D >= 8 and D <= 12:
								sql.add(ID, "lootbox_commongems", 1, "inventory")
								msg += "\nTu as trouvé une **Loot Box Gems Common**! Utilise la commande `boxes open commongems` pour l'ouvrir"

						elif nbrand >= 40 and nbrand < 95:
							nbfish = r.randint(1,7)*mult
							sql.add(ID, "fish", nbfish, "inventory")
							msg = "Tu as obtenu {} <:gem_fish:{}>`fish`".format(nbfish, GF.get_idmoji("fish"))
						else:
							msg = "Pas de poisson pour toi aujourd'hui :cry: "
							if mult >= 2:
								sql.add(ID, "fishhook", 1, "inventory")
				else:
					msg = "Il te faut une <:gem_fishingrod:{}>`canne à pèche` pour pécher, tu en trouvera une au marché !".format(GF.get_idmoji("fishingrod"))

				sql.updateComTime(ID, "fish", "gems")
				lvl.addxp(ID, 1, "gems")
			else:
				msg = "Ton inventaire est plein"
		else:
			msg = "Il faut attendre "+str(GF.couldown_6s)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def hothouse(self, ctx, fct = None, arg = None):
		"""**[fonction]** {_n° plantation_} | Plantons compagnons !!"""
		ID = ctx.author.id
		maxplanting = 200
		if sql.spam(ID,GF.couldown_4s, "hothouse", "gems"):
			nbplanting = sql.valueAt(ID, "planting_plan", "inventory")
			if nbplanting != 0:
				nbplanting = int(nbplanting[0]) + 1
			else:
				nbplanting = 1
			if nbplanting >= maxplanting:
				nbplanting = maxplanting
			msg = discord.Embed(title = "La serre",color= 6466585, description = "Voici vos plantations.\nUtilisé `hothouse plant` pour planter une <:gem_seed:{0}>`seed`".format(GF.get_idmoji("seed")))
			desc = ""
			i = 1
			sql.updateComTime(ID, "hothouse", "gems")
			if fct == None or fct == "harvest":
				if  arg != None:
					if int(arg) <= nbplanting:
						nbplanting = int(arg)
					else:
						msg = "Tu n'as pas assez de plantations ou cette plantation n'est pas disponible!"
						await ctx.channel.send(msg)
						return 404
				while i <= nbplanting:
					data = []
					valuePlanting = sql.valueAt(ID, i, "hothouse")
					if valuePlanting != 0:
						valueTime = float(valuePlanting[0])
						valueItem = valuePlanting[1]
					else:
						valueTime = 0
						valueItem = ""
					if valueTime == 0:
						desc = "Aucune <:gem_seed:{0}>`seed` plantée.".format(GF.get_idmoji("seed"))
					else:
						PlantingTime = float(valueTime)
						InstantTime = t.time()
						time = PlantingTime - (InstantTime-GF.couldown_6h)
						if time <= 0:
							D10 = r.randint(1,10)
							jour = dt.date.today()
							if (jour.month == 10 and jour.day >= 23) or (jour.month == 11 and jour.day <= 10): #Special Halloween
								if D10 <= 3:
									nbHarvest = 1
									item = "oak"
								elif D10 > 3 and D10 <= 7:
									nbHarvest = r.randint(1, 2)
									item = "pumpkin"
								elif D10 > 7 and D10 <= 9:
									nbHarvest = r.randint(3, 5)
									item = "pumpkin"
								elif D10 >= 10:
									nbHarvest = r.randint(1,2)
									item = "wheat"
							else:
								if D10 <= 4:
									nbHarvest = 1
									item = "oak"
								elif D10 > 4 and D10 <= 7:
									nbHarvest = 1
									item = "spruce"
								elif D10 > 7 and D10 <= 9:
									nbHarvest = 1
									item = "palm"
								elif D10 >= 10:
									nbHarvest = r.randint(1,3)
									item = "wheat"
							data = []
							data.append(0)
							data.append("")
							sql.add(ID, item, nbHarvest, "inventory")
							sql.updateField(ID, i, data, "hothouse")
							desc = "Ta plantation à fini de pousser, en la coupant tu gagne {2} <:gem_{1}:{0}>`{1}`".format(GF.get_idmoji(item), item, nbHarvest)
							lvl.addxp(ID, 1, "gems")
							if i > 1:
								nbPlan = sql.valueAt(ID, "planting_plan", "inventory")
								if nbPlan != 0:
									nbPlan = int(nbPlan[0])
								if nbPlan > 0:
									if sql.valueAt(ID, "planting_plan", "durability") == 0:
										for c in GF.objetOutil:
											if c.nom == "planting_plan":
												sql.add(ID, "planting_plan", c.durabilite, "durability")
									sql.add(ID, "planting_plan", -1, "durability")
									if sql.valueAt(ID, "planting_plan", "durability")[0] <= 0:
										for c in GF.objetOutil:
											if c.nom == "planting_plan":
												sql.add(ID, "planting_plan", c.durabilite, "durability")
										sql.add(ID, "planting_plan", -1, "inventory")

						else:
							timeH = int(time / 60 / 60)
							time = time - timeH * 3600
							timeM = int(time / 60)
							timeS = int(time - timeM * 60)
							desc = "Ta plantation aura fini de pousser dans :clock2:`{}h {}m {}s`".format(timeH,timeM,timeS)
					if i % 10 == 0 and i != nbplanting:
						if i // 10 == 1:
							await ctx.channel.send(embed = msg)
						else:
							await ctx.channel.send(embed = msg, delete_after = 90)
						msg = discord.Embed(title = "La serre | Partie {}".format((i//10)+1),color= 6466585, description = "Voici vos plantation.".format(GF.get_idmoji("seed")))
						msg.add_field(name="Plantation n°{}".format(i), value=desc, inline=False)
					else:
						msg.add_field(name="Plantation n°{}".format(i), value=desc, inline=False)
					i += 1
			elif fct == "plant":
				#await ctx.channel.send("Plantations endommagées! Un violent orage :cloud_lightning: à détruit tes plantations\nTes plantations seront réparrées au plus vite\n\nHalloween approche, prépare toi pour l'événement d'halloween dès demain! <:gem_pumpkin:{}>".format(GF.get_idmoji("pumpkin")))
				#return False
				if arg != None:
					try:
						arg = int(arg)
					except:
						return 404
					if arg > nbplanting:
						msg = "Tu n'as pas assez de plantations ou cette plantation n'est pas disponible!"
						await ctx.channel.send(msg)
						return 404
					elif int(arg) < 0:
						sql.addGems(ID, -100)
						lvl.addxp(ID, -10, "gems")
						msg = ":no_entry: Anti-cheat! Tu viens de perdre 100 :gem:`gems`"
						await ctx.channel.send(msg)
						return "anticheat"
					data = []
					valuePlanting = sql.valueAt(ID, i, "hothouse")
					if valuePlanting != 0:
						valueTime = float(valuePlanting[0])
						valueItem = valuePlanting[1]
					else:
						valueTime = 0
						valueItem = ""
					if valueTime == 0:
						PlantingItemValue = sql.valueAt(ID, "seed", "inventory")
						if PlantingItemValue != 0:
							PlantingItemValue = PlantingItemValue[0]
						if PlantingItemValue >= 1:
							data = []
							data.append(str(t.time()))
							data.append("seed")
							sql.add(ID, arg, data, "hothouse")
							sql.add(ID, "seed", -1, "inventory")
							desc = "<:gem_{0}:{1}>`{0}` plantée".format("seed", GF.get_idmoji("seed"))
						else:
							desc = "Tu n'as pas de <:gem_{0}:{1}>`{0}` à planter dans ton inventaire".format("seed", GF.get_idmoji("seed"))
					else:
						desc = "Tu as déjà planté une <:gem_seed:{}>`seed` dans cette plantation".format(GF.get_idmoji("seed"))
					msg.add_field(name="Plntation n°{}".format(arg), value=desc, inline=False)
				else:
					while i <= nbplanting:
						data = []
						valuePlanting = sql.valueAt(ID, i, "hothouse")
						if valuePlanting != 0:
							valueTime = float(valuePlanting[0])
							valueItem = valuePlanting[1]
						else:
							valueTime = 0
							valueItem = ""
						PlantingItemValue = sql.valueAt(ID, "seed", "inventory")
						if PlantingItemValue != 0:
							PlantingItemValue = PlantingItemValue[0]
						if valueTime == 0:
							if PlantingItemValue >= 1:
								data = []
								data.append(str(t.time()))
								data.append("seed")
								sql.add(ID, i, data, "hothouse")
								sql.add(ID, "seed", -1, "inventory")
								desc = "<:gem_{0}:{1}>`{0}` plantée".format("seed", GF.get_idmoji("seed"))
							else:
								desc = "Tu n'as pas de <:gem_{0}:{1}>`{0}` à planter dans ton inventaire".format("seed", GF.get_idmoji("seed"))
								if i > 15:
									await ctx.channel.send(embed = msg)
									await ctx.channel.send(desc)
									return 0
						else:
							desc = "Tu as déjà planté une <:gem_seed:{}>`seed` dans cette plantation".format(GF.get_idmoji("seed"))
						if i % 10 == 0 and i != nbplanting:
							if i // 10 == 1:
								await ctx.channel.send(embed = msg)
							else:
								await ctx.channel.send(embed = msg, delete_after = 90)
							msg = discord.Embed(title = "La serre | Partie {}".format((i//10)+1),color= 6466585, description = "Voici vos plantations.".format(GF.get_idmoji("seed")))
							msg.add_field(name="Plantation n°{}".format(i), value=desc, inline=False)
						else:
							msg.add_field(name="Plantation n°{}".format(i), value=desc, inline=False)
						i += 1
			else:
				msg = "Fonction inconnu"
				await ctx.channel.send(msg)
				return False
			if nbplanting // 10 == 0:
				await ctx.channel.send(embed = msg)
			else:
				await ctx.channel.send(embed = msg, delete_after = 90)
		else:
			msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def slots(self, ctx, imise = None):
		"""**[mise]** | La machine à sous, la mise minimum est de 10 :gem:`gems`"""
		ID = ctx.author.id
		gems = sql.valueAt(ID, "gems", "gems")[0]
		if imise != None:
			if int(imise) < 0:
				msg = ":no_entry: Anti-cheat! Je vous met un amende de 100 :gem:`gems` pour avoir essayé de tricher !"
				lvl.addxp(ID, -10, "gems")
				sql.add(ID, "DiscordCop Amende", 1, "statgems")
				if gems > 100 :
					sql.addGems(ID, -100)
				else :
					sql.addGems(ID, -gems)
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

		if sql.spam(ID,GF.couldown_8s, "slots", "gems"):
			tab = []
			result = []
			msg = "Votre mise: {} :gem:`gems`\n\n".format(mise)
			val = 0-mise
			for i in range(0,9): #Creation de la machine à sous
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
					msg+="<:gem_{}:{}>".format(result[i], GF.get_idmoji(result[i]))
			msg += "\n"

			#===================================================================
			# Attribution des prix
			#===================================================================
			#Ruby (hyper rare)
			if result[3] == "ruby" or result[4] == "ruby" or result[5] == "ruby":
				sql.add(ID, "ruby", 1, "inventory")
				sql.add(ID, "Mineur de Merveilles", 1, "statgems")
				sql.add(ID, "Mineur de Merveilles", 1, "trophy")
				gain = 42
				msg += "\nEn trouvant ce <:gem_ruby:{}>`ruby` tu deviens un Mineur de Merveilles".format(GF.get_idmoji("ruby"))
				D = r.randint(0,20)
				if D == 0:
					sql.add(ID, "lootbox_legendarygems", 1, "inventory")
					msg += "\nTu as trouvé une **Loot Box Gems Légendaire**! Utilise la commande `boxes open legendarygems` pour l'ouvrir"
				elif D >= 19:
					sql.add(ID, "lootbox_raregems", 1, "inventory")
					msg += "\nTu as trouvé une **Loot Box Gems Rare**! Utilise la commande `boxes open raregems` pour l'ouvrir"
				elif D >= 8 and D <= 12:
					sql.add(ID, "lootbox_commongems", 1, "inventory")
					msg += "\nTu as trouvé une **Loot Box Gems Common**! Utilise la commande `boxes open commongems` pour l'ouvrir"
			#===================================================================
			#Super gain, 3 chiffres identique
			elif result[3] == "seven" and result[4] == "seven" and result[5] == "seven":
				gain = 1000
				sql.add(ID, "Super Jackpot :seven::seven::seven:", 1, "statgems")
				sql.add(ID, "Super Jackpot :seven::seven::seven:", 1, "trophy")
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
				sql.add(ID, "La Squelatitude", 1, "statgems")
				sql.add(ID, "La Squelatitude", 1, "trophy")
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
			nbCookie = 0
			if result[3] == "cookie" and result[4] == "cookie" and result[5] == "cookie":
				nbCookie = 3
			elif (result[3] == "cookie" and result[4] == "cookie") or (result[4] == "cookie" and result[5] == "cookie") or (result[3] == "cookie" and result[5] == "cookie"):
				nbCookie = 2
			elif result[3] == "cookie" or result[4] == "cookie" or result[5] == "cookie":
				nbCookie = 1
			if nbCookie != 0:
				if GF.testInvTaille(ID):
					msg += "\nTu a trouvé {} :cookie:`cookie`".format(nbCookie)
					sql.add(ID, "cookie", nbCookie, "inventory")
				else:
					msg += "\nTon inventaire est plein"
				D = r.randint(0,20)
				if D == 0:
					sql.add(ID, "lootbox_legendarygems", 1, "inventory")
					msg += "\nTu as trouvé une **Loot Box Gems Légendaire**! Utilise la commande `boxes open legendarygems` pour l'ouvrir"
				elif D >= 19:
					sql.add(ID, "lootbox_raregems", 1, "inventory")
					msg += "\nTu as trouvé une **Loot Box Gems Rare**! Utilise la commande `boxes open raregems` pour l'ouvrir"
				elif D >= 8 and D <= 12:
					sql.add(ID, "lootbox_commongems", 1, "inventory")
					msg += "\nTu as trouvé une **Loot Box Gems Common**! Utilise la commande `boxes open commongems` pour l'ouvrir"
			#===================================================================
			#grappe
			nbGrapes = 0
			if result[3] == "grapes" and result[4] == "grapes" and result[5] == "grapes":
				nbGrapes = 3
			elif (result[3] == "grapes" and result[4] == "grapes") or (result[4] == "grapes" and result[5] == "grapes") or (result[3] == "grapes" and result[5] == "grapes"):
				nbGrapes = 2
			elif result[3] == "grapes" or result[4] == "grapes" or result[5] == "grapes":
				nbGrapes = 1
			if nbGrapes != 0:
				if GF.testInvTaille(ID):
					msg += "\nTu a trouvé {} :grapes:`grapes`".format(nbGrapes)
					sql.add(ID, "grapes", nbGrapes, "inventory")
				else:
					msg += "\nTon inventaire est plein"
			#===================================================================
			#Backpack (hyper rare)
			if result[3] == "backpack" or result[4] == "backpack" or result[5] == "backpack":
				sql.add(ID, "backpack", 1, "inventory")
				p = 0
				for c in GF.objetItem:
					if c.nom == "backpack":
						p = c.poids * (-1)
				msg += "\nEn trouvant ce <:gem_backpack:{0}>`backpack` tu gagne {1} points d'inventaire".format(GF.get_idmoji("backpack"),p)

			#Calcul du prix
			prix = gain * mise
			if gain != 0 and gain != 1:
				if prix > 400:
					msg += "\n:slot_machine: Jackpot! Tu viens de gagner {} :gem:`gems`".format(prix)
				elif prix > 0:
					msg += "\nBravo, tu viens de gagner {} :gem:`gems`".format(prix)
				else:
					msg += "\nLa machine viens d'exploser :boom:\nTu as perdu {} :gem:`gems`".format(-1*prix)
				sql.addGems(ID, prix)
			elif gain == 1:
				msg += "\nBravo, voici un ticket gratuit pour relancer la machine à sous"
				sql.addGems(ID, prix)
			else:
				msg += "\nLa machine à sous ne paya rien ..."
				sql.addGems(ID, val)
			sql.updateComTime(ID, "slots", "gems")
			lvl.addxp(ID, gain, "gems")
		else:
			msg = "Il faut attendre "+str(GF.couldown_8s)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def boxes(self, ctx, type = None, name = None):
		"""**open [nom]** | Ouverture de Loot Box"""
		ID = ctx.author.id

		if type == "open":
			if name != None:
				for lootbox in GF.objetBox:
					if name == "lootbox_{}".format(lootbox.nom):
						name = lootbox.nom
				nbLB = sql.valueAt(ID, "lootbox_{}".format(name), "inventory")
				if nbLB != 0:
					nbLB = nbLB[0]
				if nbLB > 0:
					for lootbox in GF.objetBox:
						if name == lootbox.nom:
							gain = r.randint(lootbox.min, lootbox.max)
							titre = lootbox.titre

							sql.addGems(ID, gain)
							sql.add(ID, "lootbox_{}".format(lootbox.nom), -1, "inventory")
							desc = "{} :gem:`gems`".format(gain)
							msg = discord.Embed(title = "Lot Box | {}".format(titre),color= 13752280, description = desc)
							sql.updateComTime(ID, "boxes", "gems")
							print("Gems >> {} a ouvert une Loot Box".format(ctx.author.name))
							await ctx.channel.send(embed = msg)
							return True

					await ctx.chennel.send("Cette box n'existe pas!")
					return False
				else:
					msg = "Tu ne possèdes pas cette Loot Box"
			else:
				msg = "Commande `boxes open` incomplète"
		elif type == None:
			msg = "Commande `boxes` incomplète"
		else:
			msg = "Commande `boxes` invalide"
		await ctx.channel.send(msg)


def setup(bot):
	bot.add_cog(GemsPlay(bot))
	open("help/cogs.txt","a").write("GemsPlay\n")
