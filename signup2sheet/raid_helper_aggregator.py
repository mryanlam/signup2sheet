import requests
from time import sleep
from typing import List

class raid_helper_aggregator:
    def __init__(self, raid_ids: List[str], token: str, endpoint: str):
        #Input: list of strings
        #Output: void
        #Sets endpoint, headers, raidids, output headers, and pulls raidhelper data.
        
        self.endpoint = endpoint
        self.headers = {"Authorization": token}
        self.raid_ids = list(set(self.validate_raid_ids(raid_ids)))

        self.class_remap = {"Guardian": "Druid",
                            "Feral": "Druid",
                            "Restoration": "Druid",
                            "Balance": "Druid",
                            "Beastmastery": "Hunter",
                            "Survival": "Hunter",
                            "Marskmanship": "Hunter",
                            "Arcane": "Mage",
                            "Fire": "Mage",
                            "Frost": "Mage",
                            "Holy1": "Paladin",
                            "Protection1": "Paladin",
                            "Retribution": "Paladin",
                            "Discipline": "Priest",
                            "Holy": "Priest",
                            "Shadow": "Priest",
                            "Assassination": "Rogue",
                            "Combat": "Rogue",
                            "Subtlety": "Rogue",
                            "Elemental": "Shaman",
                            "Enhancement": "Shaman",
                            "Restoration1": "Shaman",
                            "Affliction": "Warlock",
                            "Demonology": "Warlock",
                            "Destruction": "Warlock",
                            "Arms": "Warrior",
                            "Fury": "Warrior",
                            "Protection": "Warrior"}
        
        self.get_signup_data()

        self.output = [["player", "class", "role", "spec"] + self.raid_names]
        
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
                print("You should probably provide valid Raid IDs.")
        except Exception as e:
            print("This one is on me. Send the error to Andrew.")
            print(e)
            
        
    def get_signup_data(self):
        #Input: void
        #Output: void
        #Grabs the signup data from raid-helper.
        
        self.user_data = []
        self.raid_names = []
        for raid_id in self.raid_ids:
            rha_json = requests.get(self.endpoint + raid_id, headers = self.headers).json()
            self.user_data = self.user_data + rha_json["raidusers"]
            self.raid_names.append(rha_json["raids"]["name"])
        self.users = sorted(list(set([user["username"] for user in self.user_data])))

    def get_player(self, username):
        #Input: string
        #Output: list
        #Returns signups data for a specified discord username.
        
        return [user for user in self.user_data if user["username"] == username]
    
    def get_role(self, spec_string):
        #Input: string
        #Output: string
        #Returns the in-game role of a raid-helper spec.

        #Why is role an inconsistent classifier?
        
        if "Protection" in spec_string or "Guardian" in spec_string:
            return "Tank"
        elif "Restoration" in spec_string or "Holy" in spec_string:
            return "Healer"
        else:
            return "DPS"
    
    def get_specs(self, player_data):
        #Input: list of dictionaries
        #Output: list of strings
        #Returns all raid-helper specs for a given discord username.
        
        specs = []
        for signup in player_data:
            if signup["spec"] not in specs:
                specs.append(signup["spec"])
        return list(set(specs))
    
    def get_class(self, spec):
        #Input: list of dictionaries
        #Output: list of strings
        #Returns the in-game class associated with a raid-helper spec.

        if spec in self.class_remap.keys():
            return self.class_remap[spec]
        else:
            return "N/A"
    
    def get_signups(self, player_data):
        #Input: list of dictionaries
        #Output: list of strings
        #Returns signups for a given discord username.

        return list(set([signup["raidid"] for signup in player_data]))
        
    
    def build_output(self):
        #Input: void
        #Output: void
        #Ties the class together to generate the desired output structure contained within self.output.
        
        for user in self.users:
            player_data = self.get_player(user)
            specs = self.get_specs(player_data)
            raids_attending = self.get_signups(player_data)
            raid_data = ["Yes" if raid_id in raids_attending else "No" for raid_id in self.raid_ids]
            
            for spec in specs:
                char_data = [user.replace("*", "").capitalize()]
                char_data.append(self.get_class(spec))
                char_data.append(self.get_role(spec))
                char_data.append(spec.replace("1", ""))
                row_data = char_data + raid_data

                self.output.append(row_data)
