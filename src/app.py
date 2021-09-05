import os
from flask import Flask
import requests

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get('strava_access_key')
URL = 'https://www.strava.com/api/v3/athlete'

@app.route("/")
def app_main():
    return "Flask app init"

def return_resp():
    headers_auth = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    print(headers_auth)
    response = requests.get(URL,headers=headers_auth)
    return response.content