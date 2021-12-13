#Imports everything needed
import discord
import os
import random
import discord.ext
import json
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check

from keep_alive import keep_alive



#============================ClientSetup==================================================================================================
client = discord.Client()
#Prefix before every command, specifically "shapat"
#also names discord.client as just client so we dont have to type "discord.Client" when we want to reference it in our code.
client = commands.Bot(command_prefix = 's!')
client.sniped_messages = {}

#=========================================Meme Images:=========================================


#============================ManageEvents=================================================================================================
@client.event
async def on_ready():
    print("bot online") #will print "bot online" in the console when the bot is online
    


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_msg = None
#============================FunCommands==================================================================================================

@client.command()
async def play(ctx):
  await ctx.send("With the closure of music bots due to the class action  lawsuits, the music feature has been removed")

#Example of a command, replace the first -- with a command, then say the output in the next --

"""
#state it is a command
@client.command()
#"--" will be our command
async def --(ctx):
  #the bot will send a said message
  await ctx.send(--)
"""  
@client.command()
async def ping(ctx):
    await ctx.send("pong!") 

@client.command()
async def asktrump(ctx):
    atmn = random.randint(1,9)
    atml = ["DEMOCRATS", "STOLEN ELECTION", "WE NEED TO BUILD A WALL", "CHINESE PLAGUE", "FAKE NEWS", "OBAMNA", "ALIENS", "i must say i am a very good looking person", "ABHI KI BAAR, TRUMP SARKAR", "the beauty of me is that im rich"]
    embed = discord.Embed(title = atml[atmn], color=discord.Color.orange())
    embed.set_image(url="https://d.newsweek.com/en/full/1880374/donald-trump-enters-rally-arizona.jpg?w=790&f=be4336757b04f4cc3286588fc2dc2e70")
    await ctx.send(embed = embed)

@client.command()
async def yes(ctx, meme_context):
 
    embed = discord.Embed(title = meme_context, color = discord.Color.orange())
    embed.set_image(url = "https://i.kym-cdn.com/entries/icons/original/000/031/727/cover10.jpg")
    await ctx.send(embed = embed)

@yes.error
async def yes_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("You have to actually state the context")

    
@client.command()
async def socials(ctx):
    await ctx.send("@sardarrah = tiktok")

@client.command()
async def kill(ctx, member : discord.Member):
    #What this will do is that it will "kill" a said person.
    await ctx.send("killed "+member.mention)

@kill.error
async def kill_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("i cant kill air, im sorry")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("at least ping someone for me to kill lol")

@client.command()
async def fortnite(ctx):
  place=random.randint(1,100)
  kills=random.randint(1,place)
  await ctx.send("Place:"+str(place))
  await ctx.send("kills:"+str(kills))
  if place == 1:
    await ctx.send("VICTORY ROYALE!")



@fortnite.error
async def fortnite_error(ctx, error):
    print(error)
    await ctx.send("Fortnite is currently down!")

@client.command()
async def version(ctx):
  await ctx.send("ShapatBot version 3.1")

@client.command(aliases = ["pp"])
async def penis(ctx, name):
    penis = random.randint(1,7)
    await ctx.send(name + "\'s tip is "+str(penis)+" inches")
    if penis == 1:
      await ctx.send("LMAO IMAGINE")

@penis.error
async def penis_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      penis = random.randint(1,7)
      await ctx.send("Your tip is "+str(penis)+" inches")
      if penis == 1:
        await ctx.send("LMAO IMAGINE")


#==============================Economy====================================================================================================
mainshop = [{"name":"Watch","price":100,"description":"Time"},
            {"name":"Laptop","price":1000,"description":"Work"},
            {"name":"PC","price":10000,"description":"Gaming"},
            {"name":"Ferrari","price":99999,"description":"Sports Car"}]

@client.command(aliases=['bal'])
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f'{ctx.author.name} Balance',color = discord.Color.red())
    em.add_field(name="Wallet Balance", value=wallet_amt)
    em.add_field(name='Bank Balance',value=bank_amt)
    await ctx.send(embed= em)

@client.command()
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()
    ece = random.randint(1,2)
    if ece == 2:
      earnings = random.randrange(101)
    elif ece == 1:
      earnings = 0

    await ctx.send(f'{ctx.author.mention} Got {earnings} coins!!')

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json",'w') as f:
        json.dump(users,f)


@client.command(aliases=['wd'])
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[1]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,'bank')
    await ctx.send(f'{ctx.author.mention} You withdrew {amount} coins')


@client.command(aliases=['dp'])
async def deposit(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,'bank')
    await ctx.send(f'{ctx.author.mention} You deposited {amount} coins')


@client.command(aliases=['sm'])
async def send(ctx,member : discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)
    if amount == 'all':
        amount = bal[0]

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,-1*amount,'bank')
    await update_bank(member,amount,'bank')
    await ctx.send(f'{ctx.author.mention} You gave {member} {amount} coins')


@client.command(aliases=['rb'])
async def rob(ctx,member : discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)


    if bal[0]<100:
        await ctx.send('It is useless to rob him :(')
        return
    
    earning = random.randrange(0,bal[0])

    await update_bank(ctx.author,earning)
    await update_bank(member,-1*earning)
    await ctx.send(f'{ctx.author.mention} You robbed {member} and got {earning} coins')


@client.command()
async def slots(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return
    final = []
    for i in range(3):
        a = random.choice(['X','O','Q'])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        await update_bank(ctx.author,2*amount)
        await ctx.send(f'You won :) {ctx.author.mention}')
    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send(f'You lose :( {ctx.author.mention}')


@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"${price} | {desc}")

    await ctx.send(embed = em)



@client.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return


    await ctx.send(f"You just bought {amount} {item}")


@client.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)


async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]
    

@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.7* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]


@client.command(aliases = ["lb"])
async def leaderboard(ctx,x = 1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open('mainbank.json','w') as f:
        json.dump(users,f)

    return True


async def get_bank_data():
    with open('mainbank.json','r') as f:
        users = json.load(f)

    return users


async def update_bank(user,change=0,mode = 'wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('mainbank.json','w') as f:
        json.dump(users,f)
    bal = users[str(user.id)]['wallet'],users[str(user.id)]['bank']
    return bal



#=======================================Snipe=============================================================================================================================================
#when a message is deleted, this command will record it
@client.event
async def on_message_delete(message):
    client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

#obtains the last recorded message data from line 68-70, so that it can be used in line 83-87
@client.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time = client.sniped_messages[ctx.guild.id]
        
    #if line 68-70 coulnt record a deleted message, usually because the bot was enabled after the last deleted message, the command will make an exception to say "couldnt find a message to snipe".    
    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return
        

    embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")
    #makes an embedded message
    await ctx.channel.send(embed=embed)
    #sends the embedded message

#======================================TicTacToe==========================================================================================================================================

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn you dummy")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


#=====================================Guesser==================================================
#======================================8ball==============================================================================================================================================
@client.command()
async def eightball(ctx):
  random_number = random.randint(1, 12)
  if random_number == 1:
    await ctx.send("LMFAO YES")
  elif random_number == 2:
    await ctx.send("It is decidedly so")
  elif random_number == 3:
    await ctx.send("Without a doubt, lol")
  elif random_number == 4:
    await ctx.send("Reply hazy, try again")
  elif random_number == 5:
    await ctx.send("please go away")
  elif random_number == 6:
    await ctx.send("Better not tell you now, you idiot")
  elif random_number == 7:
    await ctx.send("My sources say hell nah")
  elif random_number == 8:
    await ctx.send("Outlook not so good")
  elif random_number == 9:
    await ctx.send("doubt it")
  elif random_number == 10:
    await ctx.send("lmfao hell nah")
  elif random_number == 11:
    await ctx.send("idk tbh lol")
  elif random_number == 12:
    await ctx.send("sure")

#=======================================Memes================================================
#============================================================================================
@client.command(pass_context=True)
async def meme(ctx):
    await ctx.send("this feature has been removed!")

@client.command(pass_context=True)
async def madlads(ctx):
    await ctx.send("this feature has been removed!")
@client.command(pass_context=True)
async def cursedcomments(ctx):
    await ctx.send("this feature has been removed!")

#==============================================================================================
@client.command()
async def memeshower(ctx):
    await ctx.send("this feature has been removed!")

@client.command()
async def madladshower(ctx):
    await ctx.send("this feature has been removed!")

#==============================================================================================
keep_alive()
token = os.environ.get("TOKEN") 
client.run(token)
client.run(os.getenv("TOKEN")) 

