
import hashlib
import sys
sys.path.insert(1, '../')
from Print import Print
import os
from pathlib import Path
import random
import json
import time

class Cookis:
    
    dir = 'cookies'
    
    
    @staticmethod
    def ch_path():
        
        try:
        
            Print.log("[+] Check cookie file")
            
            path_cookies = Path(Cookis.dir)
            
            if not path_cookies.exists(): os.mkdir(path_cookies)
            
            return True if path_cookies.exists() else False
        
        except Exception as e:
            Print.error('[+] Error in ch_path method')
            Print.error(e)
            return False
    
          
    @staticmethod
    def setCookie(cookie, ch, host):
        
        try:
            
            Print.log('[+] Get cookie ')
            
            if Cookis.ch_path():
            
                sc_time = (int(time.time()) * 1000) * random.randint(1000, 999999999999)
            
                n = hashlib.sha256(str(sc_time).encode()).hexdigest()
                
                name_f_co = f'{Cookis.dir}/{n}_{ch}_{host}.json'
            
                Print.log(f"[+] Save cookie: {name_f_co}")
                        
                with open(name_f_co, "w+") as f:
                    f.write(json.dumps(cookie))
            
        except Exception as e:
            Print.error("[+] Error in setCookie")
            Print.error(e)
    
    
    @staticmethod
    def getCookie(ch, host):
        try:
            
            if Cookis.ch_path():
                
               list_cookies = os.listdir(Cookis.dir)
               
               if len(list_cookies) > 1:
                   
                    m_co = []
                            
                    for i in list_cookies:
                        if i.find(ch) != -1 and i.find(host) != -1: m_co.append(i)
                    
                    if len(m_co) != 0:
                        cookies = list_cookies[random.randint(0, len(m_co) - 1)]
                        with open(f'cookies/{cookies}', "r") as f: return json.loads(f.read())
            
            return False
        
        except Exception as e:
            Print.error('[+] Error in getCookie method')
            Print.error(e)
            return False
