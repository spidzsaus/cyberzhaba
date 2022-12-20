import discord
import json
from data import db_session
from data.usermodel import SqlUser, SqlBarrellOrgan
import datetime as dt
import math
import requests
from io import BytesIO
from PIL import Image
import asyncio
from secret_data import PROD_TOKEN

ORGANS_AVAILABLE = False

frame = Image.open('frame.png')

client = discord.Client(intents=discord.Intents.all())

with open('config.json', encoding='utf-8') as file:
    CONFIG = json.load(file)

def days_delta(msg):
    now = dt.datetime.today()
    delta = now - msg.created_at
    return delta.days

def basic_embed(title, text, *fields):
    emb = discord.Embed(color=discord.Color.green(),
                        title=title,
                        description=text)
    for name, value in fields:
        emb.add_field(name=name, value=value)
    return emb

class BarellOrgan:
    def __new__(cls, id):
        owner_discord_id = id
        db_sess = db_session.create_session()
        owner = db_sess.query(SqlUser).filter(SqlUser.discord_id == owner_discord_id
                                              ).first()
        if not owner:
            return None

        organ = db_sess.query(SqlBarrellOrgan).filter(SqlBarrellOrgan.owner == owner.id
                                                      ).first()
        
        if not organ:
            return None
        
        instance = cls(organ)
        return instance

    def __init__(self, organ):
        self.name = organ.name
        self.description = organ.label
        self.path = '/barrell-organs/' + self.name + '/'

    def __bool__(self):
        return True
    
    def SQL(self):
        return db_session.create_session().query(SqlUser).filter(
            SqlUser.discord_id == self.discord_id).first()
    

class User:
    def __init__(self, id):
        self.discord_id = id
        
        db_sess = db_session.create_session()
        if not db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first():
            new = SqlUser(discord_id=id)
            db_sess.add(new)
            db_sess.commit()
        return None

    def __bool__(self):
        return True

    async def DISCORD(self):
        return await client.fetch_user(self.discord_id)
    
    def SQL(self):
        return db_session.create_session().query(SqlUser).filter(
            SqlUser.discord_id == self.discord_id).first()
    
    def organ(self):
        return db_session.create_session().query(SqlBarrellOrgan).filter(
            SqlBarrellOrgan.owner == self.SQL().id).first()

    @property
    def karma(self):
        db_sess = db_session.create_session()
        return db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first().karma

    def is_blacklisted(self):
        db_sess = db_session.create_session()
        return db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first().blacklist

    def add_to_blacklist(self):
        db_sess = db_session.create_session()
        user = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first()
        user.blacklist = True
        db_sess.commit()

    def make_mod(self):
        db_sess = db_session.create_session()
        user = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first()
        user.mod = True
        db_sess.commit()

    def unmod(self):
        db_sess = db_session.create_session()
        user = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first()
        user.mod = False
        db_sess.commit()      

    def remove_from_blacklist(self):
        db_sess = db_session.create_session()
        user = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first()
        user.blacklist = False
        db_sess.commit()

    def add_karma(self, add):
        db_sess = db_session.create_session()
        user = db_sess.query(SqlUser).filter(SqlUser.discord_id == self.discord_id
                                             ).first()
        user.karma = user.karma + add
        db_sess.commit()


def user_from_string(string):
    try:
        return User(int(string))
    except ValueError:
        if string.startswith('<@!') and string[-1] == '>':
            return User(int(string[3:-1]))
    return False


@client.event
async def on_message(msg: discord.Message):
    if msg.author == client.user:
        return

    if msg.channel.type is discord.ChannelType.private:
        if msg.author.id == 408980792165924884 or msg.author.id == 731763520416514060 or msg.author.id == 561522627118759956:
            print(msg.content)
            import random
            prefix = ['воу,', 'блин,', 'ого', 'ну,', 'ладно,', 'йоу,', '', '', '', '', '']
            data = [(['звучит', 'вышло', 'вполне', 'а вот тут уже реально', 'вообще', 'объективно', 'достаточно', 'на самом деле'],
                     ['круто', 'достойно', 'хорош', 'прикольно', 'драйвово', 'мемно', 'диско', 'респектабельно', 'мощно', 'здорово', 'неплохо', 'как-то не очень если честно']),
                    (['действительно крутой', 'неплохой', 'эпичный', 'мощный', 'правда хороший', 'ЗАЕБИСЬ', 'качёвый блин'],
                     ['трек']),
                    (['действительно крутая', 'неплохая', 'эпичная', 'мощная', 'правда хорошая', 'ЗАЕБИСЬ', 'качёвая блин'],
                     ['песня', 'музыка'])]
            d = [random.choice(var) for var in random.choice(data)]
            random.shuffle(d)
            message = ' '.join([random.choice(prefix)] + d).strip()
            await msg.channel.send(message + '.')
    if msg.content.startswith('кж!карма'):
        args = msg.content.split()
        if len(args) == 1:
            user = User(msg.author.id)
        else:
            user = user_from_string(args[1])
            if not user:
                embed = basic_embed(':x: Ээээ....',
                                    'кто?')
                embed.color = discord.Color.red()
                await msg.channel.send(embed=embed)
                return
        duser = await user.DISCORD()
        embed = basic_embed('Профиль ' + duser.name,
                            'Постовая карма: ' + str(user.karma))
        embed.set_thumbnail(url=duser.avatar.url)
        await msg.channel.send(embed=embed)

    elif msg.content.startswith('кж!шарманка'):
        if not ORGANS_AVAILABLE: return
        user=msg.author

        barrellorgan = BarellOrgan(user.id)

        voice_channel=user.voice.voice_channel
        if voice_channel != None:
            embed = basic_embed(user.name + ' запустил свою шарманку',
                                'Все присутствующие в ' + voice_channel.name + 'ошеломлены..')
            embed.set_thumbnail(url=user.avatar.url)
            await msg.channel.send(embed=embed)

            vc = await client.join_voice_channel(voice_channel)
            player = vc.create_ffmpeg_player('vuvuzela.mp3')
            player.start()
            while not player.is_done():
                await asyncio.sleep(1)
            player.stop()
            await vc.disconnect()

    elif msg.content.startswith('кж!деньлогова2022'):
        await msg.channel.send('ща будет жди')
        with requests.get(msg.author.avatar.url) as r:
            img_data = r.content
            ava = Image.open(BytesIO(img_data))
        ava = ava.resize((2000, 2000))
        ava.paste(frame, (0, 0), frame)
        with BytesIO() as image_binary:
            ava.save(image_binary, 'PNG')
            image_binary.seek(0)
            await msg.channel.send(file=discord.File(fp=image_binary, filename='result.png'))
        
    elif msg.content.startswith('кж!хелп'):
        embed = basic_embed('Справка',
                            '**кж!карма** - посмотреть свой профиль.\n'
                            '**кж!карма {пользователь}** - посмотреть чужой профиль.\n'
                            '**кж!лидеры {страница}** - посмотреть список лидеров по карме.')
        await msg.channel.send(embed=embed)
    elif msg.content.startswith('кж!лидеры'):
        args = msg.content.split()
        if len(args) == 1:
            page = 1
        else:
            try:
                page = int(args[1])
            except ValueError:
                page = 1

        db_sess = db_session.create_session()
        users = db_sess.query(SqlUser).filter(SqlUser.karma != 0).order_by(SqlUser.karma.desc())
        maxpage = math.ceil(users.count() / 10)
        page = max(1, min(maxpage, page))
        text = ''
        for i, user in enumerate(users[(page - 1) * 10:page * 10]):
            text += '**' + str((page - 1) * 10 + i + 1) + '.** `[' + str(user.karma) + ']` <@!' + str(user.discord_id) + '>\n'
        embed = basic_embed(title='Топ кармов (Страница ' + str(page) + '/' + str(maxpage) + ')',
                            text=text)
        
        await msg.channel.send(embed=embed)
        
    elif msg.content.startswith('кж!блеклист') and User(msg.author.id).SQL().mod:
        args = msg.content.split()
        if len(args) == 1:
            db_sess = db_session.create_session()
            users = db_sess.query(SqlUser).filter(SqlUser.blacklist == True)
            embed = basic_embed(title='Чёрный список Криптожабы.',
                                text='Вот они, сверху вниз:')
            for i, user in enumerate(users):
                u = await User(user.discord_id).DISCORD()
                embed.add_field(name=str(i + 1) + '. ' + u.name, value='_ _')
            await msg.channel.send(embed=embed)
        elif args[1] == 'добавить':
            user = User(int(msg.content.split()[2]))
            user.add_to_blacklist()
            d = await user.DISCORD()
            embed = basic_embed(title=d.name + ' добавлен в чёрный список.',
                                text='Смейтесь его! Гоняйте над ним!')
            embed.set_thumbnail(url=d.avatar_url)
            await msg.channel.send(embed=embed)
        elif args[1] == 'убрать':
            user = User(int(msg.content.split()[2]))
            user.remove_from_blacklist()
            d = await user.DISCORD()
            embed = basic_embed(title=d.name + ' вычтен из чёрного списка.',
                                text='на этот раз прощаем.')
            embed.set_thumbnail(url=d.avatar_url)
            await msg.channel.send(embed=embed)


async def reaction_event(payload, meaning=1):
    channel = await client.fetch_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    if msg.webhook_id:
        return
    user = await client.fetch_user(payload.user_id)
    if user.id == msg.author.id or user.bot or msg.author.bot:
        return
    if payload.channel_id not in CONFIG['channel_whitelist'] and True not in [word in channel.name for word in CONFIG['channel_whitelist_keywords']]:
        return
    if User(payload.user_id).is_blacklisted() or User(msg.author.id).is_blacklisted():
        return
   # if days_delta(msg) >= CONFIG['message_expiration_date']:
   #     return
    if payload.emoji.id in CONFIG['praise']:
        user = User(msg.author.id)
        user.add_karma(CONFIG['coeff'] * meaning)

@client.event
async def on_raw_reaction_add(payload):
    await reaction_event(payload, 1)

@client.event
async def on_raw_reaction_remove(payload):
    await reaction_event(payload, -1)

@client.event
async def on_ready():
    print('Бот запущен как ', client.user.name)
    User(408980792165924884).make_mod()

if __name__ == '__main__':
    db_session.global_init('botdata.db')
    print('Запуск бота')
    client.run(PROD_TOKEN)
    