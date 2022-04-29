#Импорт библиотек
import discord
from discord.ext import commands
import secrets
import string
from time import ctime



client=commands.Bot( command_prefix = '$' ) #Выдаем префикс боту
today = str(ctime()) #Переменная с актуальной датой
link="https://lolz.com" #Ссылка на чит
password="freecheat" #Пароль от архива на чит
ukey = '' #Индивидуальный ключ активации чита
client.remove_command('help') #удаляем стандартную команду help
users={

} #Буфер базы данных, тут хранятся ключи активации, привязанные к никам

logs = open('log.txt', 'a') #Файл с логами, если его нет - он создается
users_q = open('users.txt', 'a') #Файл с количеством пользователей, именами пользователей и их ключами активации. 

with open('users.txt', 'r') as file: #открывам файл пользователей
    data = file.readlines()

try:
    num_of_users=int(data[0]) #получаем количество пользователей для изменения
except:
    users_q.write('0') #если файл создался только что, мы начинаем отчет пользователей с 0, т.е. в начале файла пишем количество пользователей, написавших команду >get_cheat

def check(st): #функция проверки на наличие ника в базе данных
    with open('users.txt', 'r') as datafile:
        for line in datafile:
            str_list = line.split(sep=' ')
            if str(st) == str(str_list[0]):
                return True
                break
    return False

@client.command(aliases = ['help']) #Список команд
async def hlps(ctx):
    embed = discord.Embed(colour=ctx.author.color,timestamp=ctx.message.created_at)
    embed.add_field(name='>get_cheat',value='Получить ссылку на чит', inline=False),
    embed.add_field(name='>whois (@user)',value='Получение информации о пользователе', inline=False)
    embed.add_field(name='>userlist (ADMINS ONLY)',value='Список пользователей', inline=False)
    await ctx.send(embed=embed)

@client.event
async def on_message(message): #Функция фильтрации чата
    banwords = ["вирус", "ратник", "rat"] #запрещенные слова
    for word in banwords:
        if word in message.content.lower():
            await message.delete() #удаляем сообщение
            await message.author.kick() #кикаем пользователя, написавшего это сообщение
            logs = open('log.txt', 'a')
            try:
                logs.write(f'\n{today} User: {str(message.author.name)}#{str(message.author.discriminator)} - was kicked from server for word {word}!') #записываем инфу в логи
            except:
                logs.write(f'\n{today} User: null#{str(message.author.discriminator)} - was kicked from server for word {word}!') #записываем инфу в логи, если ник не стандартный
            logs.close()
    await client.process_commands(message) #после проверки продолжаем выполнять код

@client.event
async def on_ready():
    print(ctime()+': Bot activated') #надпись в консоль об активации бота

@client.command(aliases = ['ping']) #функция проверки бота. Вы пишете ping, он отвечает понг
async def pp(ctx):
    await ctx.send("Pong!")

@client.command(aliases = ['get_cheat']) #функция выдачи чита
async def gc(ctx):
    global num_of_users
    global ukey
    if check(str(ctx.author.name)) or ctx.author.name in users: #проверка на наличие имени в базе данных
        with open('users.txt', 'r') as datafile:
            for line in datafile:
                str_list = line.split(sep=' ')
                if str(ctx.author.name) == str(str_list[0]):
                    ukey = str_list[1] #Если пользователь нашелся, то у него уже есть ключ активации
    else:
        def rand_str(length): #функция сосдания строки из рандомных символов, где length - длина строки
            letters_and_digits = string.ascii_letters + string.digits
            crypt_rand_string = ''.join(secrets.choice(
                letters_and_digits) for i in range(length))
            return(crypt_rand_string)

        ukey = str(rand_str(16)) #сгенерированный код активации для нового пользователя
        logs = open('log.txt', 'a')
        users_q = open('users.txt', 'a')
        try:
            logs.write(f'\n{today} User: {str(ctx.author.name)}#{str(ctx.author.discriminator)} - got a cheat!') #записываем логи
            users_q.write(f'\n{str(ctx.author.name)} {str(ukey)}') #сохраняем имя пользователя и его ключ в базу даннных
        except:
            logs.write(f'\n{today} User: null#{str(ctx.author.discriminator)} - got a cheat!') #записываем инфу в логи, если ник не стандартный
            #Если ник не стандартными символами, пользователь не получает индивидуальный ключ в основную базу данных
        logs.close()
        users_q.close()
        with open ('users.txt', 'r') as tx: #открываем базу данных
            old_data = tx.read()
        new_data = old_data.replace(str(num_of_users), str(num_of_users+1)) #заменяем старое значение количества пользователей на +1
        with open ('users.txt', 'w') as tx: #обновляем файл
            tx.write(new_data)
        users[ctx.author.name]=ukey #добавляем ключ пользователя в буфер базы данных
        num_of_users+=1
    
    text = f'''Ссылка на скачивание: {link}
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        Код активации чита: {ukey}
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        Пароль от архива: {password}
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        Обновление от 25 апреля 2022 года (non detected)
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        Количество пользователей: {str(num_of_users+3147)}
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=''' #генерируем такой текст (все переменные см. ранее)
    await ctx.author.send(text) #отправляем сгенерированный тест пользователю в лс
    await ctx.send("Чит отправлен в личные сообщения!") #отчет об отправке
    
@client.command(aliases = ['whois']) #Функция проверки пользователя
async def who(ctx, user:discord.Member=None):
    if user == None:
        user=ctx.author #если пользователь не ввел ничье имя, то проверяем автора сообщения
    #Генерируем сообщение с инфой о пользователе
    embed = discord.Embed(colour=user.color,timestamp=ctx.message.created_at)
    embed.set_author(name=f"User info - {user}"),
    embed.set_thumbnail(url=user.avatar_url),
    embed.add_field(name='ID: ', value=str(user.id)+"#"+str(user.discriminator), inline=False)
    embed.add_field(name='Name: ', value=user.display_name, inline=False)
    embed.add_field(name='Created at: ', value=user.created_at, inline=False)
    embed.add_field(name='Joined at: ', value=user.joined_at, inline=False)
    embed.add_field(name='Top role: ', value=user.top_role.mention, inline=False)
    #Отправляем сгенерированное сообщение
    await ctx.send(embed=embed)

@client.command(aliases = ['userlist']) #Функция вывода базы данных
async def ul(ctx):
    if str(ctx.author.top_role) == 'ADMIN': #Проверка на роль, так как могут выводить только админы
        embed = discord.Embed(colour=ctx.author.color,timestamp=ctx.message.created_at) #Генерируем сообщение
        uslist = open('users.txt', 'r') #Открываем базу данных
        k=0 #Счетчик
        for line in uslist: #Перебор строк базы данных
            if k == 0: #В первой строке количество пользователей
                embed.add_field(name="Количество пользователей в БД: ", value=str(line), inline=False)
                k+=1
            else: #В остальных строках выводим имя пользователя и его ключ
                str_list = line.split(sep=' ')
                embed.add_field(name=str(k)+". "+str(str_list[0]), value="Ключ: "+str(str_list[1]), inline=False)
                k+=1
        await ctx.send(embed=embed) #Отправляем сообщение
    else:
        await ctx.send("У вас недостаточно прав!")

@client.command(aliases = ['clear']) #Функция удаления сообщений
async def delt(ctx, num):
    if str(ctx.author.top_role) == 'ADMIN':
        await ctx.channel.purge(limit=int(num)+1)
        logs = open('log.txt', 'a')
        try:
            logs.write(f'\n{today} User: {str(ctx.author.name)}#{str(ctx.author.discriminator)} - delete {num} message!') #записываем инфу в логи
        except:
            logs.write(f'\n{today} User: null#{str(ctx.author.discriminator)} - delete {num} message!') #записываем инфу в логи, если ник не стандартный
        logs.close()
    else:
        await ctx.send("У вас недостаточно прав!")

@client.command(aliases = ['info']) #Функция вывода рекламы чита
async def inf(ctx):
    embed = discord.Embed(colour=ctx.author.color,timestamp=ctx.message.created_at)
    embed.add_field(name="Количество пользователей в БД: ", value="add", inline=False)
    await ctx.send(embed=embed)

client.run("") #Токен бота