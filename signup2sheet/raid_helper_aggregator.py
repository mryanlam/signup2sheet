import requests
from time import sleep
from typing import String, List


class raid_helper_aggregator:
    def __init__(self, raid_ids: List[String], token: String):
        self.endpoint = "http://51.195.103.14:3000/api/raids/"
        self.headers = {"Authorization": token}
        self.raid_ids = raid_ids
        self.output = [['player', 'class', 'role'] + raid_ids]
        self.get_signup_data()

    def get_signup_data(self):
        self.user_data = []
        for raid_id in self.raid_ids:
            self.user_data = self.user_data + \
                requests.get(self.endpoint + raid_id,
                             headers=self.headers).json()['raidusers']
            sleep(5)
        self.users = sorted(
            list(set([user['username'] for user in self.user_data])))

    def get_player(self, username):
        return [
            user for user in self.user_data if user['username'] == username
        ]

    def build_output(self):
        for user in self.users:
            player_data = self.get_player(user)
            raids_attending = set([entry['raidid'] for entry in player_data])

            row_data = [user.replace('*', '').capitalize()]
            row_data.append(player_data[0]['role'])
            row_data.append(player_data[0]['spec'])

            for raid_id in self.raid_ids:
                if raid_id in raids_attending:
                    row_data.append('Yes')
                else:
                    row_data.append('No')

            self.output.append(row_data)
