from app.bot.commands_manager import DMSession, EndDMSession
from app.config import cmd_manager

@cmd_manager.dm_session('похвали меня')
class ComplimentOneliner(DMSession):
    async def first(self, msg):
        if msg.author.id == 408980792165924884 or msg.author.id == 731763520416514060 or msg.author.id == 561522627118759956:
            import random
            prefix = ['воу,', 'блин,', 'ого', 'ну,', 'ладно,', 'йоу,', '', '', '', '', '']
            data = [(['звучит', 'вышло', 'вполне', 'а вот тут уже реально', 'вообще', 'объективно', 'достаточно', 'на самом деле'],
                     ['круто', 'достойно', 'хорош', 'прикольно', 'драйвово', 'мемно', 'диско', 'респектабельно', 'мощно', 'здорово', 'неплохо', 'как-то не очень если честно']),
                    (['действительно крутой', 'неплохой', 'эпичный', 'мощный', 'правда хороший', 'зашибись', 'качёвый блин'],
                     ['трек']),
                    (['действительно крутая', 'неплохая', 'эпичная', 'мощная', 'правда хорошая', 'зашибись', 'качёвая блин'],
                     ['песня', 'музыка'])]
            d = [random.choice(var) for var in random.choice(data)]
            random.shuffle(d)
            message = ' '.join([random.choice(prefix)] + d).strip()
            await msg.channel.send(message + '.')
        raise EndDMSession