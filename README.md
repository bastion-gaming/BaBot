# Ba-Bot
Bot discord de bastion

Suite au décès de mewna notre bot, aimée de tous sauf lorsqu'elle buggait, nous sommes dans
l'obligation de créer notre propre bot pour retrouver les services dont nous avons besoin mais
aussi des nouveaux.

## Le nom

Il se nomme Ba-Bot

## La participation

A ce jour, on a déjà commencé à créer une partie du bot et on l'a donc mis sur ce GitHub.
On pense qu'il est important qu'on soit transparent dans ce qu'on fait et tous les membres sachant
coder en python sont évidemment les bienvenus pour nous aider à coder ou émettre des
critiques constructives.

# Idées sur le fonctionnement général

## Organisation

On propose une architecture "modulaire" avec un core qui se charge de lancer les différentes
parties du bot.

## Idées de module

**Core**: Il va se charger de lancer les autres modules  

**Rôles**: Ce module va se charger de gérer les rôles. C'est a dire de mettre le rôle "Joueurs" aux
nouveaux membres mais aussi pour pouvoir en une commande créer un nouveau rôle
correspondant à un jeu puis l'associer à un salon  

**Get Gems**: Partie déjà en cours à ce jour par Shell, ce module ce chargera de gérer le jeu. Il est semblable à celui qui existait avec Mewna. Donc toutes les commandes qui permettent d'acheter, vendre, braquer, parier etc... De toute façon Shell est en bonne voie.  

**Level** : Gestion des niveaux, genre tous les x mots on monte d'un niveaux, ça permet de quantifier la participation de chacun aux discussions. On doit se mettre d'accord sur les modalités de leveling.  

**DB**: On propose que le bot n'est qu'une seule base de donnée pour stocker les niveaux des joueurs et leur quantité d'argent. Onutilise TinyDB 

**Gestion de la musique**: On propose que le bot puissent lancer des vidéos Youtube au format audio.

**Vote** : Pouvoir créer un vote en configurant la *Question*, les *Réponses* et le *temps du vote*.

**Stat**: Compter le nombre de message poster dans les salons en fonction du temps. C'est
utile et là au moins on est sûr qu'il nous lis pas en même temps.  

**Game-Asker**: l'idée serait que quand quelqu'un sur Bastion entrerait une commande en
précisant le jeu auquel il veut jouer ça les mentionne (exactement comme on fait
aujourd'hui avec les mention de rôle) et c'est d'ailleurs ce que fera le bot MAIS je voudrais en
parallèle du Bot Bastion créer un autre bot plus léger qui en se basant sur cette idée permettrait de poster un message sur les serveurs qui l'utilisent qui précise qui veut jouer et
à quoi lorsque cette commande est entrée.

**Live Notification**: Averti dans le salon #partage du début d'un live sur la chaine Twitch Bastion et celle des partenaires/kopains



# État d'avancement du développement

## Terminés

Core

Rôles

Get Gems

Level

DB

Vote

Stat

Live Notification

## En cours/test

Musique

## Non commencé

Game-Asker
