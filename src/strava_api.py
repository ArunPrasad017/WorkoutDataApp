import json
import requests


class StravaApi:
    def __init__(self, session=None):
        self.session = session
        # Can we add the dict to class
        # self.token_dict = token_dict

    @property
    def session(self):
        print("Getting value")
        return self.__session

    @session.setter
    def session(self, value):
        print("Setting value")
        self.__session = value

    def set_athlete_id(self, id):
        self.session["athlete_id"] = id

    def get_athlete_id(self):
        return self.session["athlete_id"]

    def __get_auth_token(self, params):
        response = requests.post("https://www.strava.com/oauth/token", params=params)
        return json.loads(response.content)

    def get_access_refresh_token(self, params):
        auth_token = self.__get_auth_token(params)
        self.set_athlete_id(auth_token["athlete"]["id"])
        return [auth_token["access_token"], auth_token["refresh_token"]]
