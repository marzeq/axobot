import json


def get_prefix(client, message):  # noqa
    if message.guild is None:
        return "--"
    with open('config/config.json', 'r') as f:  # noqa
        config = json.load(f)

    return config[str(message.guild.id)]["prefix"]
