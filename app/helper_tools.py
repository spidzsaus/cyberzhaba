import discord


def basic_embed(title, text, *fields, color=discord.Color.green()):
    emb = discord.Embed(color=color,
                        title=title,
                        description=text)
    for name, value in fields:
        emb.add_field(name=name, value=value)
    return emb
