import os
from flask import abort, Flask, jsonify, request

app = Flask(__name__)

def is_request_valid(request):
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    is_team_id_valid = request.form['team_id'] == os.environ['SLACK_TEAM_ID']

    return is_token_valid and is_team_id_valid

@app.route('/purchase-item', methods=['POST'])
def purchase():

    LIST_INDEX_TEXT = 8
    if not is_request_valid(request):
        abort(400)

    data = list(request.form.values())[LIST_INDEX_TEXT]

    print(data[LIST_INDEX])

    

    return "success"
