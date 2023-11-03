import urllib3
import json

class Connector:
    '''
    Class for handling a single API connection
    :param ipaddress: IP address to connect to
    :type ipaddress: str
    :param username: Account username for API access
    :type username: str
    :param password: Account password
    :type password: str
    :param https: Connect via https, defaults to True
    :type https: bool, optional
    '''

    def __init__(self,ipaddress:str,username:str,password:str,https:bool=True):
        '''Constructor'''
        self.ipaddress = ipaddress
        self.username = username
        self.password = password
        self.__auth = urllib3.make_headers(basic_auth=f"{self.username}:{self.password}")
        mode = "https" if https else "http"
        self.__url = f"{mode}://{ipaddress}/rest/"
        self.__http = urllib3.PoolManager()

    def __process(self,response:urllib3.HTTPResponse) -> dict:
        '''Processes request responses
        :return: HTTP status code, headers and content of the response
        :rtype: dict'''
        result = {"Status":response.status,"Headers":dict(response.headers),"Content":response.json()}
        return result

    def get(self,command:str):
        '''Queries all entries for the supplied command as if \"print\" was used in the terminal
        :param command: the terminal command in routerOS eg. interface/vlan
        :type command: str
        :return: data processed by __process(response)
        :rtype: dict'''
        return self.__process(self.__http.request("GET",f"{self.__url}{command}",headers=self.__auth))
    
    def search(self,command:str,queries:list=[],returns:list=[]):
        '''Queries all entries for the supplied command as if \"print\" was used in the terminal.
        If queries are supplied only matching data will be returned. If returns are supplied only
        the requested parameters will be returned
        :param command: the terminal command in routerOS eg. interface/vlan
        :type command: str
        :param queries: strings to search for eg. "vlan-id=5"
        :type queries: list, optional
        :param returns: key names to be returned by the search eg. ["name","vlan-id"], returns all if no values supplied
        :type returns: list, optional
        :return: data processed by __process(response)
        :rtype: dict'''
        data = {}
        if len(queries) > 0:
            data[".query"] = queries
        if len(returns) > 0:
            data[".proplist"] = returns
        return self.__process(self.__http.request("POST",f"{self.__url}{command}/print",body=json.dumps(data),headers=self.__auth))

    def set(self,command:str,id:str,data:dict):
        return self.__process(self.__http.request("PATCH",f"{self.__url}{command}/{id}",body=json.dumps(data),headers=self.__auth))
    
    def add(self,command:str,data:dict):
        return self.__process(self.__http.request("PUT",f"{self.__url}{command}",body=json.dumps(data),headers=self.__auth))
    
    def remove(self,command:str,id:str):
        return self.__process(self.__http.request("DELETE",f"{self.__url}{command}/{id}",headers=self.__auth))
    
    def exec(self,command:str,data:dict):
        return self.__process(self.__http.request("POST",f"{self.__url}{command}",body=json.dumps(data),headers=self.__auth))