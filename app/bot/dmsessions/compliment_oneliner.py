import random
from app.bot.dm_sessions import DMSession, EndDMSession


# @cmd_manager.dm_session('похвали меня')
class ComplimentOneliner(DMSession):
    async def first(self, msg):
        if msg.author.id in (408980792165924884, 731763520416514060, 561522627118759956):
            prefix = ['воу,', 'блин,', 'ого', 'ну,', 'ладно,', 'йоу,', '', '', '', '', '']
            data = [(['звучит', 'вышло', 'вполне', 'а вот тут уже реально',
                      'вообще', 'объективно', 'достаточно', 'на самом деле'],
                     ['круто', 'достойно', 'хорош', 'прикольно', 'драйвово',
                      'мемно', 'диско', 'респектабельно', 'мощно', 'здорово',
                      'неплохо', 'как-то не очень если честно']),
                    (['действительно крутой', 'неплохой', 'эпичный', 'мощный',
                      'правда хороший', 'зашибись', 'качёвый блин'],
                     ['трек']),
                    (['действительно крутая', 'неплохая', 'эпичная', 'мощная',
                      'правда хорошая', 'зашибись', 'качёвая блин'],
                     ['песня', 'музыка'])]
            data_2 = [random.choice(var) for var in random.choice(data)]
            random.shuffle(data_2)
            message = ' '.join([random.choice(prefix)] + data_2).strip()
            await msg.channel.send(message + '.')
        raise EndDMSession
