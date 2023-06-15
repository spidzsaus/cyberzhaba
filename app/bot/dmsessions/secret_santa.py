import os
from io import BytesIO

import requests
import numpy
import discord
import eyed3
from PIL import Image

from app.helper_tools import basic_embed
from app.secret_santa_data import FEMALE_PRONOUNS
from app.entities.users import User
from app.entities.barrellorgans import BarellOrgan
from app.entities.secret_santa import SecretSantaPlayer

from app.bot.commands_manager import DMSession, EndDMSession
from app.config import cmd_manager


@cmd_manager.dm_session('создать шарманку!')
class BarrellOrganCrafting(DMSession):
    IMG_OFFSET = (118, 39)
    IMG_W = 1044
    IMG_H = 1038
    PAD_W = (1280 - IMG_W) // 2
    PAD_H_U = IMG_OFFSET[1]
    PAD_H_B = 1164 - IMG_H - PAD_H_U

    def __init__(self, msg):
        super().__init__(msg)
        self.user = None
        self.model = None
        self.path = None
        self.secret_santa_player = None
        self.recipient_id = None
        self.author_id = None
        self.bb_lore = None
        self.bb_name = None

    def pickup(self, _):

        model = BarellOrgan.__new__(BarellOrgan,
                                    uid=self.recipient_id)

        if model is None:
            return self.first

        path = os.path.join('data', 'barrellorgans', str(model.sql().id))
        if not os.path.isfile(os.path.join(path, 'melody.mp3')):
            return self.first

        if not os.path.isfile(os.path.join(path, 'image.png')):
            return self.image_preview

        if not model.description:
            return self.lore

        if not model.name:
            return self.name

    async def first(self, msg):
        self.secret_santa_player = SecretSantaPlayer(msg.author.id)

        if not self.secret_santa_player:
            await msg.channel.send(embed=basic_embed(title=':x: Эх.',
                                                     text="Извини, но ты не участвуешь в ивенте.",
                                                     color=discord.Color.og_blurple()))
            raise EndDMSession
        self.recipient_id = self.secret_santa_player.get_match().discord_id
        self.author_id = msg.author.id
        if self.pickup(msg) == self.image_preview:
            text = 'Тааак, такое дело.'
            text += '\n\n'
            text += 'Пока тебя не было, бот успел перезапуститься.'
            text += '\n'
            text += 'В обычной ситуации это значило бы, что крафт шарманки обнулился бы, \
нооо я вижу что у тебя уже готова мелодия шарманки, поэтому вернёмся к этому моменту.'
            text += '\n'
            text += 'Сорян если что-то потерял.'
            text += '\n'
            text += 'Продолжай приикреплять картинку к шарманке.'
            await msg.channel.send(embed=basic_embed(title='[?/5] :warning: ',
                                                    text=text,
                                                    color=discord.Color.og_blurple()))

            path = os.path.join('data', 'barrellorgans')

            self.user = User(msg.author.id)

            self.model = BarellOrgan.__new__(BarellOrgan,
                                            uid=self.recipient_id,
                                            init=True,
                                            author=self.user.sql().id)

            self.path = os.path.join(path, str(self.model.sql().id))
            self.next(self.image_preview)
            return

        if self.pickup(msg) == self.lore:
            text = 'Тааак, такое дело.'
            text += '\n\n'
            text += 'Пока тебя не было, бот успел перезапуститься.'
            text += '\n'
            text += 'В обычной ситуации это значило бы, что крафт шарманки обнулился бы, \
нооо я вижу что у тебя уже готовы мелодия шарманки с картинкой, \
поэтому вернёмся к этому моменту.'
            text += '\n'
            text += 'Сорян если что-то потерял.'
            text += '\n'
            text += 'Продолжай писать подпись к шарманке.'
            await msg.channel.send(embed=basic_embed(title='[?/5] :warning: ',
                                                    text=text,
                                                    color=discord.Color.og_blurple()))

            path = os.path.join('data', 'barrellorgans')

            self.user = User(msg.author.id)

            self.model = BarellOrgan.__new__(BarellOrgan,
                                            uid=self.recipient_id,
                                            init=True,
                                            author=self.user.sql().id)

            self.path = os.path.join(path, str(self.model.sql().id))
            self.next(self.lore)
            return

        if self.pickup(msg) == self.name:
            text = 'Тааак, такое дело.'
            text += '\n\n'
            text += 'Пока тебя не было, бот успел перезапуститься.'
            text += '\n'
            text += 'В обычной ситуации это значило бы, что крафт шарманки обнулился бы, \
    нооо я вижу что у тебя уже готовы мелодия шарманки с картинкой и подписью, поэтому \
вернёмся к этому моменту.'
            text += '\n'
            text += 'Сорян если что-то потерял.'
            text += '\n'
            text += 'Продолжай писать название к шарманке.'
            await msg.channel.send(embed=basic_embed(title='[?/5] :warning: ',
                                                    text=text,
                                                    color=discord.Color.og_blurple()))

            path = os.path.join('data', 'barrellorgans')

            self.user = User(msg.author.id)

            self.model = BarellOrgan.__new__(BarellOrgan,
                                            uid=self.recipient_id,
                                            init=True,
                                            author=self.user.sql().id)

            self.path = os.path.join(path, str(self.model.sql().id))
            self.next(self.lore)
            return


        text = f'Привет, {msg.author.name}.'
        text += '\n\n'
        text += 'Итак, сейчас мы будем вместе делать шарманку.'
        text += '\n'
        if msg.author.id in FEMALE_PRONOUNS:
            text += 'Готова узнать, кому из логовцев тебе довелось готовить подарок?'
        else:
            text += 'Готов узнать, кому из логовцев тебе довелось готовить подарок?'

        await msg.channel.send(embed=basic_embed(title='[1/5] :question: ',
                                                 text=text,
                                                 color=discord.Color.og_blurple()))
        self.next(self.reveal)

    async def reveal(self, msg):
        text = 'Сочту это за да.'
        text += '\n\n'
        text += ':drum::drum::drum::drum::drum::drum::drum:'
        text += '\n\n'
        text += f'Вот это да! **Ты делаешь шарманку для <@!{self.recipient_id}>!**'
        text += '\n'
        if self.recipient_id in FEMALE_PRONOUNS:
            text += 'Только тссс..... Она не должна об этом узнать.'
        else:
            text += 'Только тссс..... Он не должен об этом узнать.'
        text += '\n\n'
        text += 'Что-ж, приступим к работе. Скажи что-нибудь для продолжения.'


        await msg.channel.send(embed=basic_embed(title='[2/5] :flushed: ',
                                                 text=text,
                                                 color=discord.Color.og_blurple()))
        self.next(self.melody)

    async def melody(self, msg):
        text = 'Начнём с главного'
        text += '\n\n'
        text += '**Выбери мелодию, которую ты запишешь на свою шарманку.**'
        text += '\n\n'
        text += 'Прикрепи любой файл в формате mp3. Размер: тот, который позволяет тебе дискорд. '
        text += '\n\n'
        text += 'Учтите, что шарманка громкая. Не записывайте на неё ничего, \
чего вы не хотели бы чтобы слышала публика.'

        await msg.channel.send(embed=basic_embed(title='[3/5] :notes: ',
                                                 text=text,
                                                 color=discord.Color.og_blurple()))

        path = os.path.join('data', 'barrellorgans')
        if not os.path.exists(path):
            os.makedirs(path)

        self.user = User(msg.author.id)

        self.model = BarellOrgan.__new__(BarellOrgan,
                                         uid=self.recipient_id,
                                         init=True,
                                         author=self.user.sql().id)

        self.path = os.path.join(path, str(self.model.sql().id))
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.next(self.texture)

    async def texture(self, msg: discord.Message):
        async def retry(hint):
            text = 'Что-то пошло не так'
            text += '\n\n'
            text += hint
            await msg.channel.send(embed=basic_embed(title='[3/5] :notes: ',
                                                     text=text,
                                                     color=discord.Color.red()))
            self.next(self.texture)

        if len(msg.attachments) != 1:
            await retry('Прикрепи к сообщению один файл')
            return
        att = msg.attachments[0]
        if not att.filename.endswith('.mp3'):
            await retry('Прикрепи файл в формате .mp3')
            return
        melody_path = os.path.join(self.path, 'melody.mp3')
        with open(melody_path, mode='wb') as melody_f:
            await att.save(melody_f)
        if eyed3.load(melody_path) is None:
            await retry('Что-то пошло не так, кажется файл бит. Попробуй другой')
            os.remove(melody_path)
            return

        text = 'Харош.'
        text += '\n\n'
        text += '**Теперь давай разрисуем шарманку и сделаем её красивой.**'
        text += '\n\n'
        text += 'Прикрепи любой файл в формате изображения. \
Размер: тот, который позволяет тебе дискорд.'
        text += '\n\n'
        text += 'Учтите, что шарманка яркая. Не рисуйте на ней ничего, \
чего вы не хотели бы чтобы видела публика.'

        await msg.channel.send(embed=basic_embed(title='[4/5] :art: ',
                                                 text=text,
                                                 color=discord.Color.og_blurple()))
        self.next(self.image_preview)

    async def image_preview(self, msg):
        async def retry(hint):
            text = 'Что-то пошло не так'
            text += '\n\n'
            text += hint
            await msg.channel.send(embed=basic_embed(title='[4/5] :art: ',
                                                     text=text,
                                                     color=discord.Color.red()))
            self.next(self.image_preview)

        if len(msg.attachments) != 1:
            await retry('Прикрепи к сообщению один файл')
            return
        att = msg.attachments[0]
        if not (att.filename.endswith('.png') or att.filename.endswith('.jpg')):
            await retry('Прикрепи файл в формате .png или .jpg')
            return

        try:
            with requests.get(att.url, timeout=10) as request:
                img_data = request.content
                img = Image.open(BytesIO(img_data))
        except requests.exceptions.RequestException:
            await retry('Попробуй другой файл, может...')
            return

        await msg.channel.send(
            embed=basic_embed(
                title='[4/5] :art: ',
                text='Ща, прикину как это будет выглядеть, подожди чуток',
                color=discord.Color.og_blurple()
            )
        )

        img = img.resize((self.IMG_W, self.IMG_H))
        img = img.convert('RGBA')
        texture = numpy.array(img)
        source = numpy.array(Image.open(os.path.join('assets', 'bomask.png')).convert('RGBA')) / 255
        texture = numpy.pad(
            texture,
            ((self.PAD_H_U, self.PAD_H_B), (self.PAD_W, self.PAD_W), (0, 0)),
            'constant'
        )
        masked = texture * source
        result = Image.fromarray(masked.astype(numpy.uint8))
        overlay = Image.open(os.path.join('assets', 'booverlay.png')).convert('RGBA')
        result.paste(overlay, (0, 0), overlay)
        result.save(os.path.join(self.path, 'image.png'), 'PNG')

        with BytesIO() as image_binary:
            result.save(image_binary, 'PNG')
            image_binary.seek(0)
            await msg.channel.send(
                embed=basic_embed(
                    title='[4/5] :art: ',
                    text='Во, готово. Смотри как это будет выглядеть. \
Норм? Если норм, то скажи "норм" чтобы продолжить, если нет то прикрепи другое изображение.',
                    color=discord.Color.og_blurple()
                ),
                file=discord.File(fp=image_binary, filename='result.png')
            )

        self.next(self.image_decision)

    async def image_decision(self, msg):
        if msg.content.lower() == 'норм':
            await self.lore(msg)
        else:
            await self.image_preview(msg)

    async def lore(self, msg):
        text = 'ура.'
        text += '\n'
        text += 'Дело за малым'
        text += '\n\n'
        text += '**Придумай текст, который будет выведен на торце шарманки**'
        text += '\n\n'
        text += 'Это может быть пожелание, эпиграммка, эпитафия, небольшое описание, \
всё что только позволит ваша фантазия.'
        text += '\n\n'
        text += 'Учтите, что шарманка ой да вы сами всё понимаете кароче \
не признавайтесь тут в любви'

        await msg.channel.send(embed=basic_embed(title='[5/5] :scroll: ',
                                                 text=text,
                                                 color=discord.Color.og_blurple()))
        self.next(self.name)

    async def name(self, msg):
        self.bb_lore = msg.content
        text = 'Красиво звучит....'
        text += '\n\n'
        text += '**Последний штрих, придумай название своей шарманки**'
        text += '\n\n'
        text += 'Максимум 142 символа.'
        await msg.channel.send(embed=basic_embed(title='[6/5] :speech_balloon: ',
                                                 text=text,
                                                 color=discord.Color.og_blurple()))
        self.next(self.finale)

    async def finale(self, msg):
        async def retry():
            if self.recipient_id in FEMALE_PRONOUNS:
                text = 'алё ты глухая ОГРАНИЧЕНИЕ 142 СИМВОЛА мда....'
            else:
                text = 'алё ты глухой ОГРАНИЧЕНИЕ 142 СИМВОЛА чел....'
            await msg.channel.send(embed=basic_embed(title='[6/5] :speech_balloon: ',
                                                     text=text,
                                                     color=discord.Color.red()))
            self.next(self.finale)
        if not msg.content or len(msg.content) > 142:
            await retry()
            return
        self.bb_name = msg.content

        await msg.channel.send('Шарманка готова!')

        embed = discord.Embed(color=discord.Color.og_blurple(),
                              title='«' + self.bb_name + '»',
                              description=self.bb_lore)

        image = discord.File(os.path.join(self.path, 'image.png'), filename="image.png")
        embed.set_image(url="attachment://image.png")

        await msg.channel.send(embed=embed, file=image,)

        sqlmodel, sess = self.model.sql(return_sess=True)
        sqlmodel.name = self.bb_name
        sqlmodel.label = self.bb_lore
        sess.add(sqlmodel)
        sess.commit()

        await msg.channel.send('Благодарю за участие <3! Если передумаешь, \
ты всегда можешь изменить шарманку, повторно вызвав команду "создать шарманку!", \
новая шарманка просто встанет на место старой.')
        raise EndDMSession
