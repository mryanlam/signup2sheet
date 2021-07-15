import requests
from time import sleep
from typing import List

#TODO Integrate with discord for channel scrape
#TODO Integrate with gspread for automatic upload
#TODO it seems raid ids are 18 characters. Confirm and validate on it.

class raid_helper_aggregator:
    def __init__(self, raid_ids: List[str], token: str):
        #Input: list of strings
        #Output: void
        #Sets endpoint, headers, raidids, output headers, and pulls raidhelper data.
        
        self.endpoint = 'http://51.195.103.14:3000/api/raids/'
        self.headers = {'Authorization': token}
        self.raid_ids = list(set(self.validate_raid_ids(raid_ids)))

        self.output = [['player', 'class', 'role', 'spec'] + raid_ids]
        
        self.class_remap = {'Guardian': 'Druid',
                            'Feral': 'Druid',
                            'Restoration': 'Druid',
                            'Balance': 'Druid',
                            'Beastmastery': 'Hunter',
                            'Survival': 'Hunter',
                            'Marskmanship': 'Hunter',
                            'Arcane': 'Mage',
                            'Fire': 'Mage',
                            'Frost': 'Mage',
                            'Holy1': 'Paladin',
                            'Protection1': 'Paladin',
                            'Retribution': 'Paladin',
                            'Holy1': 'Paladin',
                            'Protection1': 'Paladin',
                            'Retribution': 'Paladin',
                            'Discipline': 'Priest',
                            'Holy1': 'Priest',
                            'Shadow': 'Priest',
                            'Assassination': 'Rogue',
                            'Combat': 'Rogue',
                            'Subtlety': 'Rogue',
                            'Elemental': 'Shaman',
                            'Enhancement': 'Shaman',
                            'Restoration1': 'Shaman',
                            'Affliction': 'Warlock',
                            'Demonology': 'Warlock',
                            'Destruction': 'Warlock',
                            'Arms': 'Warrior',
                            'Fury': 'Warrior',
                            'Protection': 'Warrior'}
        
        self.get_signup_data()
        
    def validate_raid_ids(self, raid_ids):
        #Input: list
        #Output: list of strings
        #Validation for user input.
        
        try:
            int_given = True
            str_given = True
            for raid_id in raid_ids:
                if type(raid_id) != int:
                    int_given = False
                if type(raid_id) != str:
                    str_given = False
            if str_given:
                return raid_ids
            elif int_given:
                return [str(raid_id) for raid_id in raid_ids]
            else:
                print('You should probably provide valid Raid IDs.')
        except Exception as e:
            print('This one is on me. Send the error to Andrew.')
            print(e)
            
        
    def get_signup_data(self):
        #Input: void
        #Output: void
        #Grabs the signup data from raid-helper.
        #There is a 5s wait between requests.
        
        self.user_data = []
        for raid_id in self.raid_ids:
            self.user_data = self.user_data + requests.get(self.endpoint + raid_id, headers = self.headers).json()['raidusers']
            sleep(5)
        self.users = sorted(list(set([user['username'] for user in self.user_data])))

    def get_player(self, username):
        #Input: string
        #Output: list
        #Returns signups data for a specified discord username.
        
        return [user for user in self.user_data if user['username'] == username]
    
    def get_role(self, spec_string):
        #Input: string
        #Output: string
        #Returns the in-game role of a raid-helper spec.

        #Why is role an inconsistent classifier?
        
        if 'Protection' in spec_string or 'Guardian' in spec_string:
            return 'Tank'
        elif 'Restoration' in spec_string or 'Holy' in spec_string:
            return 'Healer'
        else:
            return 'DPS'
    
    def get_specs(self, player_data):
        #Input: list of dictionaries
        #Output: list of strings
        #Returns all raid-helper specs for a given discord username.
        
        specs = []
        for signup in player_data:
            if signup['spec'] not in specs:
                specs.append(signup['spec'])
        return list(set(specs))
    
    def get_class(self, spec):
        #Input: list of dictionaries
        #Output: list of strings
        #Returns the in-game class associated with a raid-helper spec.

        if spec in self.class_remap.keys():
            return self.class_remap[spec]
        else:
            return 'N/A'
    
    def get_signups(self, player_data, spec):
        #Input: list of dictionaries
        #Output: list of strings
        #Returns signups for a given in-game character.
        
        signup_ids = []
        for signup in player_data:
            if signup['spec'] == spec:
                signup_ids.append(signup['raidid'])
        return list(set(signup_ids))
        
    
    def build_output(self):
        #Input: void
        #Output: void
        #Ties the class together to generate the desired output structure contained within self.output.
        
        for user in self.users:
            player_data = self.get_player(user)
            specs = self.get_specs(player_data)
            
            for spec in specs:
                row_data = [user.replace('*', '').capitalize()]
                row_data.append(self.get_class(spec))
                row_data.append(self.get_role(spec))
                row_data.append(spec.replace('1', ''))
                raids_attending = self.get_signups(player_data, spec)

                for raid_id in self.raid_ids:
                    if raid_id in raids_attending:    
                        row_data.append('Yes')
                    else:
                        row_data.append('No')

                self.output.append(row_data)
