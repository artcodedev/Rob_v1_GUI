
from flask import Flask, render_template
import sys

sys.path.insert(1, '../')
from Print import Print

from Proxy import Proxy

import os
import json
import random
from pathlib import Path



class Server:
    
    def __init__(self, config, ip, port, debug=True) -> None:
        self.ip = ip
        self.port = port
        self.debug = debug
        self.config = config
        
        self.app = Flask(__name__)
    
    
    # add endpoint
    def add_endpoint(self, endpoint, endpoint_name, handler, req_methods):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=req_methods)
        
    
    # add new value in robots config
    def addInJson(self, key, value):
        
        try:
            json_file = self.config['robot_config']
            
            with open(json_file, 'r', encoding="utf-8") as j:
                json_decoded = json.load(j)
            
            json_decoded[key] = value
            
            with open(json_file, 'w', encoding='utf-8') as j:
                json.dump(json_decoded,j, ensure_ascii=False)
            
            return True
        
        except:
            Print.error("[+] error in attempt to read or add record")
            return False
    
    
    # index page
    def index(self):
        return render_template('index.html')
    
    
    def response(self, status, data):
        return json.dumps({"status": status, "data": data})
    
    
    # registartion robot id in db 
    def registration_id(self, id):
        
        Print.log("[+] request add id robot in db")
    
        try:
            
            with open(self.config['robot_config'], 'r', encoding="utf-8") as j:
            
                ch_id = json.load(j)
                
                if str(id) in ch_id:
                    
                    Print.log(f"[+] key {id} was found in db")
                    return self.response(True, "key was found in db")
                
                main_url = self.config['main_url']
                
                visits = []
                
                default_url = self.config['default_url']
                
                for i in default_url:
                    visits.append({
                        "url": default_url[random.randint(0, len(default_url) -1)],
                        "time": [
                            random.randint(100,150),
                            random.randint(200,250)
                        ]
                    })
                
                data = {
                    "in_work": True,
                    "sleep": 60,
                    "move":  ["slow", "normal", "fest"][random.randint(0,2)],
                    "experience": ["newbie", "experienced", "old_man"][random.randint(0,2)],
                    "cookie": True,
                    "visits": visits,
                    "auth": [True, False][random.randint(0, 1)],
                    "url": {
                        "url": self.config['main_url'][random.randint(0, len(main_url) -1)],
                        "time": [
                            int(self.config['time_walk']['min'][0]),
                            int(self.config['time_walk']['max'][1])
                        ]
                    }
                }
                
                ad_c = self.addInJson(f'{id}', data)
                
                if ad_c:
                    Print.log(f"[+] key {id} add in db")
                    return self.response(True, "key add in db")
                else:
                    Print.error(f"[+] key {id} not add in db")
                    return self.response(False, "key not add in db")
                
                
        except Exception as e:
            Print.error(e)
            return self.response(False, "Error! key not add in db")
        
        
    # get behavior for robot
    def behavior(self, id):
        
        Print.log(f"[+] Request get behavior for id: {id}")
        
        try:
            with open(self.config['robot_config'], 'r', encoding="utf-8") as j:
            
                ch_id = json.load(j)
                
                if str(id) not in ch_id:
                    res_txt = f" key {id} not found in db"
                    
                    return self.response(False, res_txt)
                
                if str(id) in ch_id:
                    Print.log(f"[+] Response config for id {id}")
                    
                    ch_id[f'{id}']['movement'] = {
                        "move":  self.config['move'][ch_id[f'{id}']['move']],
                        "experience": self.config['experience'][f'{ch_id[f'{id}']['experience']}']
                    }
                    
                    auth_data = []
                    
                    if ch_id[f'{id}']['auth']:
                        
                        with open('../configs/auth.json', 'r', encoding="utf-8") as ja:
                            data = json.load(ja)
                            
                            auth_data = data['data'][random.randint(0, len(data['data']) - 1)]
                    
                    ch_id[f'{id}']['auth_data'] = auth_data
                    
                    return self.response(True, ch_id[f'{id}'])
                
            Print.error("[+] Error in behavior method")
            return self.response(False, [])
                
        except Exception as e:
            Print.error(e)
            return self.response(False, "Error! Get behavior for id")
       
    
    # get proxy
    def getProxy(self):
        
        proxy = Proxy.getproxy()
        
        return self.response(True, proxy) if proxy else self.response(False, [])
    
    
    def getconfvisitorurl(self, url):
        
        try:
            
            with open(f'./static/configs/{url}.json', 'r', encoding="utf-8") as j:    
                
                # return json.load(j)
                return self.response(True, json.load(j))
            
        except Exception as e:
            Print.error(e)
            return self.response(False, [])
    
    
    def getutmargs(self):
        try:
            args = json.load(open('./static/args.json'))['args']
            ran = random.randint(0, len(args) - 1)
            return args[ran]
        
        except Exception as e:
            Print.error(e)
            return ''
    
    def dw(self):
        try:
            
            return json.load(open('./static/configs/dw.json'))['path']
        
        except Exception as e:
            Print.error("[+] Error in DW")
            Print.error(e)
            
    # start server
    def run(self):
        
        self.add_endpoint('/', 'index', self.index, ['GET'])
        
        # ======== API ========
        # =====================
        
        self.add_endpoint('/api/v1/getproxy', 'getProxy', self.getProxy, ['GET'])
        
        self.add_endpoint('/api/v1/registration_id/<int:id>', 'registration_id', self.registration_id, ['GET'])
        
        self.add_endpoint('/api/v1/behavior/<int:id>', 'behavior', self.behavior, ['GET'])
        
        self.add_endpoint('/api/v1/getconfvisitorurl/<url>', 'getconfvisitorurl', self.getconfvisitorurl, ['GET'])
        
        self.add_endpoint('/api/v1/getutmargs', 'getutmargs', self.getutmargs, ['GET'])
        
        self.add_endpoint('/api/v1/dw', 'dw', self.dw, ['GET'])
        
        
        # ======= run serve =======
        self.app.run(host=self.ip, port=self.port, debug=True)
    

if __name__ == '__main__':

    try:
        
        with open('../configs/config.json', 'r', encoding="utf-8") as j:
            
                config = json.load(j)
                
                robot_config = config["robot_config"]
                
                if not os.path.exists(robot_config):
                    with open(robot_config, 'w') as file:
                        file.write("{}")
                
                Print.log("[+] Starting server...")
                Server(config=config, ip=config['ip'], port=config['port']).run()
        
    except Exception as e:
        Print.error(e)