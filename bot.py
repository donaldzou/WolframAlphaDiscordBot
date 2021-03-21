import os
import discord
from discord.ext import commands, tasks
from discord.utils import get
import random
from tinydb import TinyDB, Query
import asyncio
import time
import t
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
from PIL import Image
from temporary import lookup
from get_html import getxml
import threading
import fcntl, termios, struct
import hashlib
token = t.token_k
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
jobs = []
finished_list = []
current_jobs = []
bot.request_count = 0

user_find = Query()
@bot.event
async def on_ready():
    looping.start()
    checking.start()
    check_pushback.start()
    update_request.start()
    os.system('clear')
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='g')
async def get(ctx, link):
    accept = True
    user_id = ctx.author.id
    print(link)
    if accept == True:
        if 'https://www.wolframalpha.com/input/?i=' not in link:
            await ctx.send(ctx.author.mention+', wrong format. Please try again.')
        else:
            link = link.replace('"','%22')
            print(link)
            user = str(ctx.author)
            user_id = ctx.author.id
            await ctx.send("I'll DM you in a minute, if you don't get the answer, request again."+ctx.author.mention)
            jobs.append([link,user,ctx.author.id])
            print('done')

@bot.command(name='q')
async def q(ctx, link):
    accept = True
    user_id = ctx.author.id
    print("QUESTION: "+link)
    if accept == True:
        link = link.split()
        content = ''
        for c in link:
            for a in c:
                if a.isdigit() or a.isalpha():
                    content+=a
                else:
                    content+="%"+format(ord(a),"x").upper()
            content+="+"
        content = content.rstrip("+")
        link = content
        user = str(ctx.author)
        user_id = ctx.author.id
        await ctx.send("I'll DM you in a minute, if you don't get the answer, request again."+ctx.author.mention)
        jobs.append([link,user,ctx.author.id])
        print('done')

@bot.command(name = 'help')
async def help(ctx):
    await ctx.send("You can check #how-to-use-this."+ctx.author.mention)
    await ctx.message.delete()
    
    


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

@tasks.loop(seconds=0.1)
async def check_pushback():
    pushback = open('job_repush.txt','r')
    pushback_data = pushback.readlines()
    if len(pushback_data) > 0:
        for data in pushback_data:
            data = data.strip('\n')
            data = data.split('<repush>')
            repush_link = data[0]
            repush_username = data[1]
            repush_id = int(data[2])
            position = current_jobs.index(data[3])
            current_jobs.pop(position)
            jobs.append([repush_link,repush_username,repush_id])
    pushback.close()
    pushback = open('job_repush.txt','w')
    pushback.close()
    
@tasks.loop(seconds = 0.1)
async def looping():
    now = datetime.now()
    if jobs.__len__()>0:
        user_id = jobs[0][2]        
        link = jobs[0][0]
        user_name = jobs[0][1]
        job_id_text = str(jobs[0])+str(datetime.now())
        job_id = hashlib.sha256(job_id_text.encode())
        job_id = job_id.hexdigest()
        print('-'*100)
        print('[Bot] |Recieved Fetching Jobs|')
        print('[Bot] |Job ID:',job_id,'|')
        print('[Bot] |User Id:',user_id,'|')
        print('[Bot] |User Name:',user_name,'|')
        print('[Bot] |Fetch Link:',link,'|')
        print('-'*100)
        current_jobs.append(job_id)
        print('Amount of Jobs: ',len(current_jobs))
        status = threading.Thread(target=getxml,args=(link,user_name,user_id,job_id))
        status.start()
        jobs.pop(0)

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



@tasks.loop(seconds = 0.1)
async def checking():
    job = open('job.txt','r')
    jobs = job.readlines()
    job_status = open('job_status.txt','r')
    status = job_status.readline()
    status = status.strip('\n')
    if status == 'not writing':
        if len(jobs) > 0:
            job_status.close()
            job_status = open('job_status.txt','w')
            job_status.write('bot writing')
            job_status.close()
            for a in jobs:
                a = a.strip('\n')
                a = a.strip('][').split(', ')
                a[1] = int(a[1])
                a[0] = a[0].strip("'")
                file_name = a[0]
                job_id = a[0]
                job_id = job_id.replace('result.png','')
                job_id = job_id.replace('result.html','')
                job_id = job_id.replace('_no_step_by_step.png','')
                print('[Bot] |Job ID|', job_id)
                account = int(a[1])
                print('-'*100)
                print('[Bot] |Recieved Sending Job|',account,','+file_name)
                
                user = bot.get_user(account)
                print(user)
                if '_no_step_by_step.png' in file_name:
                    await user.send(a[2]+' - This link does not have step-by-step solution, please try again.')
                    position = current_jobs.index(job_id)
                    current_jobs.pop(position)
                else:
                    await user.send('Here is the results ;)')
                    # await user.send(file=discord.File(file_name))
                    print(file_name)
                    if 'result.html' in file_name:
                        jpg_name = file_name.replace('result.html','result.jpg')
                        await user.send(file=discord.File(jpg_name))
                        bot.request_count += 1
                        try:
                            os.remove(jpg_name)
                        except FileNotFoundError:
                            pass
                    try:
                        os.remove(a[0])
                    except FileNotFoundError:
                        pass
                    position = current_jobs.index(job_id)
                    print(job_id,position)
                    current_jobs.pop(position)
                print('-'*100)
                print('[Bot] |Finshed Sending Job|',account,','+a[0])
                print('Amount of Jobs: ',len(current_jobs))
                ('-'*100)
            job.close()
            job = open('job.txt','w')
            job.close()
            job = open('job_status.txt','w')
            job.write('not writing')
            job.close()
    else:
        pass

bot.run(token)