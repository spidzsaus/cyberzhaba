from hub import dm_session, DMSession, EndDMSession
from helper_tools import basic_embed
import discord
from secret_data import SECRETSANTA_PARTICIPANTS, SECRETSANTA_RECIPIENTS, FEMALE_PRONOUNS

@dm_session('похвали меня')
class ComplimentOneliner(DMSession):
    async def first(self, msg):
        if msg.author.id == 408980792165924884 or msg.author.id == 731763520416514060 or msg.author.id == 561522627118759956:
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
        raise EndDMSession

@dm_session('создать шарманку!')
class BarrellOrganCrafting(DMSession):
    async def first(self, msg):
        if msg.author.id not in SECRETSANTA_PARTICIPANTS:
            await msg.channel.send(embed=basic_embed(title=':x: Эх.',
                                                     text="Извини, но ты не участвуешь в ивенте.",
                                                     color=discord.Color.og_blurple()))
            raise EndDMSession
        text = f'Привет, {msg.author.name}.'
        text += '\n\n'
        text += f'Итак, сейчас мы будем вместе делать шарманку.'
        text += '\n'
        if msg.author.id in FEMALE_PRONOUNS:
            text += f'Готова узнать, кому из логовцев тебе довелось готовить подарок?'
        else:
            text += f'Готов узнать, кому из логовцев тебе довелось готовить подарок?'
        
        await msg.channel.send(embed=basic_embed(title='[1/5] :question: ',
                                                 text=text,
                                                 color=discord.Color.og_blurple()))
        self.next(self.reveal)
    
    async def reveal(self, msg):
        recipient = SECRETSANTA_RECIPIENTS[SECRETSANTA_PARTICIPANTS.index(msg.author.id)]

        text = f'Сочту это за да.'
        text += '\n\n'
        text += f':drum::drum::drum::drum::drum::drum::drum:'
        text += '\n\n'
        text += f'Вот это да! **Ты делаешь шарманку для <@!{recipient}>!**'
        text += '\n'
        if recipient in FEMALE_PRONOUNS:
            text += f'Только тссс..... Она не должна об этом узнать.'
        else:
            text += f'Только тссс..... Он не должен об этом узнать.'
        text += '\n\n'
        text += f'Что-ж, приступим к работе. Скажи что-нибудь для продолжения.'
        
        
        await msg.channel.send(embed=basic_embed(title='[2/5] :flushed: ',
                                                 text=text,
                                                 color=discord.Color.og_blurple()))
        self.next(self.reveal)
    
    #async def texture(self, msg):
