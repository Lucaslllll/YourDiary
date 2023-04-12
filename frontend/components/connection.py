import json
from components.authentication import Authenticat
from kaki.app import App
from kivy.storage.jsonstore import JsonStore

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class AccessDB(object):

    # tag é só enfeitar e para fácil visualização
    def __init__(self, name_url:str, url:str="http://localhost:8000/", tag:str="None"):
        self.name_url = name_url
        self.url = url
        self.path = App.get_running_app().user_data_dir+"/"
        
        store = JsonStore(self.path+"data.json")
        if store.exists('authentication'):    
            self.resposta = store.get("authentication")["resposta"]
            self.token_access = store.get("authentication")["token_access"]
            self.token_refresh = store.get("authentication")["token_refresh"]
        else:
            self.resposta = False
            self.token_access = None
            self.token_refresh = None


    def get(self, id_object=None, page=None):
        if self.resposta == True:
            head = {'Authorization': 'Bearer {}'.format(self.token_access)}

            
            if page != None:
                try:
                    request = requests.get(self.url+self.name_url+"?page={}".format(page), headers=head, verify=False)
                except:
                    return "Error ao Fazer Requisição ao Servidor"                
            
            else:
                if id_object == None:
                    try:
                        request = requests.get(self.url+self.name_url, headers=head, verify=False)
                    except:
                        return "Error ao Fazer Requisição ao Servidor"
                
                else:
                    try:
                        request = requests.get(self.url+self.name_url+"/{}".format(id_object), headers=head, verify=False)
                    except:
                        return "Error ao Fazer Requisição ao Servidor"



            if request.status_code == 200:
                return request.json()
            elif request.status_code == 401:
                return "Sem Autorização"
            else:
                return "Erro Inesperado"
        elif self.resposta == False:
            return "Credencias Inválidas"
        else:
            return "Problemas em contatar o servidor!"


    def delete(self, id_object=None):
        
        if self.resposta == True:
            head = {'Authorization': 'Bearer {}'.format(self.token_access)}

            try:
                request = requests.delete(self.url+self.name_url+"/{}".format(id_object), headers=head, verify=False)
            except:
                return "Error ao Fazer Requisição ao Servidor"

            if request.status_code == 204:
                return {}
            elif request.status_code == 200:
                return {}
            elif request.status_code == 401:
                return "Sem Autorização"
            else:
                return "Erro Inesperado"

        
        elif self.resposta == False:
            return "Credencias Inválidas"

        else:
            return "Problemas em contatar o servidor!"


    def post(self, data, files=None, *args, **kwargs):
        head = {'Authorization': 'Bearer {}'.format(self.token_access)}

        
        if files != None:
            try:
                requisicao = requests.post(self.url+self.name_url, data=data, files=files,
                                            headers=head, verify=False)
            except:
                return "Error ao Fazer Requisição ao Servidor"
        else:
            try:
                requisicao = requests.post(self.url+self.name_url, data=data, headers=head, verify=False)
            except:
                return "Error ao Fazer Requisição ao Servidor"

        # print((requisicao.text, requisicao.json))
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
        head = {'Authorization': 'Bearer {}'.format(self.token_access)}


        if files != None:
            try:
                requisicao = requests.put(self.url+self.name_url+"/{}".format(id_object)+"/", data=data, files=files,
                                            headers=head, verify=False)
            except:
                return "Error ao Fazer Requisição ao Servidor"
        else:
            try:
                requisicao = requests.put(self.url+self.name_url+"/{}".format(id_object)+"/", data=data, headers=head, verify=False)
            except:
                return "Error ao Fazer Requisição ao Servidor"



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

    def patch(self, data, id_object, files=None, *args, **kwargs):
        head = {'Authorization': 'Bearer {}'.format(self.token_access)}


        if files != None:
            try:
                requisicao = requests.patch(self.url+self.name_url+"/{}".format(id_object)+"/", data=data, files=files,
                                            headers=head, verify=False)
            except:
                return "Error ao Fazer Requisição ao Servidor"
        else:
            try:
                requisicao = requests.patch(self.url+self.name_url+"/{}".format(id_object)+"/", data=data, headers=head, verify=False)
            except:
                return "Error ao Fazer Requisição ao Servidor"



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
        if self.resposta == True:
            head = {'Authorization': 'Bearer {}'.format(self.token_access)}

            
            if page != None:
                try:
                    request = requests.get(self.url+self.name_url+"/"+str(id_object)+"?page={}".format(page), headers=head, verify=False)
                except:
                    return "Error ao Fazer Requisição ao Servidor"                
                    
            else:
                if id_object == None:
                    try:
                        request = requests.get(self.url+self.name_url, headers=head, verify=False)
                    except:
                        return "Error ao Fazer Requisição ao Servidor"
                
                else:
                    try:
                        request = requests.get(self.url+self.name_url+"/{}".format(id_object), headers=head, verify=False)
                    except:
                        return "Error ao Fazer Requisição ao Servidor"




            if request.status_code == 200:
                return request.json()
            elif request.status_code == 401:
                return "Sem Autorização"
            else:
                return "Erro Inesperado"
        elif self.resposta == False:
            return "Credencias Inválidas"
        else:
            return "Problemas em contatar o servidor!"