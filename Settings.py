'''
Date: 05/06/2019
Developer: Andrew Serrra
Description: Class that contains settings for the operations,
             saves the data in a file in case of server downtime.
'''
import json

class Settings:

    def __init__():
        # read file to get all the data that is needed
        with open("settings.txt", "r") as f:
            data = json.loads(f)

            self.team_names = data["team_names"]
            self.channel_access = data["channel_access"]
            self.commands_avail = data["commands_avail"]

    def setNewTeamName(self, data):
        # get the channel that the message was sent in
        channel_used = data["channel_name"]

        if channel_used not in self.channel_access["settings"]:
            return False

        # add the new team name and save to file.
        self.team_names.append(data["text"])
        self.saveSettings()

        assert isinstance(data, list)

        return True

    def saveSettings(self):

        with open("settings.txt", "w") as f:
            json.dumps({
                "team_names": self.team_names,
                "channel_access": self.channel_access,
                "commands_avail": self.commands_avail,
            }, f)
