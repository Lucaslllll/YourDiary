import requests
import json
from components.crypto import USERNAME, PASSWORD



class Authenticat(object):
    def __init__(self, url_token="http://api.yourdiary.top/token"):
        self.token_access = None
        self.token_refresh = None
        self.url_token = url_token
        self.resposta = None
        

    def do_auth(self):
        valores = {
            "username":USERNAME,
            "password":PASSWORD
        }
        


        try:
            requisicao = requests.post(self.url_token, data=valores)
        except:
            return None

        
        if requisicao.status_code == 200:
            dic_content = requisicao.json()
            self.token_access = dic_content["access"]
            self.token_refresh = dic_content["refresh"]
        elif requisicao.status_code == 401:
            return False

        return True


        # return token acess if auth is true

    def do_refresh(self, refresh, url_refresh="http://api.yourdiary.top/token/refresh"):
        valores = {
            "refresh":self.token_refresh,
        }
        

        try:
            requisicao = requests.post(url_refresh, data=valores)
        except:
            return None

        dic_content = requisicao.json()
        self.token_access = dic_content["access"]

        return self.token_access
        # return token if send refresh token


    def get_resposta(self):
        return self.resposta

    def get_token(self):
        return self.token_access


    def get_token_refresh(self):
        return self.token_refresh