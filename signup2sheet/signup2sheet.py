from typing import Dict
from ruamel.yaml import YAML


def read_config(path: str) -> Dict[str, str]:
    with open(path, 'r') as f:
        yaml = YAML()
        config = yaml.load(f)
        return {
            "token": config["token"],
            "sheet": config["sheet"],
            "discord_token": config["discord_token"]
        }


if __name__ == '__main__':
    config = read_config("conf.yaml")
    print(config)
