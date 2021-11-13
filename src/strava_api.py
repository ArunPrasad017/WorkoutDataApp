
class StravaApi():
    def __init__(self, session) -> None:
        self.session = session

    def get_athlete_id(self):
        return self.session["athlete_id"]

    def set_session(self, session):
        self.session = session
