'''
Date: 05/06/2019
Developer: Andrew Serrra
Description: Class that contains settings for the operations,
             saves the data in a file in case of server downtime.
'''
import json
from scripts.helpers import getRandomColor

class Settings:

    def __init__(self):
        # read file to get all the data that is needed
        with open("settings.txt", "r") as f:
            data = json.load(f)

            self.file_name = data["file_name"]
            self.team_names = data["team_names"]
            self.channel_access = data["channel_access"]
            self.commands_avail = data["commands_avail"]
            self.commands_avail_help = data["commands_avail_help"]

    def setTeam(self, data_ch_name, data_text, action=None):

        return_msg = ""

        # returns false if the channel does not have access to
        # change settings
        if data_ch_name not in self.channel_access["settings"]:
            return "This channel cannot be used to change settings.\nOnly eboard has access."

        if action == "add":
            # add the new team name and save to file.
            self.team_names.append(data_text)
            return_msg = "Successfully added {} from the team list.".format(data_text[-1])

        elif action == "remove":
            # remove the team name and save to file.
            self.team_names.remove(data_text)
            return_msg = "Successfully removed {} from the team list.".format(data_text[-1])

        self.saveSettings()

        return return_msg

    def setFileName(self, new_name):

        self.file_name = new_name
        self.saveSettings()

        return "Changed spreadsheet file name to \"{}\"".format(new_name)

    def getFileName(self):

        return self.file_name

    def getHelpText(self):

        command_help_pair = zip(self.commands_avail["settings"], self.commands_avail_help["settings"])
        attachments = []

        for k, v in command_help_pair:
            attachments.append({
                "title": k,
                "text": v,
                "color": getRandomColor(),
            })

        return attachments

    def saveSettings(self):

        with open("settings.txt", "w") as text_file:
            json.dump({ "file_name": self.file_name,
                        "team_names": self.team_names,
                        "channel_access": self.channel_access,
                        "commands_avail": self.commands_avail,
                        "commands_avail_help": self.commands_avail_help},
                        text_file, indent=4)
