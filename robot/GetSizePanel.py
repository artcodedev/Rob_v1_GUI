
from playwright.sync_api import sync_playwright, Playwright
import time
from Actions import Actions
import os
import sys
sys.path.insert(1, '../')
from Print import Print
import json

class GetSizePanel:
    
    # def __init__(self, ch, file) -> None:
    #     self.ch = ch
    #     self.file = file
    
    
    def getSizePanel(self, ch, file):
        try:
            with sync_playwright() as playwright:
                
                actions = Actions()
                
                actions.moveTo(1, 1, .1)

                browser = playwright.chromium.launch(args=['--start-maximized'], headless=False, channel=ch)
                
                context = browser.new_context(no_viewport=True)
                page = context.new_page()
                page.goto(f'file://{os.path.abspath(file)}')   
                page.wait_for_load_state("load")
                time.sleep(1)
                size_panel = actions.locateOnScreen('find_me.webp')
                Print.log(f"[+] Size panel: {size_panel.top}")
                time.sleep(1)
                browser.close()
                
                return size_panel.top
            
        except Exception as e:
            Print.error("[+] Error in SIZE PANEL")
            Print.error(e)
            return False
    
    
    def getTop(self, ch):
        try:
            
            Print.log("[+] Get Top")
            
            path = 'top_conf.json'
            
            if os.path.exists(path):
                
                Print.log(f'[+] File {path} exists')
                
                with open(path, 'r') as f:
                    file = f.read()
                    Print.warning(f"[+] File len {len(file)}")
                    path = { "chrome": 0, "msedge": 0 } if len(file) == 0 else json.loads(file)
                    
            else:
                
                Print.log(f'[+] File {path} not exists')
                
                data = { "chrome": 0, "msedge": 0 }
                
                data['chrome'] = int(self.getSizePanel("chrome", "find_me.html"))
                # data['msedge'] = int(self.getSizePanel("msedge", "find_me.html"))
                
                Print.log(f'[+] Save file {path}')
                with open(path, 'w+') as f: f.write(json.dumps(data))
                
                path = data

            if ch == 'chrome': return path['chrome']
            # if ch == 'msedge': return path['msedge']
            
            
        except Exception as e:
            Print.error("[+] Error in getTop method")
            Print.error(e)
            return False
    