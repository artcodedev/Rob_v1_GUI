


import sys
sys.path.insert(1, '../')
import pyautogui as pg
import time
import os
import random
import numpy as np
from Print import Print
from Actions import Actions
from Executor import Executor



class Study:
        
    @staticmethod
    def reads_carefully(obj, act):
        
        Print.log("[+] Read carefully")
        
        obj_w = int(obj['width'])
        obj_h = int(obj['top'])
        
        mass = []
        
        for i in range(0, int(obj_h / 10)):
            
            h = i * 10
            
            for i1 in range(0, int(obj_w / 10)):
                
                w = i1 * 10
                
                mass.append({
                    'x': random.randint(w, w + 10) + obj_w,
                    'y': random.randint(h, h + 10) + obj_h
                })
        
        for i2 in mass: act.mosemove(i2['x'], i2['y'])
    
    
    @staticmethod
    def just_drives(obj, act):
        
        Print.log("[+] Just driver")
        
        mass = []
        
        for i in range(0, random.randint(5, 15)):
            
            mass.append({ 
                "x": random.randint(0, int(obj['width']) ) + int(obj['left']),
                "y": random.randint(0, int(obj['height']) ) + int(obj['top'])
            })
            
        for i in mass: act.mosemove(i['x'], i['y'])
    
    
    @staticmethod
    async def study(t, page, act, top):
        
        try:
            
            Print.log("[+] Start study")
            
            tag = 'p' if t == 'txt' else 'img'
            
            Print.log(f'[+] Tag study {tag}')
            
            Print.log("[+] Study wait")
            act.d_wait_random({"min": 3, "max": 4})
            
            
            Print.log("[+] Get elem for study")
            locator = await Executor.locator(page, tag)
            
            if len(locator) == 0: 
                Print.warning(f"[+] Element {t} is not found")
                return
            
            Print.log(f"[+] Length elem : {len(locator)}")
            
            el = random.randint(0, len(locator) - 1)
            
            Print.log(f'[+] Element {el}')
            
            coords = locator[el]
            
            coords = await Executor.coords(page, tag, el)
            
            Print.log(f"[+] Coords {coords}")
            
            view_h = pg.size().height
 
            act.f_move_random_scroll()
            
            coords = await Executor.coords(page, tag, el)
            
            if coords['top'] > (view_h - 100) or coords['top'] < 0:
                
                ck = True
                counter = 0
                
                coords = await Executor.coords(page, tag, el)
               
                padding_top = await page.evaluate("document.documentElement.clientHeight")
                
                while ck:
                    
                    if counter > 10:
                        Print.warning('[+] Counter study scroll > 10')
                        break
                    
                    counter += 1
                    
                    y = coords['top']                    
                    if y > (view_h - 200):
                        Print.log('[+] y > height view')
                        act.d_scroll((y - (view_h / 2)) * -1)
                    
                    if y < 100:
                        Print.log('[+] y < height view')
                        act.d_scroll(abs(y) + padding_top + (padding_top - view_h))
                    
                    if y > 100 and y < (view_h - 200):
                        Print.ok("[+] Scroll completed on element")
                        ck == False
                        break
                    
                    Print.log('[+] Next step while scroll')
                    
                    coords = await Executor.coords(page, tag, el)
                    
                    Print.log(coords)
            
            Print.log("[+] Update coords")
            
            coords = await Executor.coords(page, tag, el)
            
            Print.log(f"[+] Coords {coords}")
            
            coords['top'] = coords['top'] + int(top)
            
            Print.log(f"[+] Coords {coords}")
            
            Study.just_drives(coords, act)
            
            if t == 'txt':
                
                Print.log('[+] Study TXT')
                
                Study.reads_carefully(coords, act) if random.randint(0, 1) else Study.just_drives(coords, act)
                
            else:
                
                Print.log('[+] Study IMG')
                
                Study.just_drives(coords, act)
            
            Print.ok("[+] Study is done.")
            

        
        except Exception as e:
            Print.error(e)
