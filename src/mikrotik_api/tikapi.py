import urllib3
import json

class Connector:

    def __init__(self,ipaddress:str,username:str,password:str,https:bool=True):
        self.ipaddress = ipaddress
        self.username = username
        self.password = password
        self.auth = urllib3.make_headers(basic_auth=f"{self.username}:{self.password}")
        mode = "https" if https else "http"
        self.url = f"{mode}://{ipaddress}/rest/"
        self.http = urllib3.PoolManager()

    def __return(self,response:urllib3.HTTPResponse) -> dict:
        result = {"HTTP":response.status,"Headers":dict(response.headers),"Content":response.json()}
        return result

    def get(self,command:str):
        return self.__return(self.http.request("GET",f"{self.url}{command}",headers=self.auth))
    
    def search(self,command:str,queries:list=[],returns:list=[]):
        data = {}
        if len(queries) > 0:
            data[".query"] = queries
        if len(returns) > 0:
            data[".proplist"] = returns
        return self.__return(self.http.request("POST",f"{self.url}{command}/print",body=json.dumps(data),headers=self.auth))

    def set(self,command:str,id:str,data:dict):
        return self.__return(self.http.request("PATCH",f"{self.url}{command}/{id}",body=json.dumps(data),headers=self.auth))
    
    def add(self,command:str,data:dict):
        return self.__return(self.http.request("PUT",f"{self.url}{command}",body=json.dumps(data),headers=self.auth))
    
    def remove(self,command:str,id:str):
        return self.__return(self.http.request("DELETE",f"{self.url}{command}/{id}",headers=self.auth))
    
    def exec(self,command:str,data:dict):
        return self.__return(self.http.request("POST",f"{self.url}{command}",body=json.dumps(data),headers=self.auth))