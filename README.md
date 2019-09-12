# PurchasingApp

This is a Slack app that receives a message from club members in the channel and adds the data into an google spreadsheet for robotics club purchasing operations.

## Slash Commands

1. /purchase
    - **Access channel:** #eboard, #purchasing
    - **Purpose:** It will trigger a dialog and add the values to the purchasing list for the                          treasurer to do ordering of the product.

2. /set \<command\> \<new-setting\>
    - **Access channel:** #eboard
    - **Purpose:** It will change the settings that are saved in a text file. You can add and remove teams that are active.                      You can change the file name used for spreadsheet.
    - **Note:** Only restricted to eboard members, you will receive an error message if tried to call from other channels. The                 command must have two hyphens leading the command, i.e "--add-team". If there is a case that one parameter has                 to have a space in between, you will receive an error message. Use underscores (_) to have them counted as one                 parameter.
    
## Settings.txt
Contains a json object for all the settings that are loaded when an instance is created.

| Key | Value Type |
|-----|------------|
| file_name | string |
| team_names | list |
| channel_access | dict |
| commands_avail | dict |
| commands_avail_help | dict |
