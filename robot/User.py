
import sys
sys.path.insert(1, '../')

from robot.Actions import Actions
import time
import os
import json
import random
import requests
from Cookie import Cookis
from Print import Print
from Study import Study
from Auth import Auth
from Scroll import Scroll
from Move import Move
from Link import Link
from Some_DO import Some_DO
from Sleep import Sleep
from GetSizePanel import GetSizePanel
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync



class User:
    
    def __init__(self, url, move, experience, auth, movement, proxy, auth_data, conf, base_url, utm=False, cookie=False) -> None:
        self.url = url
        self.move = move
        self.experience = experience
        self.auth = auth
        self.movement = movement
        self.proxy = proxy
        self.error = 0
        self.conf = conf
        self.auth_data = auth_data
        self.top = None
        self.base_url = base_url
        self.utm = utm
        self.cookie = cookie
    
    
    def walk(self) -> bool:
        
        try:
            
            Print.ok('[+] Next step')
            
            exp = self.movement['experience']
            
            range_walk = random.randint(int(exp['min']),  (exp['max']))
            
            Print.log(f'[+] Range walk {range_walk}')
            
            for i1 in range(0, range_walk):
                
                Print.log("[+] Some do step")
                Some_DO.some_do(self.page, self.actions, self.conf['some_do']['check_el'])
                
                event = ["read_text", "watch_img", "auth", "scroll", "move"]
        
                Print.log('[+] Get random behavior')
                event_el = event[random.randint(0, len(event) - 1)]
                
                Print.warning(f'[+] Type event [{event_el}]')
                
                if event_el == 'read_text': Study.study("txt", self.page, self.actions, self.top)
                
                if event_el == 'watch_img': Study.study("img", self.page, self.actions, self.top)
                
                if event_el == 'auth' and self.auth: Auth.auth(self.page, self.actions, self.auth_data)
                
                if event_el == 'scroll': Scroll.scroll(self.page, self.actions)
                
                if event_el == 'move': Move.move(self.actions)
                
            Print.log('[+] Find link for click')
            Link.link(self.page, self.actions, self.conf['close_urls'])
            
            Sleep.zZz(1000)
            Print.log('\n')

            return True
        
        except Exception as e:
            Print.error(e)
            return False
    
    
    def run(self):
        
        try:    
                        
            Print.ok("[+] User start")
            
            self.ch = ['msedge', 'chrome'][random.randint(0, 1)]
            
            self.ch = "chrome"
            
            Print.log(f"[+] Type browser {self.ch}")
            
            Print.log("[+] Create url proxy")
            if len(self.proxy['login']) == 0:
                Print.error('[+] Proxy without auth')
                return False
            
            pr = self.proxy
            
            proxy = {
                "server": f"{pr['ip']}:{pr['port']}",
                "username": f"{pr['login']}",
                "password": f"{pr['pass']}"
            }
            
            Print.log('[+] Start browser')
            
            with sync_playwright() as playwright:
                
                try:
                    
                    # use without proxy
                    self.browser = playwright.chromium.launch(args=['--start-maximized'], headless=False, channel=self.ch)
                    
                    # use proxy
                    # self.browser = playwright.chromium.launch(args=['--start-maximized'], headless=False, channel=self.ch, proxy=proxy)
                
                    self.context = self.browser.new_context(no_viewport=True)

                    self.page = self.context.new_page()
                    
                    stealth_sync(self.page)
                    
                    move = self.movement['move']
                    
                    self.actions = Actions(move['mousemove'], move['scroll'], self.page)
                
                    url = self.url['url']
                
                    url_start = self.conf['start_urls'][random.randint(0, len(self.conf['start_urls']) - 1)] if len(self.conf['start_urls']) > 1 else self.conf['start_urls'][0]
                
                    _s_url = f"{url}{url_start}"
                
                    _s_url = _s_url if 'http' in _s_url else f'https://{_s_url}'
                    
                    utm = random.randint(0, 1) if self.utm else False
                    
                    Print.log(f'[+] Utm status: {utm}')
                    
                    if utm:
                        
                        try:
                            Print.log('[+] Get UTM metric')
                            utm = requests.get(f'http://{self.base_url}/api/v1/getutmargs')
                            
                            Print.log(f'[+] UTM: {utm.text}')
                            
                            url = f'{url}{utm.text}'
                        
                        except Exception as e:
                            Print.error('[+] Error in get UTM metric')
                            Print.error(e)
                    else:
                        
                        cookie = random.randint(0, 1) if self.cookie else False
                        
                        if cookie:
                        
                            Print.log('[+] Set cookie')
                        
                            cookies = Cookis.getCookie(self.ch, url)
                        
                            if cookies: self.context.add_cookies(cookies)
                    
                    Print.log(f'[+] Go to: {self.url}')
                    
                    self.page.goto(_s_url)
                    
                    Cookis.setCookie(self.context.cookies(), self.ch, url)
                
                    Print.log("[+] Wait after goto")
                    
                    self.actions.d_wait_random({"min": 4, "max": 5})
                
                    time_s = self.url['time']
                
                    time_s = random.randint(int(time_s[0]), int(time_s[1]))
                
                    Print.log(f"[+] Time walk {time_s}")
                
                    time_s = int(time.time()) + time_s
                
                    Print.log(f'[+] Full time in sec {time_s}')
                
                    while time_s > int(time.time()):
                    
                        if self.error > 5:
                            Print.error('[+] Error limit exceeded')
                            return False
                    
                        res = self.walk()
                    
                        if res: Print.ok('[+] Walk without mistakes')
                    
                        else:
                            Print.error("[+] Walk with mistakes")
                            self.error += 1
                    
                        res = None
                
                    Print.ok("[+] Time walk is done.")
            
                    return True
            
                except Exception as e:
                    Print.error('[+] Error in { with playwright }')
                    Print.error(e)
                    self.page.close()
                    self.context.close()
                    self.browser.close()
        
        except Exception as e:
            
            Print.error('[+] Error in method run')
            Print.error(e)
                
            return False








