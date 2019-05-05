import os
from scripts.sheets import addGSheetsRow
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

    team_names = ["3lb", "30lb", "Pacbot", "URC"]


    if not is_request_valid(request):
        abort(400)

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

    if t_name not in team_names:
        return jsonify({
            "response_type" : "in_channel",
            "text": "Team name has to be one of {}.".format(", ".join(t for t in team_names)),
        })

    # add the data in the spreadsheet
    addGSheetsRow(data)

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
