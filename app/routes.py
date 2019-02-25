from app import app
import requests
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return "Hello friends! :)"


shared_var = None
req_counter = 0

bearer_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1ODI3NzAwNTEs" \
               "ImlkIjoid2VpamluX3RhbkBteW1haWwuc3V0ZC5lZHUuc2ciLCJvcmlnX2lhdCI6MTU1" \
               "MDYyOTI1MX0.jQb5CD8vRw7rU5StmJEE9q0-pwMQStTJ8vl8ZE6pgvI"


@app.route('/api', methods=['GET'])
def apicall():
    url = 'https://ug-api.acnapiv3.io/swivel/language-identification/lang-2.0?'
    text = 'Hi my name is'
    url = "https://ug-api.acnapiv3.io/swivel/language-identification/lang-2.0?of=json&txt=hello what is up"
    data = {"txt": 'Hi my name is'}

    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1ODI3NzAwNTEs"
                                + "ImlkIjoid2VpamluX3RhbkBteW1haWwuc3V0ZC5lZHUuc2ciLCJvcmlnX2lhdCI6MTU1"
                                + "MDYyOTI1MX0.jQb5CD8vRw7rU5StmJEE9q0-pwMQStTJ8vl8ZE6pgvI"}
    response = requests.get(url, headers=headers)
    value = response.text

    return render_template("apicall.html", value=value)


