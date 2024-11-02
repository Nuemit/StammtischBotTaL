import requests

class Joking:
    def __init__(self) -> None:
        self.URL = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=political,racist,explicit&format=txt&type=single"
        self.responsetext = ""
        self.response = ""

    def getJoke(self) -> str:
        return self.responsetext
    
    def newJoke(self) -> None:
        self.response = requests.get(self.URL)
        self.responsetext = self.response.text
        
