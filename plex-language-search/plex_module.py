from plexapi.server import PlexServer
import requests
import urllib3
from confighandler import read_config


class PlexService:
    def __init__(self):
        self.config = read_config("plex")
        self.server_url = self.config.get("url")
        self.server_token = self.config.get("api_key")
        self.replace = self.config.get("replace")

    def connect_plex(self):
        session = requests.Session()
        session.verify = False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        return PlexServer(self.server_url, self.server_token, session=session)
