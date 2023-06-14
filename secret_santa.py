from secret_data import SECRETSANTA_PARTICIPANTS, EXES, SECRETSANTA_QUITTED

import logging

import random
SECRETSANTA_RECIPIENTS = SECRETSANTA_PARTICIPANTS[:]
for seed in range(4948395347374, 23894728374283429):
    random.seed(seed)
    random.shuffle(SECRETSANTA_RECIPIENTS)
    try:
        for a, b in EXES:
            assert SECRETSANTA_RECIPIENTS[SECRETSANTA_PARTICIPANTS.index(a)] != b
            assert SECRETSANTA_RECIPIENTS[SECRETSANTA_PARTICIPANTS.index(b)] != a
        for i in range(len(SECRETSANTA_PARTICIPANTS)):
            assert SECRETSANTA_PARTICIPANTS[i] != SECRETSANTA_RECIPIENTS[i]
        break
    except AssertionError:
        continue

logging.info('Generated Secret Santa player match table with a seed ' + str(seed))



class SecretSantaPlayer:
    is_player = False
    is_in_the_game = False

    all_players = SECRETSANTA_PARTICIPANTS
    player_matches = SECRETSANTA_RECIPIENTS
    quited_players = SECRETSANTA_QUITTED
    
    def __init__(self, discord_id):
        self.discord_id = discord_id
        self.is_player = (discord_id in SecretSantaPlayer.all_players)
        self.is_in_the_game = not (discord_id in SecretSantaPlayer.quited_players)
        if self.is_player:
            self.id = SecretSantaPlayer.all_players.index(discord_id)
        else:
            self.id = None

    def get_match(self):
        if not self.is_player:
            return None
        player = SecretSantaPlayer(SecretSantaPlayer.player_matches[self.id])
        if not player.is_in_the_game:
            return player.get_match()
        return player

    def __bool__(self):
        return self.is_player and self.is_in_the_game