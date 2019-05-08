'''
Date: 05/06/2019
Developer: Andrew Serrra
Description: Contains all the commands that are sent from the slack
             channel to be processsed.
'''
import os
from Settings import Settings
from scripts.helpers import *
from scripts.sheets import GSheetsAgent
from flask import abort, Flask, jsonify, request

app = Flask(__name__)

def is_request_valid(request):
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    is_team_id_valid = request.form['team_id'] == os.environ['SLACK_TEAM_ID']

    return is_token_valid and is_team_id_valid

@app.route('/purchase-item', methods=['POST'])
def purchase():

    # Index of the text
    LIST_INDEX_TEXT = 8

    if not is_request_valid(request):
        abort(400)

    settings = Settings()

    # Get text split into words
    data = list(request.form.values())[LIST_INDEX_TEXT].split()

    # check for the data amount
    # if something is missing notify
    if len(data) != 6:
        return jsonify({
            "response_type" : "in_channel",
            "text": "You have to have all four data filled in.",
            "attachments" :[
                {
                "text": "Hint: In order, write: <Team> <Part-name> <Quantity> <Price per unit> <Company> <Link>"
                }
            ],
        })

    t_name, p_name, quantity, price_unit, company, link = (word for word in data)

    # check if the numerical entries are valid
    try:
        data[2], data[3] = int(quantity), int(price_unit)

    except ValueError:
        return jsonify({
            "response_type" : "in_channel",
            "text": "Values for quantity and price per unit are not valid.",
            "attachments" :[
                {
                "text": "Hint: The values should not contain any character except integers."
                }
            ],
        })

    if t_name not in settings.team_names:
        return jsonify({
            "response_type" : "in_channel",
            "text": "Team name has to be one of {}.".format(", ".join(t for t in settings.team_names)),
        })


    gs_agent = GSheetsAgent()
    # add the data in the spreadsheet
    gs_agent.addGSheetsRow(data)

    return jsonify({
        "response_type": "in_channel",
        "text" : "Successfully added\n\t\tTeam: {}\
                                    \n\t\tPart: {}\
                                    \n\t\tQuantity: {}\
                                    \n\t\tPrice per unit: ${}\
                                    \n\t\tCompany: {}\
                                    \n\t\tLink: {}\
                  \nto the pruchasing list.".format(t_name, p_name, quantity, price_unit, company, link),
        "attachments" : [
            {
                "text" : "Notify Eboard if there is a mistake."
            }
        ],
    })

@app.route('/set-setting', methods=['POST'])
def setSettings():

    COMMAND_INDEX = 0

    if not is_request_valid(request):
        abort(400)

    # Request from slack
    data = request.form

    settings = Settings()
    commands_available = settings.commands_avail["settings"]

    data_text = parseCommands(data["text"])

    if data_text[COMMAND_INDEX] not in commands_available:
        return jsonify({
            "response_type": "in_channel",
            "text": "Command do not match {}".format(", ".join(command for command in commands_available)),
        })

    # Message to add to json response
    response_msg = ""

    if data_text[COMMAND_INDEX] == "--add-team":
        # set the response message according to channel access
        # and if the team is not already created
        if data_text[-1] not in settings.team_names:
            response_msg = settings.setTeam(data["channel_name"], data_text, action="add")
        else:
            response_msg = "Team already in the list."
    elif data_text[COMMAND_INDEX] == "--remove-team":
        # set the response message according to channel access
        # and team is already created
        if data_text[-1] in settings.team_names:
            response_msg = settings.setTeam(data["channel_name"], data_text, action="remove")
        else:
            response_msg = "Team not in the list."

    return jsonify({
        "response_type": "in_channel",
        "text": response_msg,
    })
