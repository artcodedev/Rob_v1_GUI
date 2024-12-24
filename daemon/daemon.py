import sys
sys.path.insert(1, '../')
from  Print import Print
# from Print import Print
import json
import math
from timezone import Time
import random
import time

class Daemon:
    
    def __init__(self) -> None: pass
    
    
    def __change_conf(self):
        
        try:
            with open("../configs/config.json", 'r', encoding="utf-8") as j:
                
                json_decoded = json.load(j)
                
                hour = Time().getTimeZone('Europe/Moscow')
                
                Print.log(f"[+] Hour: {hour}")
                
                time_limit = json_decoded['time_limit'][f'{hour}']
                
                file = json_decoded['robot_config']
                
                with open(file, 'r', encoding="utf-8") as f:
                    
                    jf = json.load(f)
                    
                    keys = jf.keys()
                    
                    keys_mass = []
                    
                    for i in keys: keys_mass.append(i)
                
                    pr = math.ceil((int(len(keys)) / 100) * int(time_limit))
                    
                    Print.log(f"[+] Limit walk {pr}")
                    
                    for i1 in keys: jf[i1]['in_work'] = False
                    
                    for i in range(0, int(pr)): jf[keys_mass[i]]['in_work'] = True
                    
                    with open(file, 'w', encoding='utf-8') as js: json.dump(jf, js, ensure_ascii=False)
                    
                    Print.ok("[+] __change_conf Done.")
                    
            
        except Exception as e:
            Print.error("[+] Error in method __change_conf")
            Print.error(e)
    
    
    def __change_time_walk(self):
        try:
            with open("../configs/config.json", 'r', encoding="utf-8") as j:
                
                json_decoded = json.load(j)
                
                file = json_decoded['robot_config']
                
                time = json_decoded['time_walk']
                
                with open(file, 'r', encoding="utf-8") as f:
                    
                    jf = json.load(f)
                    
                    keys = jf.keys()
                    
                    keys_mass = []
                    
                    for i in keys: keys_mass.append(i)
                    
                    for i1 in keys:
                        
                        min = random.randint(time['min'][0], time['min'][1])
                        max = random.randint(time['max'][0], time['max'][1])
                        
                        jf[i1]['url']['time'] = [min, max]
                        
                    with open(file, 'w', encoding='utf-8') as js: json.dump(jf, js, ensure_ascii=False)
                    
                    Print.ok("[+] __change_time_walk Done.")
                    
            
        except Exception as e:
            Print.error("[+] Error in method __change_time_walk")
            Print.error(e)
    
    
    def __change_type(self):  self.__change_func(True)
    
    
    def __experience(self): self.__change_func(False)
    
    
    def __change_func(self, type):
        
        try:
            with open("../configs/config.json", 'r', encoding="utf-8") as j:
                
                json_decoded = json.load(j)
                
                file = json_decoded['robot_config']
                
                with open(file, 'r', encoding="utf-8") as f:
                    
                    jf = json.load(f)
                    
                    keys = jf.keys()
                    
                    keys_mass = []
                    
                    for i in keys: keys_mass.append(i)
                    
                    for i1 in keys:
                        
                        if type: jf[i1]['type'] = ["slow", "normal", "fest"][random.randint(0,2)]
                        
                        else: jf[i1]['experience'] = ["newbie", "experienced", "old_man"][random.randint(0,2)]

                    with open(file, 'w', encoding='utf-8') as js: json.dump(jf, js, ensure_ascii=False)
                    
                    Print.ok("[+] __change_func Done.")
                    
            
        except Exception as e:
            Print.error('[+] Error in method __change_func')
            Print.error(e)
        
        
    def run(self):
        try:
            Print.log("[+] Start Daemon")
            
            while True:
                Print.log(f'[+] Сhange file')
                
                self.__change_conf()
                
                self.__change_time_walk()
                
                self.__change_type()
                
                self.__experience()
                
                # sleep 30 min
                time.sleep(600)
                
        except Exception as e:
            Print.error("[+] Error in method run")
            Print.error(e)
        

if __name__ == '__main__': Daemon().run()
