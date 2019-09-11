'''
Date: 05/06/2019
Developer: Andrew Serrra
Description: Contains all the commands that are sent from the slack
             channel to be processsed.
'''
import os
from Settings import Settings
from scripts.helpers import parseCommands
from sheets import GSheetsAgent
from flask import abort, Flask, jsonify, request, make_response, Response
from slack import WebClient
import json

app = Flask(__name__)

# Slack client for Web API requests
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
slack_client = WebClient(SLACK_BOT_TOKEN)

def is_request_valid(request):
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    is_team_id_valid = request.form['team_id'] == os.environ['SLACK_TEAM_ID']

    print("Token is valid: ",is_token_valid)
    print("Team Id is valid: ",is_team_id_valid)

    return is_token_valid and is_team_id_valid


@app.route('/', methods=['GET'])
def index():
    return make_response("The app is running.", 200)

@app.route('/purchase-form', methods=['POST'])
def purchaseForm():

    # Index of the text
    LIST_INDEX_TEXT = 8

    payload = json.loads(request.form["payload"])
    user_name = payload["user"]
    submission = payload["submission"]

    response_list = [user_name["name"]]

    settings = Settings()

    # check if the numerical entries are valid
    try:
        submission["quantity"], submission["unit_price"] = int(submission["quantity"]), int(submission["unit_price"])

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


    gs_agent = GSheetsAgent(settings)

    for key in submission:
        response_list.append(submission[key])

    # add the data in the spreadsheet
    if not gs_agent.addGSheetsRow(response_list):

        return make_response("", status=500)
        
    else:
        res_text = "Successfully added\n\t\tTeam: {}\
                                            \n\t\tPart: {}\
                                            \n\t\tQuantity: {}\
                                            \n\t\tPrice per unit: ${}\
                                            \n\t\tCompany: {}\
                                            \n\t\tLink: {}\
                        \nto the pruchasing list.".format(submission["team_name"],
                                                        submission["part_name"],
                                                        submission["unit_price"],
                                                        submission["quantity"],
                                                        submission["company"],
                                                        submission["link"])

        slack_client.chat_update(ts=payload["action_ts"], channel=payload["channel"]["id"], text=res_text)

        return make_response("", 200)

@app.route('/purchase-item', methods=['POST'])
def purchase():

    if not is_request_valid(request):
        abort(400)

    # Settings 
    settings = Settings()

    team_name_selection = list({ "label": team, "value": team} for team in settings.team_names)

    message_action = request.form
    user_id = message_action["user_id"]

    print(message_action["trigger_id"])

    open_dialog = slack_client.api_call(
        api_method="dialog.open",
        json={
        "trigger_id":message_action["trigger_id"],
        "dialog":{
            "title": "Purchasing Request Form",
            "submit_label": "Submit",
            "callback_id": user_id + "purchsing_request_form",
            "elements": [
                {
                    "label": "Team Name",
                    "type": "select",
                    "name": "team_name",
                    "placeholder": "-- team name --",
                    "options": team_name_selection,
                },
                {
                    "label": "Part Name",
                    "type": "text",
                    "name": "part_name",
                },
                {
                    "label": "Price per Unit",
                    "type": "text",
                    "name": "unit_price",
                    "hint": "Enter the price without multiplying with the quantity.",
                },
                {
                    "label": "Quantity",
                    "type": "text",
                    "name": "quantity",
                },
                {
                    "label": "Company Name",
                    "type": "text",
                    "name": "company",
                    "Hint": "amazon.com",
                },
                {
                    "label": "Link",
                    "type": "text",
                    "name": "link",
                },
                {
                "label": "Additional information",
                "name": "comment",
                "type": "textarea",
                "optional": "true",
                "hint": "Provide additional information if needed."
                },
            ]
        }
        }
    )

    print(open_dialog)

    return "You will receive a message when it is processed."

@app.route('/set-setting', methods=['POST'])
def setSettings():

    COMMAND_INDEX = 0
    TEXT_INDEX = 1

    if not is_request_valid(request):
        abort(400)

    # Request from slack
    data = request.form

    settings = Settings()
    commands_available = settings.commands_avail["settings"]

    # Split the text into a list to separate command and text
    data_text = parseCommands(data["text"])

    if data_text[COMMAND_INDEX] not in commands_available:
        return jsonify({
            "response_type": "in_channel",
            "text": "Command do not match {}".format(", ".join(command for command in commands_available)),
        })

    # Message to add to json response
    attachments = []
    response_msg = ""

    if data_text[COMMAND_INDEX] == "add-team":
        # set the response message according to channel access
        # and if the team is not already created
        if data_text[TEXT_INDEX] not in settings.team_names:
            response_msg = settings.setTeam(data["channel_name"], data_text[TEXT_INDEX], action="add")
        else:
            response_msg = "Team already in the list."
    elif data_text[COMMAND_INDEX] == "remove-team":
        # set the response message according to channel access
        # and team is already created
        if data_text[TEXT_INDEX] in settings.team_names:
            response_msg = settings.setTeam(data["channel_name"], data_text[TEXT_INDEX], action="remove")
        else:
            response_msg = "Team not in the list."
    elif data_text[COMMAND_INDEX] == "file-name" and (data_text is not ""):
        # set the response message according to file_name availability
        response_msg = settings.setFileName(data_text[TEXT_INDEX])
    elif data_text[COMMAND_INDEX] == "help" and len(data_text) == 1:
        # Displays the plain text explanation of the commands available
        attachments = settings.getHelpText()

    return jsonify({
        "response_type": "in_channel",
        "text": response_msg,
        "attachments": attachments
    })