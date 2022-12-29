import requests
import json


class Authenticat(object):
    def __init__(self, url_token="http://localhost:8000/token"):
        self.token_access = None
        self.token_refresh = None
        self.url_token = url_token
        

    def do_auth(self):
        valores = {
            "username":"cliente",
            "password":"#You*Front$Diary"
        }

        try:
            requisicao = requests.post(self.url_token, data=valores)
        except:
            return None

        dic_content = requisicao.json()
        if requisicao.status_code == 200:
            self.token_access = dic_content["access"]
            self.token_refresh = dic_content["refresh"]
        elif requisicao.status_code == 401:
            return False

        return True


        # return token acess if auth is true

    def do_refresh(self, refresh, url_refresh="http://localhost:8000/token/refresh"):
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


    def get_token(self):
        return self.token_access


    def get_token_refresh(self):
        return self.token_refresh


class AccessDB(object):

    # tag é só enfeitar e para fácil visualização
    def __init__(self, name_url:str, url:str="http://localhost:8000/", tag:str="None"):
        self.token_access = None
        self.token_refresh = None
        self.name_url = name_url
        self.url = url

    def get(self, id_object=None, page=None):
        auth = Authenticat()
        resposta = auth.do_auth()


        if resposta == True:
            self.token_access = auth.get_token()
            self.token_refresh = auth.get_token_refresh()
            head = {'Authorization': 'Bearer {}'.format(self.token_access)}

            
            if page != None:
                try:
                    request = requests.get(self.url+self.name_url+"?page={}".format(page), headers=head)
                except:
                    return "Error ao Fazer Requisição ao Servidor"                
            
            else:
                if id_object == None:
                    try:
                        request = requests.get(self.url+self.name_url, headers=head)
                    except:
                        return "Error ao Fazer Requisição ao Servidor"
                
                else:
                    try:
                        request = requests.get(self.url+self.name_url+"{}".format(id_object), headers=head)
                    except:
                        return "Error ao Fazer Requisição ao Servidor"



            if request.status_code == 200:
                return request.json()
            elif request.status_code == 401:
                return "Sem Autorização"
            else:
                return "Erro Inesperado"
        elif resposta == False:
            return "Credencias Inválidas"
        else:
            return "Problemas em contatar o servidor!"


    def delete(self, id_object=None):
        auth = Authenticat()
        resposta = auth.do_auth()


        if resposta == True:
            self.token_access = auth.get_token()
            self.token_refresh = auth.get_token_refresh()
            head = {'Authorization': 'Bearer {}'.format(self.token_access)}

            try:
                request = requests.delete(self.url+self.name_url+"/{}".format(id_object), headers=head)
            except:
                return "Error ao Fazer Requisição ao Servidor"

            if request.status_code == 200:
                return request.json()
            elif request.status_code == 401:
                return "Sem Autorização"
            else:
                return "Erro Inesperado"

        
        elif resposta == False:
            return "Credencias Inválidas"

        else:
            return "Problemas em contatar o servidor!"


    def post(self, data, files=None, *args, **kwargs):
        auth = Authenticat()
        resposta = auth.do_auth()

        self.token_access = auth.get_token()
        self.token_refresh = auth.get_token_refresh()


        head = {'Authorization': 'Bearer {}'.format(self.token_access)}


        if files != None:
            try:
                requisicao = requests.post(self.url+self.name_url, data=data, files=files,
                                            headers=head)
            except:
                return "Error ao Fazer Requisição ao Servidor"
        else:
            try:
                requisicao = requests.post(self.url+self.name_url, data=data, headers=head)
            except:
                return "Error ao Fazer Requisição ao Servidor"

        # print(requisicao.text)
        # codigo 201 é para create
        if requisicao.status_code == 201:
            return True
        elif requisicao.status_code == 200:
            return requisicao.json()
        elif requisicao.status_code == 401:
            return "Sem Autorização"
        elif requisicao.status_code == 400:
            return "Falta ou Dado Já Repetido Por Outros"
        else:
            return "Erro Inesperado"


        # print(requisicao.content)
        return False

    def put(self, data, id_object, files=None, *args, **kwargs):
        auth = Authenticat()
        resposta = auth.do_auth()

        self.token_access = auth.get_token()
        self.token_refresh = auth.get_token_refresh()


        head = {'Authorization': 'Bearer {}'.format(self.token_access)}


        if files != None:
            try:
                requisicao = requests.put(self.url+self.name_url+"/{}".format(id_object)+"/", data=data, files=files,
                                            headers=head)
            except:
                return "Error ao Fazer Requisição ao Servidor"
        else:
            try:
                requisicao = requests.put(self.url+self.name_url+"/{}".format(id_object)+"/", data=data, headers=head)
            except:
                return "Error ao Fazer Requisição ao Servidor"


        # codigo 201 é para create
        if requisicao.status_code == 201:
            return True
        elif requisicao.status_code == 200:
            return requisicao.json()
        elif requisicao.status_code == 401:
            return "Sem Autorização"
        else:
            return "Erro Inesperado"


        # print(requisicao.content)
        return False

    
    # annotations/by/author/<int:pk> or annotations/by/author/<int:pk>?page=nº => nesse formato para usar os filtros
    def filter_by_id(self, id_object=None, page=None):
        auth = Authenticat()
        resposta = auth.do_auth()


        if resposta == True:
            self.token_access = auth.get_token()
            self.token_refresh = auth.get_token_refresh()
            head = {'Authorization': 'Bearer {}'.format(self.token_access)}

            
            if page != None:
                try:
                    request = requests.get(self.url+self.name_url+"/"+str(id_object)+"?page={}".format(page), headers=head)
                except:
                    return "Error ao Fazer Requisição ao Servidor"                
                    
            else:
                if id_object == None:
                    try:
                        request = requests.get(self.url+self.name_url, headers=head)
                    except:
                        return "Error ao Fazer Requisição ao Servidor"
                
                else:
                    try:
                        request = requests.get(self.url+self.name_url+"/{}".format(id_object), headers=head)
                    except:
                        return "Error ao Fazer Requisição ao Servidor"




            if request.status_code == 200:
                return request.json()
            elif request.status_code == 401:
                return "Sem Autorização"
            else:
                return "Erro Inesperado"
        elif resposta == False:
            return "Credencias Inválidas"
        else:
            return "Problemas em contatar o servidor!"