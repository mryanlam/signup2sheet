from typing import Dict, List
from ruamel.yaml import YAML
from raid_helper_aggregator import raid_helper_aggregator
import discord

client = discord.Client()
raid_helper_id = 579155972115660803


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$scrape'):
        print("Test command called")
        print(message.channel.id)
        raid_ids = await _scrape_channel(message.channel)
        raid_helper = raid_helper_aggregator(raid_ids, config["token"])
        raid_helper.build_output()
        await message.channel.send(raid_helper.output)


async def _scrape_channel(channel) -> List[str]:
    res = list()
    async for elem in channel.history():
        print(elem)
        if elem.author.id == raid_helper_id:
            print("Found raid-helper msg {}".format(elem.id))
            res.append(str(elem.id))
    return res


def read_config(path: str) -> Dict[str, str]:
    with open(path, 'r') as f:
        yaml = YAML()
        config = yaml.load(f)
        return {
            "token": config["token"],
            "sheet": config["sheet"],
            "discord_token": config["discord_token"]
        }


config = read_config("conf.yaml")
if __name__ == '__main__':
    client.run(config["discord_token"])
