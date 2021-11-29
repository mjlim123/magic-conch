from asyncio.tasks import wait_for
import discord
from discord.ext import commands
from discord.ext.commands.core import check
from discord.ext.commands import cooldown
from discord.message import Message
import os
import mysql.connector
from mysql.connector.cursor import MySQLCursor
import random
import asyncio
import mysql
from decouple import config



db = mysql.connector.connect(
    host="us-cdbr-east-04.cleardb.com",
    user=config('user',default=''),
    passwd=config('passwd',default=''),
    database="heroku_7e0961da45020f8"
)

cursor = db.cursor(buffered=True)
columns = []
cursor.execute("SELECT * FROM INVENTORY")
for x in cursor.description:
    if x[0] == "id":
        pass
    elif x[0] == "krabby_patty":
        pass
    else:
        columns.append(x[0])

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents, command_prefix= '$')

def changeBalance(id, currency, amount):
    cursor = db.cursor(buffered=True)

    cursor.execute("UPDATE inventory SET {} = {} + {} WHERE id={}".format(str(currency), str(currency), str(amount), str(id)))
    db.commit()

def checkBalance(item, id):
    cursor = db.cursor(buffered=True)
    try:
        cursor.execute("SELECT {} FROM INVENTORY WHERE id={}".format(item, str(id)))
        for item in cursor:
            pass
        return item
    except Exception as e:
        return e

characters = {"1★ Spongebob":"onestarspongebob",
              "1★ Squidward":"onestarsquidward",
              "1★ Sandy":"onestarsandy",
              "1★ Patrick":"onestarpatrick",

              "2★ Spongebob":"twostarspongebob",
              "2★ Squidward":"twostarsquidward",
              "2★ Sandy":"twostarsandy",
              "2★ Patrick":"twostarpatrick",

              "3★ Spongebob":"threestarspongebob",
              "3★ Squidward":"threestarsquidward",
              "3★ Sandy":"threestarsandy",
              "3★ Patrick":"threestarpatrick",

              "4★ Patrick":"fourstarpatrick",
              "4★ Sandy":"fourstarsandy",
              "4★ Spongebob":"fourstarspongebob",
              "4★ Squidward":"fourstarsquidward",  

              "5★ Squidward":"fivestarsquidward",
              "5★ Spongebob":"fivestarspongebob",
              "5★ Sandy":"fivestarsandy",
              "5★ Patrick":"fivestarpatrick",

              "6★ Squidward":"sixstarsquidward",
              "6★ Spongebob":"sixstarspongebob",
              "6★ Patrick":"sixstarpatrick",
              "6★ Sandy":"sixstarsandy",
              
              "7★ Squidward":"sevenstarsquidward",
              "7★ Spongebob":"sevenstarspongebob",
              "7★ Patrick":"sevenstarpatrick",
              "7★ Sandy":"sevenstarsandy",

              "2★ Gary":"twostargary",
              "3★ Mr. Krabs":"threestarmrkrabs",
              "5★ Larry":"fivestarlarry"

             }

inventoryValues = { "basic_pack":["Basic Pack"],
                    "advanced_pack":["Advanced Pack"],
                    "master_pack":["Master Pack"],

                    "onestarspongebob":["1★ Spongebob",20,20],
                    "onestarsquidward":["1★ Squidward",25,15],
                    "onestarsandy":["1★ Sandy",30,10],
                    "onestarpatrick":["1★ Patrick",15,25],

                    "twostarspongebob":["2★ Spongebob",25,25],
                    "twostarsquidward":["2★ Squidward",30,20],
                    "twostarsandy":["2★ Sandy",35,15],
                    "twostarpatrick":["2★ Patrick",20,30],

                    "threestarspongebob":["3★ Spongebob",30,30],
                    "threestarsquidward":["3★ Squidward",35,25],
                    "threestarsandy":["3★ Sandy",40,20],
                    "threestarpatrick":["3★ Patrick",25,35],

                    "twostargary":["2★ Gary",45,25],
                    "threestarmrkrabs":["3★ Mr. Krabs",50,65],

                    "fourstarspongebob":["4★ Spongebob",35,35],
                    "fourstarpatrick":["4★ Patrick",30,40],
                    "fourstarsandy":["4★ Sandy",45,25],
                    "fourstarsquidward":["4★ Squidward",40,30],
                    
                    "fivestarsandy":["5★ Sandy",55,35],
                    "fivestarspongebob":["5★ Spongebob",45,45],
                    "fivestarpatrick":["5★ Patrick",40,50],
                    "fivestarsquidward":["5★ Squidward",50,40],

                    "sixstarsquidward":["6★ Squidward",65,55],
                    "sixstarspongebob":["6★ Spongebob",60,60],
                    "sixstarsandy":["6★ Sandy",70,50],
                    "sixstarpatrick":["6★ Patrick",55,65],

                    "sevenstarsquidward":["7★ Squidward",80,70],
                    "sevenstarspongebob":["7★ Spongebob",75,75],
                    "sevenstarsandy":["7★ Sandy",85,65],
                    "sevenstarpatrick":["7★ Patrick",70,80],

                    

                    "fivestarlarry":["5★ Larry",100,100]            
                    }

enemies = {
           "Jellyfish":[10,10,100],
           "Nematode":[20,20,180],
           "Kevin":[30,30,240],
           "Thug":[50,50,300],
           "Strangler":[75,75,600],
           "Flatts":[100,100,1000]
          }

basic_pack = {1:"1★ Spongebob",
              2:"1★ Squidward",
              3:"1★ Patrick",
              4:"1★ Sandy",
              5:"2★ Gary"
             }

advanced_pack = {1:"2★ Spongebob",
                 2:"2★ Squidward",
                 3:"2★ Patrick",
                 4:"2★ Sandy",
                 5:"3★ Mr. Krabs"
}
master_pack = {1:"4★ Spongebob",
               2:"4★ Squidward",
               3:"4★ Patrick",
               4:"4★ Sandy",
               5:"5★ Larry"

}



@client.event

async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    cursor.execute("SELECT * FROM User")
    memberList = []
    for member in cursor:
        if member in memberList:
            pass
        else:
            memberList.append(member[1])
            
    for guild in client.guilds:
        for member in guild.members:
            memberTuple = (str(member), str(member.id))
            if memberTuple[1] in memberList:
                
                pass
            else:
                cursor.execute("INSERT INTO User (Username, id) VALUES (%s,%s)",(str(member),str(member.id)))
                cursor.execute("INSERT INTO Inventory (id) VALUES ({})".format(member.id))
                db.commit()
    del memberList
            

@client.event
async def on_member_join(member):
    memberList = []
    cursor.execute("SELECT * FROM User")
    for member in cursor:
        if member in memberList:
            pass
        else:
            memberList.append(member)

    for guild in client.guilds:
        for member in guild.members:
            memberTuple = (str(member), str(member.id))
            if memberTuple in memberList:
                pass
            else:
                cursor.execute("INSERT INTO User (Username, id) VALUES (%s,%s)",(str(member),str(member.id)))
                cursor.execute("INSERT INTO Inventory (id) VALUES ({})".format(member.id))
                db.commit()
    print("Database Updated")
    del memberList


@client.command()
@commands.cooldown(1,15, commands.BucketType.user)
async def work(ctx):
    roll = random.randint(1,100)
    if roll == 1:
        rare = str(random.randint(200,250))
        await ctx.send(str(ctx.author.mention) + " You worked **extra** hard and earned " + rare + " :hamburger: !")
        changeBalance(str(ctx.author.id),'krabby_patty', rare)
    elif roll > 1 and roll <= 10:
        uncommon = str(random.randint(100,150))
        await ctx.send(str(ctx.author.mention) + " You worked hard and earned " + uncommon + " :hamburger: !")
        changeBalance(str(ctx.author.id),'krabby_patty', uncommon)
    elif roll > 10 and roll <= 50:
        okay = str(random.randint(50,75))
        await ctx.send(str(ctx.author.mention) + " You earned " + okay + " :hamburger: !")
        changeBalance(str(ctx.author.id),'krabby_patty', okay)
    else:
        common = str(random.randint(30,50))
        await ctx.send(str(ctx.author.mention) + " You earned " + common + " :hamburger: !")
        changeBalance(str(ctx.author.id),'krabby_patty', common)

@work.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ' Wait {:.0f} seconds before trying again.'.format(error.retry_after)
        await ctx.send(str(ctx.author.mention) + (msg))

@client.command()
async def balance(ctx):
    currentBalance = checkBalance('krabby_patty',ctx.author.id)
    await ctx.send(ctx.author.mention + " Your current balance is " + str(currentBalance[0]) + " :hamburger: .")


@client.command()
async def shop(ctx):
    shop = \
"\nSHOP\n\
1)BASIC PACK        500 Krabby patties\n\
2)ADVANCED PACK     1000 Krabby patties\n\
3)BASIC PACK x5     2300 Krabby Patties\n\
4)ADVANCED PACK x5  4700 Krabby Patties\n\
5)MASTER PACK       5000 Krabby Patties\n\
6)MASTER PACK x5    24700 Krabby Patties"

    await ctx.send("```fix\n"+ shop + "```")
    def check(m):
        if m.content == '1':
            return m.content == '1' and m.channel == ctx.channel
        elif m.content == '2':
            return m.content == '2' and m.channel == ctx.channel
        elif m.content == '3':
            return m.content == '3' and m.channel == ctx.channel
        elif m.content == '4':
            return m.content == '4' and m.channel == ctx.channel
        elif m.content == '5':
            return m.content == '5' and m.channel == ctx.channel
        elif m.content == '6':
            return m.content == '6' and m.channel == ctx.channel


    msg = await client.wait_for('message', check=check)
    if msg.author == ctx.author:
        currentBalance = checkBalance('krabby_patty', ctx.author.id)
        if msg.content == '1' and currentBalance[0] >= 500:
            await ctx.send(ctx.author.mention + "Basic Pack purchased!")
            changeBalance(ctx.author.id,'krabby_patty',str(-500))
            changeBalance(ctx.author.id,'basic_pack',str(1))
        elif msg.content == '2' and currentBalance[0] >= 1000:
            await ctx.send(ctx.author.mention + "Advanced Pack purchased!")
            changeBalance(ctx.author.id,'krabby_patty',str(-1000))
            changeBalance(ctx.author.id,'advanced_pack',str(1))
        elif msg.content == '3' and currentBalance[0] >= 2300:
            await ctx.send(ctx.author.mention + "Basic Pack x5 purchased!")
            changeBalance(ctx.author.id,'krabby_patty',str(-2300))
            changeBalance(ctx.author.id,'basic_pack',str(5))
        elif msg.content == '4' and currentBalance[0] >= 4700:
            await ctx.send(ctx.author.mention + "Advanced Pack x5 purchased!")
            changeBalance(ctx.author.id,'krabby_patty',str(-4700))
            changeBalance(ctx.author.id,'advanced_pack',str(5))
        elif msg.content == '5' and currentBalance[0] >= 5000:
            await ctx.send(ctx.author.mention + "Master Pack purchased!")
            changeBalance(ctx.author.id,'krabby_patty',str(-4700))
            changeBalance(ctx.author.id,'master_pack',str(1))
        elif msg.content == '6' and currentBalance[0] >= 24700:
            await ctx.send(ctx.author.mention + "Master Pack purchased!")
            changeBalance(ctx.author.id,'krabby_patty',str(-24700))
            changeBalance(ctx.author.id,'master_pack',str(5))


        
        else:
            await ctx.send(ctx.author.mention + "Insufficient Funds.")
    else:
        pass


@client.command()
async def unpack(ctx, *args):
    print(args)
    type = args[0]
    amount = int(args[2])
    print(amount)

    if type == "Basic":
        currentBalance = checkBalance('basic_pack',ctx.author.id)
        userPacks = currentBalance[0]
        if amount > userPacks:
            await ctx.send(ctx.author.mention + "Not enough packs")
        else:
            changeBalance(ctx.author.id, 'basic_pack', -amount)
            unpackResults = ""
            for i in range(amount):
                roll = random.random()
                if roll <= .01:
                    unpackResults += ctx.author.mention +"You received a " + basic_pack[5] + "\n"
                    changeBalance(ctx.author.id, characters[basic_pack[5]],1)
                    
                else:
                    common = random.randint(1,4)
                    reward = basic_pack[common]
                    unpackResults += ctx.author.mention +"You received a " + reward + "\n"
                    changeBalance(ctx.author.id,characters[reward],1)
    elif type == "Advanced":
        currentBalance = checkBalance('advanced_pack',ctx.author.id)
        userPacks = currentBalance[0]
        if amount > userPacks:
            await ctx.send(ctx.author.mention + "Not enough packs")
        else:
            changeBalance(ctx.author.id, 'advanced_pack', -amount)
            unpackResults = ""
            for i in range(amount):
                roll = random.random()
                if roll <= .01:
                    unpackResults += ctx.author.mention +"You received a " + advanced_pack[5] + "\n"
                    changeBalance(ctx.author.id, characters[advanced_pack[5]],1)
                    
                else:
                    common = random.randint(1,4)
                    reward = advanced_pack[common]
                    unpackResults += ctx.author.mention +"You received a " + reward + "\n"
                    changeBalance(ctx.author.id,characters[reward],1)
    elif type == "Master":
        currentBalance = checkBalance('master_pack',ctx.author.id)
        userPacks = currentBalance[0]
        if amount > userPacks:
            await ctx.send(ctx.author.mention + "Not enough packs")
        else:
            changeBalance(ctx.author.id, 'master_pack', -amount)
            unpackResults = ""
            for i in range(amount):
                roll = random.random()
                if roll <= .01:
                    unpackResults += ctx.author.mention +"You received a " + master_pack[5] + "\n"
                    changeBalance(ctx.author.id, characters[master_pack[5]],1)
                    
                else:
                    common = random.randint(1,4)
                    reward = master_pack[common]
                    unpackResults += ctx.author.mention +"You received a " + reward + "\n"
                    changeBalance(ctx.author.id,characters[reward],1)        
    await ctx.send(unpackResults)

@client.command()
async def inventory(ctx):
    print(columns)
    string = ""
    for x in columns:
        result = checkBalance(x,ctx.author.id)
        if result[0] == 0:
            pass
        else:
            char = inventoryValues[x]
            string += char[0] + ": " + str(result[0]) + "\n"
    await ctx.send(ctx.author.mention + "```fix\n" + string + "\n```")


@commands.cooldown(1,15, commands.BucketType.user)
@client.command()
async def battle(ctx, monster, user):
    check = checkBalance(user, ctx.author.id)
    if check == "Something went wrong.":
        await ctx.send(ctx.author.mention + "Invalid input")
    elif check[0] <= 0:
        print("oops!")
        await ctx.send("You do not own this character.")
    else:
        player = inventoryValues[user]
        enemy = enemies[monster]
        playerHP = player[2]
        enemyHP = enemy[1]
        playerDMG = player[1]
        enemyDMG = enemy[0]
        turn = 1
        message = await ctx.send(
            "```fix\n" +
            "BATTLE COMMENCING\n"+
            "```")
        while playerHP > 0 and enemyHP > 0:
            await asyncio.sleep(1)
            playerRoll = random.randint(1,3)
            enemyRoll = random.randint(1,3)
            await message.edit(content=
            ctx.author.mention + "\n" +
            "```fix\n"
            "--------------------------------------------\n"+
            "ROUND " + str(turn) + "\n" +
            "PLAYER HP: " + str(playerHP) + "  ENEMY HP: " + str(enemyHP)+"\n"
            "--------------------------------------------\n"+
            "```")
            await asyncio.sleep(1)
            if playerRoll == 1:
                await message.edit(content=
                ctx.author.mention + "\n" +
                "```fix\n"
                "--------------------------------------------\n"+
                "ROUND " + str(turn) + "\n" +
                "PLAYER HP: " + str(playerHP) + "  ENEMY HP: " + str(enemyHP)+"\n"+
                "--------------------------------------------\n"+
                "PLAYER ATTACKING...\n"+
                "```")
                await asyncio.sleep(1)
                await message.edit(content=
                ctx.author.mention + "\n" +
                "```fix\n"
                "--------------------------------------------\n"+
                "ROUND " + str(turn) + "\n" +
                "PLAYER HP: " + str(playerHP) + "  ENEMY HP: " + str(enemyHP)+"\n"+
                "--------------------------------------------\n"+
                "PLAYER ATTACKING...\n"+
                "HIT!\n"+
                "```")
                await asyncio.sleep(1)
                
                enemyHP -= playerDMG
                if enemyHP <= 0:
                    break
            else:
                await message.edit(content=
                ctx.author.mention + "\n" +
                "```fix\n"
                "--------------------------------------------\n"+
                "ROUND " + str(turn) + "\n" +
                "PLAYER HP: " + str(playerHP) + "  ENEMY HP: " + str(enemyHP)+"\n"+
                "--------------------------------------------\n"+
                "PLAYER ATTACKING...\n"+
                "```")
                await asyncio.sleep(1)
                await message.edit(content=
                ctx.author.mention + "\n" +
                "```fix\n"
                "--------------------------------------------\n"+
                "ROUND " + str(turn) + "\n" +
                "PLAYER HP: " + str(playerHP) + "  ENEMY HP: " + str(enemyHP)+"\n"+
                "--------------------------------------------\n"+
                "PLAYER ATTACKING...\n"+
                "MISS!\n"+
                "```")
                await asyncio.sleep(1)

                
            if enemyRoll == 1:
                await message.edit(content=
                ctx.author.mention + "\n" +
                "```fix\n"
                "--------------------------------------------\n"+
                "ROUND " + str(turn) + "\n" +
                "PLAYER HP: " + str(playerHP) + "  ENEMY HP: " + str(enemyHP)+"\n"+
                "--------------------------------------------\n"+
                "ENEMY ATTACKING...\n"+
                "```")
                await asyncio.sleep(1)
                await message.edit(content=
                ctx.author.mention + "\n" +
                "```fix\n"
                "--------------------------------------------\n"+
                "ROUND " + str(turn) + "\n" +
                "PLAYER HP: " + str(playerHP) + "  ENEMY HP: " + str(enemyHP)+"\n"+
                "--------------------------------------------\n"+
                "ENEMY ATTACKING...\n"+
                "HIT!"+
                "```")
                await asyncio.sleep(1)
                playerHP -= enemyDMG
                if playerHP <= 0:
                    break
            else:
                await message.edit(content=
                ctx.author.mention + "\n" +
                "```fix\n"
                "--------------------------------------------\n"+
                "ROUND " + str(turn) + "\n" +
                "PLAYER HP: " + str(playerHP) + "  ENEMY HP: " + str(enemyHP)+"\n"+
                "--------------------------------------------\n"+
                "ENEMY ATTACKING...\n"+
                "```")
                await asyncio.sleep(1)
                await message.edit(content=
                ctx.author.mention + "\n" +
                "```fix\n"
                "--------------------------------------------\n"+
                "ROUND " + str(turn) + "\n" +
                "PLAYER HP: " + str(playerHP) + "  ENEMY HP: " + str(enemyHP)+"\n"+
                "--------------------------------------------\n"+
                "ENEMY ATTACKING...\n"+
                "MISS!\n"+
                "```")
                await asyncio.sleep(1)
            turn += 1
        
        if playerHP <= 0:
            await message.edit(content=ctx.author.mention + "You died!  :skull: ")
        elif enemyHP <= 0:
            await message.edit(content=ctx.author.mention +"You Won!\n" + monster + " dropped " + str(enemy[2]) + " :hamburger:!")
            changeBalance(ctx.author.id, 'krabby_patty', enemy[2])
        battle.reset_cooldown(ctx)


@client.command()
async def teambattle(ctx, enemy):
    await ctx.send(ctx.author.mention + " wants to fight " + enemies[enemy] + "!" + "type 'join' to join them!")












@client.command()
async def promote(ctx, character):
    print(character)
    
    if character.startswith("one"):
        print("Im in")
        check = checkBalance(character, ctx.author.id)
        if check[0] < 4:
            await ctx.send("You do not have enough characters!")
        else:
            promotedCharacter = 'two' + character[3:]
            changeBalance(ctx.author.id, character, -4)
            changeBalance(ctx.author.id, promotedCharacter,   1)
            char1 = inventoryValues[character]
            char2 = inventoryValues[promotedCharacter]
            await ctx.send(ctx.author.mention + " Promotion successful! " + char1[0] + " evolved to " + char2[0])
    elif character.startswith("two"):
        check = checkBalance(character, ctx.author.id)
        if check[0] < 4:
            await ctx.send("You do not have enough characters!")
        else:
            promotedCharacter = 'three' + character[3:]
            changeBalance(ctx.author.id, character, -4)
            changeBalance(ctx.author.id, promotedCharacter, 1)
            char1 = inventoryValues[character]
            char2 = inventoryValues[promotedCharacter]
            await ctx.send(ctx.author.mention + " Promotion successful! " + char1[0] + " evolved to " + char2[0])
    
    elif character.startswith("three"):
        check = checkBalance(character, ctx.author.id)
        if check[0] < 4:
            await ctx.send("You do not have enough characters!")
        else:
            promotedCharacter = 'four' + character[5:]
            changeBalance(ctx.author.id, character, -4)
            changeBalance(ctx.author.id, promotedCharacter, 1)
            char1 = inventoryValues[character]
            char2 = inventoryValues[promotedCharacter]
            await ctx.send(ctx.author.mention + " Promotion successful! " + char1[0] + " evolved to " + char2[0])
    elif character.startswith("four"):
        check = checkBalance(character, ctx.author.id)
        if check[0] < 4:
            await ctx.send("You do not have enough characters!")
        else:
            promotedCharacter = 'five' + character[4:]
            changeBalance(ctx.author.id, character, -4)
            changeBalance(ctx.author.id, promotedCharacter, 1)
            char1 = inventoryValues[character]
            char2 = inventoryValues[promotedCharacter]
            await ctx.send(ctx.author.mention + " Promotion successful! " + char1[0] + " evolved to " + char2[0])
    elif character.startswith("five"):
        check = checkBalance(character, ctx.author.id)
        if check[0] < 4:
            await ctx.send("You do not have enough characters!")
        else:
            promotedCharacter = 'six' + character[4:]
            changeBalance(ctx.author.id, character, -4)
            changeBalance(ctx.author.id, promotedCharacter, 1)
            char1 = inventoryValues[character]
            char2 = inventoryValues[promotedCharacter]
            await ctx.send(ctx.author.mention + " Promotion successful! " + char1[0] + " evolved to " + char2[0])
    elif character.startswith("six"):
        check = checkBalance(character, ctx.author.id)
        if check[0] < 4:
            await ctx.send("You do not have enough characters!")
        else:
            promotedCharacter = 'seven' + character[3:]
            changeBalance(ctx.author.id, character, -4)
            changeBalance(ctx.author.id, promotedCharacter, 1)
            char1 = inventoryValues[character]
            char2 = inventoryValues[promotedCharacter]
            await ctx.send(ctx.author.mention + " Promotion successful! " + char1[0] + " evolved to " + char2[0])

@client.command()
@commands.cooldown(1,1000,commands.BucketType.guild)  # 1000 second cooldown
async def russian(ctx, amount):
    try:
        int(amount)
    except:
        await ctx.send("Please input a valid amount.")
        russian.reset_cooldown(ctx)
    else:
        wager = int(amount)
        pool = 0
        def check(m):
            input = (m.content.lower())
            print(type(input))
            if input == "join":
                print("IM IN")
                print(input)
                return input
            if input == "start" and m.author == ctx.author:
                    return m.content == input and m.channel == ctx.channel



        userBalance = checkBalance('krabby_patty', ctx.author.id)
        if userBalance[0] < wager:
            await ctx.send("You do not have enough :hamburger:  to start this game.")
            russian.reset_cooldown(ctx)
        else:
            await ctx.send("A game of Russian roulette has started! Type 'russian' to join! **Entrance fee: **"+ str(wager)+ " :hamburger:")
            numberOfPlayers = 1
            playerList = []
            playerList.append(ctx.author)
            status = 'waiting'
            while status == 'waiting':
                try:
                    msg = await client.wait_for('message',timeout=60)
                    if msg.channel == ctx.channel:
                        if msg.content.lower() == "russian":
                            userBalance = checkBalance('krabby_patty', msg.author.id)
                            if userBalance[0] < wager:
                                await ctx.send(msg.author.mention + "You do not have enough :hamburger:  to join.")
                            else:
                                if msg.author in playerList:
                                    await ctx.send("You are already entered!")
                                    pass
                                else:
                                    await ctx.send(msg.author.mention + " joined the game!")
                                    playerList.append(msg.author)
                                    numberOfPlayers += 1
                        elif msg.content.lower() == "start" and msg.author == ctx.author:
                            status = 'starting'
                    else:
                        pass
                except Exception as e :
                    print(e)
                    break
            if len(playerList) > 1:
                await ctx.send("Game is starting!")
                print(len(playerList))
                for person in playerList:
                    changeBalance(person.id, 'krabby_patty', -wager)
                    pool += wager
                round = 0
                chamber = 6
                rounds = 1
                await ctx.send("**GRAND PRIZE**: "+ str(pool) + " :hamburger:")
                await ctx.send("**ROUND "+ str(rounds) + "**")
                while True:
                    await asyncio.sleep(4)
                    if round >= len(playerList):
                        round = 0
                    else:
                        pass
                    await ctx.send(playerList[round].mention + " points the gun to their head.  " + ":flushed:" )
                    roll = random.randint(1,chamber)
                    print("Chance = ", 1/chamber)
                    await asyncio.sleep(4)
                    if roll == 1:
                        await ctx.send("BANG! :exploding_head: :boom: ")
                        playerList.pop(round)
                        chamber = 6
                        round = 0
                        rounds += 1
                        if len(playerList) == 1:
                            break

                    else:
                        await ctx.send("CLICK! :cold_face:")
                        chamber -= 1
                        round += 1
                await ctx.send(':tada: ' + playerList[round].mention + " wins " + str(pool) + " :hamburger: " + " :tada: ")
                changeBalance(playerList[round].id, 'krabby_patty', pool)
                russian.reset_cooldown(ctx)
            else:
                await ctx.send("Not enough people joined")
                russian.reset_cooldown(ctx)


@russian.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(ctx.author.mention + " Please specify an amount to enter. ")
        russian.reset_cooldown(ctx)

    if isinstance(error, commands.CommandOnCooldown):
        msg = ' Theres already an instance of russian roulette running.'.format(error.retry_after)
        await ctx.send(str(ctx.author.mention) + (msg))
                        

@client.command()
@commands.cooldown(1,10,commands.BucketType.guild) 
async def ask(ctx):
    
    responses =       {1:"No.mp3",
                       2: "Maybe Someday.mp3",
                       3:"Noooo.mp3",
                       4:"Try Asking Again.mp3",
                       5: "I Dont Think So.mp3",
                       6: "PlanktonYes.mp3",
                       7: "NoNoNo.mp3",
                       8: "YesYesYes.mp3"
                       }

    secret = {1:"guh.mp3",
              2:"sigh.mp3"

             }

    yes = {1: "YesYesYes.mp3",
           2: "PlanktonYes.mp3"
           }

    
    misc_questions = { 1:"No",
                     2: "Maybe Someday",
                     3: "Noooo",
                     4: "Try Asking Again",
                     5: "I Dont Think So"}

    questionWords = ["are", "am", "is", "can","will", "does", "do", "were", "did", "should", "guh", "sigh" ]

    sizeOfDict = len(responses)
    sizeeOfYes = len(yes)
    status = "in channel"
    eatCount = []
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        vc = await channel.connect()
        while status == "in channel":
            try:
                msg = await client.wait_for('message',timeout=60)
                if msg.channel == ctx.channel:
                    try:
                        for word in questionWords:
                                if (ctx.author.voice) and msg.content.lower().startswith(word) == True:
                                    if msg.content.lower().startswith(word):
                                        if msg.content == "is daniel gay":
                                            choice = random.randint(1,2)
                                            vc.play(discord.FFmpegPCMAudio("MP3_Files/"+yes[choice]))
                                            break
                                        elif msg.content.lower().startswith("guh"):
                                            vc.play(discord.FFmpegPCMAudio(source="MP3_Files/"+secret[1]))
                                            break
                                        elif msg.content.lower().startswith("sigh"):
                                            vc.play(discord.FFmpegPCMAudio(source="MP3_Files/"+secret[2]))
                                            break
                                        else:
                                            choice = random.randint(1,sizeOfDict)
                                            vc.play(discord.FFmpegPCMAudio("MP3_Files/"+responses[choice]))
                                            break
                
                                    else:
                                        print("Im in")
                                        choice = random.randint(1,sizeOfDict)
                                        vc.play(discord.FFmpegPCMAudio(source="MP3_Files/"+responses[choice]))

                                elif msg.content == "dc":
                                    await ctx.guild.voice_client.disconnect()
                                    break
                                else:
                                    pass   
                    except:
                        pass                  
                else:
                    print("something went wrong")
                    pass
            except Exception as e:
                print(e)
                print("well shit")
                break
        await ctx.guild.voice_client.disconnect()      
    else:
        await ctx.send("You must be in a voice channel to use this command.")
    
    
    
@ask.error 
async def ask_error(ctx, error):  
    if isinstance(error, commands.CommandOnCooldown):
            msg = ' Wait {:.0f} seconds before trying again.'.format(error.retry_after)
            await ctx.send(str(ctx.author.mention) + (msg))
    
@client.command()
async def monsters(ctx):
    string = ""
    for item in enemies:
        stats = enemies[item]
        string += item + " | HP: "+str(stats[0])+" DMG: "+str(stats[1])+" REWARD: "+str(stats[2]) + "\n"
    await ctx.send("```fix\n" + string + "\n```")

@client.command()
async def character(ctx):
    string = ""
    for item in characters:
        string += item + "\n"
    await ctx.send("```fix\n" + string + "\n```")

@client.command()
async def helpme(ctx):
    string = \
" $balance: shows player balance\n\
 $inventory: shows player inventory\n\
 $work: rewards player with krabby patties. useable every 15 seconds\n\
 $russian [amount]: initiate a game of russian roulette, [amount] being entry fee\n\
       (ex. $russian 100)\n\
 $ask: Summon the Magic Conch Shell. After apprearing, type yes/no questions. Type 'dc'\n\
       to disconnect the bot.\n\
 $shop: Show shop. After invoking, type the number of the item you want to buy.\n\
 $character: Show all characters available for acquisition.\n\
 $monsters: Show all monsters you can fight.\n\
 $battle [monster] [character]: Initiate a battle with a monster. Refer to \n\
       $monster command for all monsters able to be fought. As for summoning your character\n\
       if you own a '1★ Spongebob' it should be typed 'onestarspongebob; case sensitive. \n\
       (ex. $battle Jellyfish onestarspongebob)\n\
 $fastbattle [monster] [character]: Exactly the same as $battle, but skips the dialogue.\n\
 $promote [character]: Promotes a character (ex. $promote onestarsandy\n\
 $unpack [type] [amount]: Unpack a pack in your inventory.(ex. $unpack Basic Pack 10]\n\
 $duel [user]: Duel another user in the server."

    await ctx.send("```fix\n" + string + "```")


@client.command()
@commands.cooldown(5,60,commands.BucketType.user)
async def fastbattle(ctx, monster, user):
    check = checkBalance(user, ctx.author.id)
    if check == "Something went wrong.":
        await ctx.send(ctx.author.mention + "Invalid input")
    elif check[0] <= 0:
        print("oops!")
        await ctx.send("You do not own this character.")
    else:
        player = inventoryValues[user]
        enemy = enemies[monster]
        playerHP = player[2]
        enemyHP = enemy[1]
        playerDMG = player[1]
        enemyDMG = enemy[0]
        turn = 1
        while playerHP > 0 and enemyHP > 0:
            playerRoll = random.randint(1,3)
            enemyRoll = random.randint(1,3)
            if playerRoll == 1:
                enemyHP -= playerDMG
                if enemyHP <= 0:
                    break
            if enemyRoll == 1:
                playerHP -= enemyDMG
                if playerHP <= 0:
                    break        
            turn += 1
        if playerHP <= 0:
            await ctx.send("You Lost!")
        elif enemyHP <= 0:
            await ctx.send("You Won!\n" + monster + " drops " + str(enemy[2]) + " :hamburger:!")
            changeBalance(ctx.author.id, 'krabby_patty', enemy[2])

@fastbattle.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = ' Wait {:.0f} seconds before trying again.'.format(error.retry_after)
        await ctx.send(str(ctx.author.mention) + (msg))



@client.command()
async def duel(ctx, user):
    id = int(user[3:-1])
    if ctx.author.id == id:
        await ctx.send("You can't duel yourself, silly!")
    else:
        users = []
        users.append(ctx.author)
        await ctx.send(user + "\n" + ctx.author.mention + " challenges you to a duel! Do you accept?")
        status = 'waiting'
        while status == 'waiting':
            try:
                msg = await client.wait_for('message',timeout=20)
                if msg.channel == ctx.channel:
                    if msg.content.lower() == "accept" and msg.author.id == id:
                        users.append(msg.author)
                        break
                    else:
                        await ctx.send("Invalid Entry")
                else:
                    pass
            except Exception as e:
                print(e)
                break
        if len(users) == 2:
            userCharacters = {}
            await ctx.send("Duel Accepted! Select your character!")
            while status == "waiting":
                try:
                    if len(userCharacters) == 2:
                        break
                    msg = await client.wait_for('message',timeout=60)
                    if msg.channel == ctx.channel:
                        if msg.author.id in userCharacters:
                            await ctx.send("You've already selected you character.")
                        else:
                            if msg.content in inventoryValues:
                                checkCharacter = checkBalance(msg.content, msg.author.id)
                                if checkCharacter[0] == 0:
                                    await ctx.send("You do not own this character.")
                                elif checkCharacter == "Something went wrong.":
                                    await ctx.send("Invalid Entry.")
                                else:
                                    await ctx.send(msg.author.mention + " has selected their character!")
                                    userCharacters[msg.author.id] = msg.content
                            else:
                                await ctx.send("Invalid Entry")
                    else:
                        pass
                except Exception as e:
                    print(e)
                    break
        if len(userCharacters) == 2:
            player1 = inventoryValues[userCharacters[users[0].id]]
            print(player1)
            player2 = inventoryValues[userCharacters[users[1].id]]
            print(player2)
            player1HP = player1[2]
            player2HP = player2[2]
            player1DMG = player1[1]
            player2DMG = player2[1]
            turn = 1
            message = await ctx.send(
            "```fix\n" +
            "BATTLE COMMENCING\n"+
            "```")
            while player1HP > 0 and player2HP > 0:
                await asyncio.sleep(2)
                playerRoll = random.randint(1,3)
                enemyRoll = random.randint(1,3)
                await message.edit(content=
                "```fix\n"+
                "--------------------------------------------\n"+
                "ROUND " + str(turn) + "\n" +
                str(users[0]) +":  "+ str(player1HP)+"   "+  str(users[1])+":  "+ str(player2HP)+"\n"+
                "--------------------------------------------\n"+
                "```")
                await asyncio.sleep(2)
                if playerRoll == 1:
                    await message.edit(content=
                    "```fix\n"+
                    "--------------------------------------------\n"+
                    "ROUND " + str(turn) + "\n" +
                    str(users[0]) +":  "+ str(player1HP)+"   "+  str(users[1])+":  "+ str(player2HP)+"\n"+
                    "--------------------------------------------\n"+
                    str(users[0])+ " ATTACKING...\n"+
                    "```")
                    await asyncio.sleep(2)
                    await message.edit(content=
                    ctx.author.mention + "\n" +
                    "```fix\n"
                    "--------------------------------------------\n"+
                    "ROUND " + str(turn) + "\n" +
                    str(users[0]) +":  "+ str(player1HP)+"   "+  str(users[1])+":  "+ str(player2HP)+"\n"+
                    "--------------------------------------------\n"+
                    str(users[0])+ " ATTACKING...\n"+
                    "HIT!\n"+
                    "```")
                    await asyncio.sleep(2)
                    
                    player2HP -= player1DMG
                    if player2HP <= 0:
                        break
                else:
                    await message.edit(content=
                    ctx.author.mention + "\n" +
                    "```fix\n"
                    "--------------------------------------------\n"+
                    "ROUND " + str(turn) + "\n" +
                    str(users[0]) +":  "+ str(player1HP)+"   "+  str(users[1])+":  "+ str(player2HP)+"\n"+

                    "--------------------------------------------\n"+
                    str(users[0])+ " ATTACKING...\n"+
                    "```")
                    await asyncio.sleep(2)
                    await message.edit(content=
                    ctx.author.mention + "\n" +
                    "```fix\n"
                    "--------------------------------------------\n"+
                    "ROUND " + str(turn) + "\n" +
                    str(users[0]) +":  "+ str(player1HP)+"   "+  str(users[1])+":  "+ str(player2HP)+"\n"+

                    "--------------------------------------------\n"+
                    str(users[0])+ " ATTACKING...\n"+
                    "MISS!\n"+
                    "```")
                    await asyncio.sleep(2)

                    
                if enemyRoll == 1:
                    await message.edit(content=
                    ctx.author.mention + "\n" +
                    "```fix\n"
                    "--------------------------------------------\n"+
                    "ROUND " + str(turn) + "\n" +
                    str(users[0]) +":  "+ str(player1HP)+"   "+  str(users[1])+":  "+ str(player2HP)+"\n"+

                    "--------------------------------------------\n"+
                    str(users[1])+ " ATTACKING...\n"+
                    "```")
                    await asyncio.sleep(2)
                    await message.edit(content=
                    ctx.author.mention + "\n" +
                    "```fix\n"
                    "--------------------------------------------\n"+
                    "ROUND " + str(turn) + "\n" +
                    str(users[0]) +":  "+ str(player1HP)+"   "+  str(users[1])+":  "+ str(player2HP)+"\n"+

                    "--------------------------------------------\n"+
                    str(users[1])+ " ATTACKING...\n"+
                    "HIT!"+
                    "```")
                    await asyncio.sleep(2)
                    player1HP -= player2DMG
                    if player1HP <= 0:
                        break
                else:
                    await message.edit(content=
                    ctx.author.mention + "\n" +
                    "```fix\n"
                    "--------------------------------------------\n"+
                    "ROUND " + str(turn) + "\n" +
                    str(users[0]) +":  "+ str(player1HP)+"   "+  str(users[1])+":  "+ str(player2HP)+"\n"+

                    "--------------------------------------------\n"+
                    str(users[1])+ " ATTACKING...\n"+
                    "```")
                    await asyncio.sleep(2)
                    await message.edit(content=
                    ctx.author.mention + "\n" +
                    "```fix\n"
                    "--------------------------------------------\n"+
                    "ROUND " + str(turn) + "\n" +
                    str(users[0]) +":  "+ str(player1HP)+"   "+  str(users[1])+":  "+ str(player2HP)+"\n"+
                    "--------------------------------------------\n"+
                    str(users[1])+ " ATTACKING...\n"+
                    "MISS!\n"+
                    "```")
                    await asyncio.sleep(2)
                turn += 1
        
        if player1HP <= 0:
            await message.edit(content="\n" + users[1].mention + " won!")
        elif player2HP <= 0:
            await message.edit(content="\n" + users[0].mention + " won!")
        else:
            await ctx.send("Command timed out.")




@client.command()
async def blackjack(ctx, amount):
    class Hand:
        def __init__(self, name, id, bet, hand = []):
            self.name = name
            self.hand = []
            self.id = id
            self.bet = bet

        def addCard(self, card):
            self.hand.append(card)

        def sumOfHand(self):
            sum = 0
            for card in self.hand:
                if card.startswith('2'):
                    sum += 2
                elif card.startswith('3'):
                    sum+= 3
                elif card.startswith('4'):
                    sum+= 4
                elif card.startswith('5'):
                    sum+= 5
                elif card.startswith('6'):
                    sum+= 6
                elif card.startswith('7'):
                    sum+= 7
                elif card.startswith('8'):
                    sum+= 8
                elif card.startswith('9'):
                    sum+= 9
                elif card.startswith('10'):
                    sum+= 10
                elif card.startswith('Jack'):
                    sum+= 10
                elif card.startswith('King'):
                    sum+= 10
                elif card.startswith('Queen'):
                    sum+= 10
                elif card.startswith('Ace'):
                    if sum < 11:
                        sum+=11
                    else:
                        sum+=1
            return sum
        
        def printHand(self):
            string = ''
            for card in self.hand:
                string += card + "\n"
            return string


    
    card_values = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
    card_suites = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
    cardVal = [2,3,4,5,6,7,8,9,10,10,10,10,1]
    deck = [v + ' of ' + s for s in card_suites for v in card_values]
    lobby = []
    dealer = Hand('Dealer',856604431948840980,0)
    playerNames = []
    playerID = []
    players = []
    busts = []
    nonbusts = []
    blackjacks = []
    winners = []
    losers = []
    ties = []

    bets = []

    def checkAction(m):
        if m.channel == ctx.channel:
            if m.author.id == player.id:
                return m
    
    def checkLobby(m):
        if m.channel == ctx.channel:
            return m

    

    wager = int(amount)
    check = checkBalance('krabby_patty', ctx.author.id)
    if check[0] < wager:
        await ctx.send("You do not have enough krabby patties.")
    else:
        await ctx.send(ctx.author.mention + " started a blackjack table! Type 'blackjack [bet]' to join and place your bet!")
        playerNames.append("<@!"+ str(ctx.author.id) + ">")
        playerID.append(ctx.author.id)
        lobby.append(ctx.author.id)
        bets.append(wager)
        while True:
            print(bets)
            try:
                msg = await client.wait_for("message",timeout=30,check=checkLobby)
                wager = msg.content[10:]
                print(wager)
                try:
                    if msg.content.startswith("blackjack") and msg.author.id in lobby:
                        await ctx.send("You are already in!")
                    elif msg.content.startswith("blackjack") and msg.channel == ctx.channel and wager != "":
                        await ctx.send(msg.author.mention + " joined the table!")
                        playerNames.append("<@!"+ str(msg.author.id) + ">")
                        playerID.append(msg.author.id)
                        lobby.append(msg.author.id)
                        bets.append(int(wager))
                    elif msg.content == "start" and ctx.author == msg.author and msg.channel == ctx.channel:
                        await ctx.send("Blackjack Table is starting!")
                        break
                    else:
                        await ctx.send("Something went wrong.")
                except:
                    await ctx.send(msg.author.mention + "Invalid Entry.")
            except:
                
                await ctx.send("Blackjack table is starting!")
                break
        players = [Hand(playerNames[i],playerID[i],bets[i]) for i in range(len(playerNames))]
        deal = random.randint(0,len(deck)-1)
        dealer.addCard(deck[deal])
        deck.remove(deck[deal])
        for player in players:
            while len(player.hand) < 2:
                deal = random.randint(0,len(deck)-1)
                player.addCard(deck[deal])
                deck.remove(deck[deal])
        for player in players:
            turn = "playing"
            while turn != "done":
                if player.sumOfHand() == 21:
                    message = await ctx.send(player.name+"\n"+
                                            "```fix\n"+
                                            "DEALER'S HAND\n"+
                                            dealer.printHand()+" FACE-DOWN \n"+
                                            "\n"+
                                            "YOUR HAND\n"+
                                            player.printHand()+"\n"+
                                            "VALUE OF HAND: "+str(player.sumOfHand())+"\n"+
                                            "BLACKJACK!\n"
                                            "```"         )
                    turn = "done"
                    blackjacks.append(player)
                    nonbusts.append(player)
                else:
                    await ctx.send(player.name+"\n"+
                                            "```fix\n"+
                                            "DEALER'S HAND\n"+
                                            dealer.printHand()+" FACE-DOWN \n"+
                                            "\n"+
                                            "YOUR HAND\n"+
                                            player.printHand()+"\n"+
                                            "VALUE OF HAND: "+str(player.sumOfHand())+"\n"+
                                            "```"         )
                    action = await client.wait_for("message",check=checkAction)
                    if action.channel != ctx.channel:
                        print(action.channel, ctx.channel)
                        pass
                    elif action.content.lower() == 'hit' and action.author.id == player.id:
                        deal = random.randint(0,len(deck)-1)
                        player.addCard(deck[deal])
                        deck.remove(deck[deal])
                        if player.sumOfHand() > 21:
                            message = await ctx.send(player.name+"\n"+
                                            "```fix\n"+
                                            "DEALER'S HAND\n"+
                                            dealer.printHand()+" FACE-DOWN \n"+
                                            "\n"+
                                            "YOUR HAND\n"+
                                            player.printHand()+"\n"+
                                            "VALUE OF HAND: "+str(player.sumOfHand())+"\n"
                                            "BUST!"
                                            "```")
                            busts.append(player)
                            turn = "done"
                        elif player.sumOfHand() == 21:
                            message = await ctx.send(player.name+"\n"+
                                            "```fix\n"+
                                            "DEALER'S HAND\n"+
                                            dealer.printHand()+" FACE-DOWN \n"+
                                            "\n"+
                                            "YOUR HAND\n"+
                                            player.printHand()+"\n"+
                                            "VALUE OF HAND: "+str(player.sumOfHand())+"\n"
                                            "BLACKJACK!"
                                            "```")
                            turn = "done"
                            blackjacks.append(player)
                            nonbusts.append(player)

                    elif action.content.lower() == 'stay' and action.author.id == player.id:
                        turn = "done"
                        nonbusts.append(player)
                    else:
                        pass

        deal = random.randint(0,len(deck)-1)
        dealer.addCard(deck[deal])
        await asyncio.sleep(3)
        message = await ctx.send(  "```fix\n"+
                                    "DEALER'S HAND\n"+
                                    dealer.printHand()+
                                    "\n"+
                                    str(dealer.sumOfHand())+"\n"+
                                    "```")
        while dealer.sumOfHand() < 17:
            await asyncio.sleep(3)
            await message.edit(content=("```fix\nDEALER HITS...\n```"))
            await asyncio.sleep(3)
            deal = random.randint(0,len(deck)-1)
            dealer.addCard(deck[deal])
            await message.edit(content=("```fix\n"+
                                    "DEALER'S HAND\n"+
                                    dealer.printHand()+
                                    "\n"+
                                    str(dealer.sumOfHand())+"\n"+
                                    "```"))
        if dealer.sumOfHand() > 21:
            await message.edit(content=(  "```fix\n"+
                                    "DEALER'S HAND\n"+
                                    dealer.printHand()+
                                    "\n"+
                                    "DEALER BUSTED!\n"+
                                    str(dealer.sumOfHand())+"\n"+
                                    "```"))
            string = ''
            for player in nonbusts:
                if len(nonbusts) == 0:
                    break
                else:
                    winners.append(player)
                    string += player.name + ' '
            if string == '':
                await ctx.send("Nobody won")
            else:
                await ctx.send(string + " won!")
            string = ''
            for player in busts:
                if len(nonbusts) == 0:
                    break
                else:
                    busts.append(player)
                    string += player.name + ' '
            if string == "":
                pass
            else:
                ctx.send(string + " lost!")
            
        elif dealer.sumOfHand() == 21:
            await message.edit(content=(  "```fix\n"+
                                    "DEALER'S HAND\n"+
                                    dealer.printHand()+
                                    "\n"+
                                    "DEALER GOT BLACKJACK!\n"+
                                    str(dealer.sumOfHand())+"\n"+
                                    "```"))
            string = ""
            for player in blackjacks:
                string += player.name + " "
            if len(blackjacks) != 0:
                await ctx.send(string + " tied with the dealer!")
            else:
                pass
            string = ""
            for player in nonbusts:
                string += player.name + " "
            for player in busts:
                string += player.name + " "
            await ctx.send(string + " lost")


        elif dealer.sumOfHand() >= 17:
            for player in nonbusts:
                if len(nonbusts) == 0:
                    break
                elif player.sumOfHand() > dealer.sumOfHand():
                    winners.append(player)
                elif player.sumOfHand() < dealer.sumOfHand():
                    losers.append(player)
                elif player.sumOfHand() == dealer.sumOfHand():
                    ties.append(player)
            for player in busts:
                losers.append(player)
            for player in blackjacks:
                if player in winners:
                    pass
                else:
                    winners.append(player)
            
            string = ""
            for player in winners:
                if len(winners) == 0:
                    break
                else:
                    string += player.name + " "
            if len(winners)!= 0:
                await ctx.send(string + "won!")
            else:
                pass
            string = ""
            for player in losers:
                string += player.name + " "
            if len(losers)!= 0:
                await ctx.send(string + "lost!")
            string = ""
            for player in ties:
                string += player.name + " "
            if len(ties)!= 0:
                await ctx.send(string + " tied with the dealer!")
            for i in ties:
                print("ties  ",i)
            for i in winners:
                print("winners  ", i)
            for i in losers:
                print("losers  ", i)




@client.command()
async def test(ctx):
    file = open("MP3_Files/test.txt","r")
    for line in file:
        print(line)

           
client.run(config('token',default=''))
