

import sys
sys.path.insert(1, '../')
import asyncio
import nodriver as uc
import json
import random
import os
import requests
from Actions import Actions
import time
import datetime
from Print import Print
from Study import Study
from Auth import Auth
from Scroll import Scroll
from Move import Move
from Link import Link
from Some_DO import Some_DO
from Sleep import Sleep
from GetSizePanel import GetSizePanel
from Executor import Executor
from Cookie_ND import Cookie_ND
from nodriver.core.browser import CookieJar 


class User_ND:
    
    
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
        self.extention = f'--load-extension={os.getcwd()}\\0.3.2_0'
    
    
    async def launch_browser(self):
        try:
            self.browser = await uc.start(
                headless=True,
                 browser_args=[
                    self.extention,
                    '--start-maximized'
                    ]
            )
        except Exception as e:
            Print.error(f"[+] Failed to launch browser: {e}")
            raise
        return self.browser


    async def launch_proxy_browser(self, ipPort, username, password):
        try:
            self.browser = await uc.start(
                # headless=True,
                browser_args=[
                    f"--proxy-server={ipPort}",
                    self.extention,
                    '--start-maximized'
                    ]
            )

            self.username = username
            self.password = password

            self.main_tab = await self.browser.get("draft:,")
            
            self.main_tab.add_handler(uc.cdp.fetch.RequestPaused, self.req_paused)
            
            self.main_tab.add_handler(uc.cdp.fetch.AuthRequired, self.auth_challenge_handler)
            
            await self.main_tab.send(uc.cdp.fetch.enable(handle_auth_requests=True))
            
            return self.browser
        
        except Exception as e:
            Print.error(f"[+] Failed to launch proxy browser: {e}")
            raise


    async def auth_challenge_handler(self, event: uc.cdp.fetch.AuthRequired):
        try:
            asyncio.create_task(
                self.main_tab.send(
                    uc.cdp.fetch.continue_with_auth(
                        request_id=event.request_id,
                        auth_challenge_response=uc.cdp.fetch.AuthChallengeResponse(
                            response="ProvideCredentials",
                            username=self.username,
                            password=self.password,
                        ),
                    )
                )
            )
        except Exception as e:
            Print.error(f"[+] Error handling authentication challenge: {e}")


    async def req_paused(self, event: uc.cdp.fetch.RequestPaused):
        try:
            asyncio.create_task(
                self.main_tab.send(
                    uc.cdp.fetch.continue_request(request_id=event.request_id)
                )
            )
        except Exception as e:
            Print.error(f"[+] Error while continuing paused request: {e}")
    
    
    async def walk(self) -> bool:
        
        try:
            
            Print.ok('[+] Next step')
            
            exp = self.movement['experience']
            
            range_walk = random.randint(int(exp['min']),  (exp['max']))
            
            Print.log(f'[+] Range walk {range_walk}')
            await Some_DO.some_do(self.page, self.actions, self.conf['some_do']['check_el'])
            
            for _ in range(0, range_walk):
                
                Print.log("[+] Some do step")
                
                event = ["read_text", "watch_img", "auth", "scroll", "move"]
        
                Print.log('[+] Get random behavior')
                event_el = event[random.randint(0, len(event) - 1)]
                
                Print.warning(f'[+] Type event [{event_el}]')
                
                if event_el == 'read_text': await Study.study("txt", self.page, self.actions, self.top)
                
                if event_el == 'watch_img': await Study.study("img", self.page, self.actions, self.top)
                
                if event_el == 'auth' and self.auth: await Auth.auth(self.page, self.actions, self.auth_data)
                
                if event_el == 'scroll': await Scroll.scroll(self.page, self.actions)
                
                if event_el == 'move': await Move.move(self.actions)
                
            Print.log('[+] Find link for click')
            
            try:
                
                await Link.link(self.page, self.actions, self.conf['close_urls'])
                
            except: pass
            
            Print.log('\n')
            Sleep.zZz(10)
            Print.log('\n')

            return True
        
        except Exception as e:
            Print.error(e)
            return False
    
     
    async def run(self):
        
        try:
            
            Print.log('[+] Start User')
            
            Print.log([f"[+] Date: {datetime.datetime.now()}"])
            
            
            # use proxy
            self.driver = await self.launch_proxy_browser(f'{self.proxy['ip']}:{self.proxy['port']}', self.proxy['login'], self.proxy['pass']) 
            
            # use withpout proxy
            # self.driver = await self.launch_browser()
            
            self.page = self.driver
            
            url = self.url['url']
        
            url__s = self.conf['start_urls']

            url_start = url__s[random.randint(0, len(url__s) - 1)] if len(url__s) > 1 else url__s[0]

            move = self.movement['move']

            _s_url = f"{url}{url_start}"
                
            _s_url = _s_url if 'http' in _s_url else f'https://{_s_url}'
            
            utm = random.randint(0, 1) if self.utm else False
                    
            Print.log(f'[+] Utm status: {utm}')
            
            self.actions = Actions(move['mousemove'], move['scroll'], self.top)
            
            # use utm metrix
            if utm:
                        
                try:
                    
                    Print.log('[+] Get UTM metric')
                    utm = requests.get(f'http://{self.base_url}/api/v1/getutmargs')
                            
                    Print.log(f'[+] UTM: {utm.text}')
                    _s_url = f'{_s_url}{utm.text}'
                        
                except Exception as e:
                    
                    Print.error('[+] Error in get UTM metric')
                    Print.error(e)
            
            Print.log(f"[+] Set cookie type {self.cookie}")
            if self.cookie is not False:
                
                Print.log("[+] Check cookie")
                
                if random.randint(0, 1):
                    
                    Print.log("[+] Set cookies")
                    self.cookie = await Cookie_ND.setCookie(self.driver, "chrome", self.url['url'])
                    
                    Print.warning("[+] Response setCookie")
                    Print.warning(self.cookie)
            
            
            self.page = await self.driver.get(f'{_s_url}?utp=apostol_proxy')
            
            Sleep.zZz(random.randint(5, 7))
            
            if self.cookie is False:
                
                Sleep.zZz(random.randint(1, 2))
                Print.warning("[+] Save cookie")
                await Cookie_ND.saveCookie(self.browser, "chrome", self.url['url'], None)
        
            
            DOMContentLoaded = await Executor.coords(self.page, "a", 0)
            
            Print.log("[+] Tick counter")
            
            DOMContentLoaded_while = True
            
            while DOMContentLoaded_while:
                
                Print.log("[+] Checker tiker counter")
            
                DOMContentLoaded = await Executor.coords(self.page, "a", 0)
                
                Sleep.zZz(1)
                
                if DOMContentLoaded:  DOMContentLoaded_while = False
                
                if DOMContentLoaded != None:
                    break
                
                counter_tick += 1
                
                Print.log(f"[+] Counter tick {counter_tick}")
                
                if counter_tick == 100:
                    Print.error("[+] Counter tick max lenght 100")
                    return False
                
                Print.warning(counter_tick)
                Print.warning(DOMContentLoaded)
            
            if counter_tick == 100:
                Print.error("[+] Counter tick max lenght 100")
                return False
            
            try:
                
                Print.log("[+] Find error-code  ")
                error_code = await self.page.select("div[class=error-code]")
                
                if "ERR_TIMED_OUT" in error_code:
                    Print.warning("[+] Coonect is down")
                    return False
            
            except Exception as e:
                Print.warning(f'[+] {e}')
                
            Sleep.zZz(random.randint(5, 10))
                
            time_s = self.url['time']
                
            time_s = random.randint(int(time_s[0]), int(time_s[1]))
                
            Print.log(f"[+] Time walk {time_s}")
                
            time_s = int(time.time()) + time_s
                
            Print.log(f'[+] Full time in sec {time_s}')
            
            while time_s > int(time.time()):
                    
                if self.error > 5:
                    Print.error('[+] Error limit exceeded')
                    return False
                    
                res = await self.walk()
                    
                if res: Print.ok('[+] Walk without mistakes')
                    
                else:
                    Print.error("[+] Walk with mistakes")
                    self.error += 1
                    
                res = None
                
                Print.ok("[+] Time walk is done.")
                
            Print.log("[+] Save cookie")
            
            if self.cookie is not False:
                
                if type(self.cookie) is bool:
                    
                    Print.log("[+] Save new cookies")   
                    
                    await Cookie_ND.saveCookie(self.browser, "chrome", self.url['url'], None)
                     
                
                file_t = self.cookie if type(self.cookie) is not bool else None
                
                Print.log(f"[+] Update file {file_t}" if file_t is not None else "[+] Create new file session")
                
                await Cookie_ND.saveCookie(self.browser, "chrome", self.url['url'], file_t)
                
            await self.page.close()
                
            return True
        
        except Exception as e:
            Print.error("[+] Error in method start User_ND")
            Print.error(e)
            
            if self.page != None: await self.page.close()
            
            return False
    
          
    def start(self):
        
        try:
            self.top = GetSizePanel().getTop("chrome")
            
            uc.loop().run_until_complete(self.run())
            
        except Exception as e:
            Print.error(e)
    

if __name__ == "__main__":
    
    name_file = None

    try:
        args = sys.argv
        
        name_file = f'{args[1]}.json'
        
        def readfile(file):
            try: 
                
                with open(file, 'r') as f: return json.loads(f.read())
                
            except Exception as e:
                Print.log(e)
                return None
        
        data = readfile(name_file)
        
        if data != None:
            
            os.remove(name_file)
            
            user = User_ND(
                data['url'],
                data['move'],
                data['experience'],
                data['auth'],
                data['movement'],
                data['proxy'],
                data['auth_data'],
                data['conf'],
                data['base_url'],
                data['utm'],
                data['cookie']                     
            )
            
            user.start()
        
        else:
            Print.warning("[+] Can not get data file")
            os.remove(name_file)
        
    except Exception as e:
        Print.error("[+] Error in main User_ND")
        Print.error(e)
        
        try:
            
            if name_file != None: os.remove(name_file)
        
        except Exception as ee:
            Print.error(f"[+] Can not delete file {name_file}")
            Print.error(ee)