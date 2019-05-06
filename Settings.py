'''
Date: 05/06/2019
Developer: Andrew Serrra
Description: Class that contains settings for the operations,
             saves the data in a file in case of server downtime.
'''
import json

class Settings:

    def __init__(self):
        # read file to get all the data that is needed
        with open("settings.txt", "r") as f:
            data = json.load(f)

            self.team_names = data["team_names"]
            self.channel_access = data["channel_access"]
            self.commands_avail = data["commands_avail"]

    def setNewTeamName(self, data_ch_name, data_text):
        # returns false if the channel does not have access to
        # change settings
        if data_ch_name not in self.channel_access["settings"]:
            return False

        # add the new team name and save to file.
        self.team_names.append(data_text[-1])
        self.saveSettings()

        return True

    def saveSettings(self):

        with open("settings.txt", "w") as text_file:
            json.dump({ "team_names": self.team_names,
                        "channel_access": self.channel_access,
                        "commands_avail": self.commands_avail}, text_file)
