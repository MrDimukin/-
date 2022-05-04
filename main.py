import time

from discord.utils import get
import discord
import requests
from discord.ext import commands
from random import choice

# Спасибо за помощь этим людям: Беззубик#6022, (〃°𝓞𝔀𝓵°〃)#8438

from youtube_dl import YoutubeDL

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True',
               'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

TOKEN = 'ODQ3NTYwMDIzNzgxODAyMDE0.YK_1yA.X0jOz5WGucV_Jz_41ig-kkMeNKs'
bot = commands.Bot(command_prefix='!', help_command=None)
bot.remove_command("help")


@bot.check
async def global_guild_only(ctx):
    if not ctx.guild:
        raise commands.NoPrivateMessage
    return True


@bot.check
async def check_channel(ctx):
    list_ignore_channel = []
    with open('list_ignore_channel.txt', 'r') as file:
        for el in file.readlines():
            list_ignore_channel.append(int(el.strip()))
    if ctx.channel.id in list_ignore_channel and ctx.message.content != '!toggleIgnore':
        raise commands.NoPrivateMessage
    return True


@bot.command(name='help')
async def bot_help(ctx, arg=None):
    if not arg:
        emb = discord.Embed(title='Список команд')
        emb.add_field(name='!cat', value='Картинка с кошечкой', inline=False)
        emb.add_field(name='!dog', value='Картинка с собачкой', inline=False)
        emb.add_field(name='!coin', value='Вы бросаете монетку', inline=False)
        emb.add_field(name='!random_number', value='Вы получите рандомное число', inline=False)
        emb.add_field(name='!play', value='Включить музыку', inline=False)
        emb.add_field(name='!stop', value='Выключить музыку', inline=False)
        emb.add_field(name='!pause', value='Ставит музыку на паузу', inline=False)
        emb.add_field(name='!resume', value='Снимает музыку с паузы', inline=False)
        emb.add_field(name='!volume', value='Меняет громкость', inline=False)
        emb.add_field(name='!mute', value='Замутить участника', inline=False)
        emb.add_field(name='!kick', value='Кикнуть участника с сервера', inline=False)
        emb.add_field(name='!ban', value='Забанить участника', inline=False)
        emb.add_field(name='!unban', value='Разбанить участника', inline=False)
        emb.add_field(name='!clear', value='Удалить несколько сообщений', inline=False)
        emb.add_field(name='!add_role', value='Добавляет участнику роль', inline=False)
        emb.add_field(name='!remove_role', value='Убирает у участника роль', inline=False)
        emb.add_field(name='!toggleIgnore', value='Переключить работу бота в чате', inline=False)
        await ctx.send(embed=emb)
    elif arg == 'mute':
        await ctx.send('!mute [member] [time] [reason]')
        await ctx.send('Команда позваляет замутить участника')
    elif arg == 'cat':
        await ctx.send('Команда выводит фото кошки')
    elif arg == 'dog':
        await ctx.send('Команда выводит фото собаки')
    elif arg == 'play':
        await ctx.send('!play [url]')
        await ctx.send('Команда подключает бота к голосовому каналу и включает музыку')
    elif arg == 'stop':
        await ctx.send('Команда останавливает проигрывание музыки и отключает бота от голосового канала')
    elif arg == 'kick':
        await ctx.send('!kick [member] [reason]')
        await ctx.send('Команда кикает участника сервера с некоторой причиной')
    elif arg == 'ban':
        await ctx.send('!ban [member] [reason]')
        await ctx.send('Команда банит участника с некоторой причиной')
    elif arg == 'unban':
        await ctx.send('!unban [member]')
        await ctx.send('Команда разбанивает участника')
    elif arg == 'clear':
        await ctx.send('!clear [count]')
        await ctx.send('Команда удаляет некоторое количество сообщений')
    elif arg == 'toggleIgnore':
        await ctx.send('Команда переключает работу бота в канале')
    elif arg == 'coin':
        await ctx.send('Команда бросает монетку. Результатом будет "Орел" или "Решка"')
    elif arg == 'random_number':
        await ctx.send('!random_number [number]')
        await ctx.send('Команда выдает рандомное число')
    elif arg == 'pause':
        await ctx.send('Команда ставит музыку на паузу')
    elif arg == 'resume':
        await ctx.send('Команда снимает музыку с паузы')
    elif arg == 'volume':
        await ctx.send('!volume [number]')
        await ctx.send('Команда ставит громкость на указанное число')


@bot.command(name='dog')
async def dog(ctx):
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    data = response.json()
    await ctx.send(data['message'])


@bot.command(name='cat')
async def cat(ctx):
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    data = response.json()
    await ctx.send(data[0]['url'])


@bot.command(name='coin')
async def coin(ctx):
    result = ['Орел', 'Решка']
    result = choice(result)
    await ctx.send(result)


@bot.command(name='random_number')
async def random_number(ctx, max_number=100):
    result = choice([i for i in range(int(max_number))])
    await ctx.send(result)


@bot.command(name='clear')
@commands.has_permissions(administrator=True)
async def clear(ctx, count=1):
    await ctx.channel.purge(limit=int(count) + 1)
    await ctx.send(':white_check_mark:')
    time.sleep(3)
    await ctx.channel.purge(limit=1)


@bot.command(name='toggleIgnore')
async def toggleIgnore(ctx):
    list_ignore_chanel = []

    with open('list_ignore_channel.txt', 'r', encoding='UTF8') as file:
        for el in file.readlines():
            list_ignore_chanel.append(int(el.strip()))

    channel = ctx.channel.id

    if channel in list_ignore_chanel:
        del list_ignore_chanel[list_ignore_chanel.index(channel)]
        await ctx.send('Теперь команды здесь работают')
    else:
        list_ignore_chanel.append(channel)
        await ctx.send('Теперь команды здесь не работают')

    with open('list_ignore_channel.txt', 'w') as file:
        for el in list_ignore_chanel:
            file.write(str(el) + '\n')


@bot.command(name='mute')
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, time_mute, reason):
    time_mute1 = time_mute[-1]
    time_mute2 = time_mute[:-1]

    mute_role = discord.utils.get(ctx.message.guild.roles, name='мут')
    await member.add_roles(mute_role)

    if time_mute1.lower() == 's':
        time.sleep(float(time_mute2))
    elif time_mute1.lower() == 'm':
        time.sleep(float(time_mute2) * 60)
    elif time_mute1.lower() == 'h':
        time.sleep(float(time_mute2) * 60 * 60)
    elif time_mute1.lower() == 'd':
        time.sleep(float(time_mute2) * 60 * 60 * 24)
    await member.remove_roles(mute_role)


@bot.command(name='kick')
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, reason=None):
    await ctx.channel.purge(limit=1)
    await member.kick(reason=reason)


@bot.command(name='ban')
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, reason=None):
    await ctx.channel.purge(limit=1)
    await member.ban(reason=reason)


@bot.command(name='unban')
@commands.has_permissions(administrator=True)
async def unban(ctx, member):
    if member.isdigit() and '#' not in member:
        member = int(member)
        await ctx.guild.unban(discord.Object(member))
    else:
        member = member.split('#')
        banned_user = await ctx.guild.bans()
        for user in banned_user:
            if user.user.name == member[0] and user.user.discriminator == member[1]:
                unban_user_id = user.user.id
        await ctx.guild.unban(discord.Object(unban_user_id))


@bot.command()
async def play(ctx, *, arg):
    vc = await ctx.message.author.voice.channel.connect()

    with YoutubeDL(YDL_OPTIONS) as ydl:
        if 'https://' in arg:
            info = ydl.extract_info(arg, download=False)
        else:
            info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
    url = info['formats'][0]['url']
    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=url, **FFMPEG_OPTIONS))


@bot.command(name='stop')
async def stop_voice(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()


@bot.command(name='pause')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.pause()


@bot.command(name='resume')
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.resume()
    print('pause')


@bot.command(name='volume')
async def volume(ctx, vol):
    voice = get(bot.voice_clients, guild=ctx.guild)
    channel = ctx.author.voice.channel
    vol_new = int(vol)
    if voice and voice.is_connected():
        voice.source = discord.PCMVolumeTransformer(
            voice.source, vol_new / 100)
        print(voice.source.volume)
    else:
        await ctx.send("Я не нахожусь в войс канале")


@bot.command(name='add_role')
@commands.has_permissions(administrator=True)
async def add_role(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)


@bot.command(name='remove_role')
@commands.has_permissions(administrator=True)
async def remove_role(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)

bot.run(TOKEN)
