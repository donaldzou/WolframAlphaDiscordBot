import os
import discord
from discord.ext import commands, tasks
from pyvirtualdisplay import Display
import t
from get_html import getxml
import threading
import pymongo
import urllib.parse

token = t.token_k
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
jobs = []
finished_list = []
current_jobs = []
bot.request_count = 0
client = pymongo.MongoClient(host="0.0.0.0", port=27017)
db = client.wolfram_bot
job_db = db.job
finished_job_db = db.finished_job

display = Display(visible=0, size=(1920, 1080))
display.start()

@bot.event
async def on_ready():
    looping.start()
    checking.start()
    update_request.start()
    os.system('clear')
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='g')
async def get(ctx, link):
    if ctx.message.channel.id == 665271879619051532:
        if 'https://www.wolframalpha.com/input/?i=' in link:
            link = link.replace('"', '%22')
            print(link)
            user = str(ctx.author)
            await ctx.send("I'll DM you right away ;) " + ctx.author.mention)
            new_job = {
                "link": link,
                "user": user,
                "user_id": ctx.author.id,
                "status": "pending"
            }
            job_db.insert_one(new_job)
        else:
            await ctx.send(ctx.author.mention + ', wrong format. Please try again.')
    else:
        await ctx.send("Please send this question in " + bot.get_channel(
            665271879619051532).mention + ". You can copy the following: \n`!g " + link + "`\n" + ctx.author.mention)
        try: await ctx.message.delete()
        except Exception:
            pass

@bot.command(name='q')
async def q(ctx, *question):
    link = ' '.join(question)
    if ctx.message.channel.id == 665271879619051532:
        print("QUESTION: "+link)
        link = urllib.parse.quote_plus(link)
        user = str(ctx.author)
        await ctx.send("I'll DM you right away ;) " + ctx.author.mention)
        new_job = {
            "link": link,
            "user": user,
            "user_id": ctx.author.id,
            "status": "pending"
        }
        job_db.insert_one(new_job)
    else:
        await ctx.send("Please send this question in "+bot.get_channel(665271879619051532).mention+
                       ". You can copy the following: \n`!q "+link+"`\n"+ctx.author.mention)
        try:
            await ctx.message.delete()
        except Exception:
            pass

@bot.command(name='help')
async def help(ctx):
    await ctx.send("You can check "+bot.get_channel(664271349237415936).mention+". "+ctx.author.mention)
    try:
        await ctx.message.delete()
    except Exception:
        pass

@get.error
async def info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(ctx.author.mention+', please enter a link. You can check #how-to-use-this.')

@bot.command(name='end')
async def end(ctx):
    user = str(ctx.author.id)
    if user == '647518744146608139':
        await ctx.send(bot.user.name+' logged out!')
        await bot.logout()

    
@tasks.loop(seconds = 0.5)
async def looping():
    if job_db.count_documents({"status": "pending"}) > 0:
        pending_job = job_db.find({"status": "pending"})
        for i in pending_job:
            job_db.update_one({"_id": i['_id']}, {"$set": {"status": "fetching"}})
            user_id = i['user_id']
            link = i['link']
            user_name = i['user']
            print('-' * 100)
            print('[Bot] |Recieved Fetching Jobs|')
            print('[Bot] |Job ID:', i['_id'], '|')
            print('[Bot] |User Id:', user_id, '|')
            print('[Bot] |User Name:', user_name, '|')
            print('[Bot] |Fetch Link:', link, '|')
            print('-' * 100)
            status = threading.Thread(target=getxml, args=(link, user_name, user_id, i['_id'], client))
            status.start()

@tasks.loop(seconds = 900)
async def update_request():
    if bot.request_count > 0:
        try:
            request = bot.get_channel(787895668026376202)
            c_name = request.name
            c_name = c_name.replace(" Requests", "")
            c_name = c_name.replace(" ", "")
            c_name = c_name.replace("📊|", "")
            c_name = c_name.replace("|📊", "")
            c_name = int(c_name)
            c_name += bot.request_count
            c_name = "📊| "+str(c_name)+" Requests"
            print(c_name)
            await request.edit(name=c_name)
            bot.request_count = 0
        except discord.InvalidArgument as e:
            print(e)
        except discord.Forbidden as e:
            print(e)
        except discord.HTTPException as e:
            print(e)



@tasks.loop(seconds = 0.5)
async def checking():
    finished_job = job_db.find({
        "$or": [{"status": "yes_result"}, {"status": "no_result"}]
    })
    for i in finished_job:
        print('[Bot] |Job ID|', str(i['_id']))
        account = i['user_id']
        print('-' * 100)
        print('[Bot] [ID: '+str(i['_id'])+'] |Received Sending Job| Receiver: ', account)
        user = await bot.fetch_user(account)
        if i['status'] == "no_result":
            await user.send('`' + i['link'] + '` - This question does not have step-by-step solution, please try again.')
        else:
            await user.send('**Here are the results ;) **')
            jpg_name = str(i['_id'])+'result.jpg'
            await user.send(file=discord.File(jpg_name))
            bot.request_count += 1
            try:
                os.remove(jpg_name)
            except FileNotFoundError:
                pass
        job_db.update_one({"_id": i['_id']}, {"$set": {"status": "sent"}})
        print('[Bot] [ID: '+str(i['_id'])+'] |Finshed Sending Job|', account)

bot.run(token)