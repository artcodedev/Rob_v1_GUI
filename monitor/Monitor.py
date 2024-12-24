

sys.path.insert(1, '../')
from  Print import Print
import requests
import zipfile
import io
import sys
import time
from pathlib import Path

class Manitor:
    
    def __init__(self, sleep, ip) -> None:
        self.ip = ip
        self.sleep = sleep
    
    
    def start(self):
        
        try:
            while True:
                
                try:
                    url = f'{self.ip}/api/v1/dw'
                    url = url if 'http' in url else f'http://{url}'
                    
                    path = requests.get(url)
                    
                    if path.status_code == 200:
                        
                        if len(path.text) != 0:
                            
                            file_name = path.text.split("/")[-1].split(".")[0]
                            
                            path_file = Path(file_name)
                            
                            if not path_file.exists():
                                
                                Print.log("[+] File not exists \nDownload...")
                                
                                url = f'{self.ip}/{path.text}'
                                url = url if 'http' in url else f'http://{url}'
                                r = requests.get(url)
                                z = zipfile.ZipFile(io.BytesIO(r.content))
                                z.extractall()
                                
                                r = None
                                z = None
                                
                            else: Print.log(f"File {file_name} is exists")
                        
                        else: Print.log("[+] Respons in None")
                    
                    else: Print.error('[+] Response is not valide')
                    
                    path = None
    
                except Exception as e:
                    Print.error('[+] Error in while')
                    Print.error(e)
            
                Print.log("Sleeep Z z zZ zzzZZ")
                time.sleep(self.sleep)
                    
        except Exception as e:
            Print.error('[+] Error in start ')
            Print.error(e)


if __name__ == "__main__":
    
    try:
        
        args = sys.argv
        
        if len(args) < 2: Print.error("[+] Args is None")
            
        else: Manitor(args[1], args[2]).start() if args[1] != None else Print.error("[+]")
        
    except Exception as e:
        Print.error("[+] Error in method main")
        Print.error(e)