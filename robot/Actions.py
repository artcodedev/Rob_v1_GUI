
import sys
sys.path.insert(1, '../')
import pyautogui as pg
import time
import os
import random
import numpy as np
from Print import Print
from playwright.sync_api import sync_playwright, Playwright

pg.FAILSAFE = False

class Actions:
    
    def __init__(self, mouse=None, scroll=None, top=None) -> None:
        self.mouse = mouse
        self.scroll = scroll
        self.top = top
    
    def speed_mouse_cur(self): return [pg.easeInQuad, pg.easeInOutQuad, pg.easeOutQuad][self.t(0, 2)]
    
    
    def d_wait_random(self, d: dict): time.sleep(self.t(int(d['min']), int(d['max'])))
    
    
    def moveTo(self, x: int, y: int, t: float): pg.moveTo(x, y, t, self.speed_mouse_cur())
    
    
    def t(self, a: int, b: int): return random.randint(a, b)
    
    
    def locateOnScreen(self, image: str):
        
        try: return pg.locateOnScreen(os.path.abspath(image))
        except: return False
    
    
    def f_move_random_scroll(self):
        
        try:
            view_h = pg.size().height
            view_w = pg.size().width
            pro_20 = lambda a : int((a / 100) * 20)
            
            x = self.t(pro_20(view_w), view_w - pro_20(view_w))
            y = self.t(pro_20(view_h), view_h - pro_20(view_h))
            
            # ========================
            self.mosemove(x, y)
            # ========================
            
            time.sleep(self.t(200, 600) / 1000)
            
        except Exception as e:
            Print.error('[+] Error in move_random_scroll')
            Print.error(e)
    
    
    def d_move_random(self, p: dict) -> object:
        try:
            s = self.t(900, 1000) / 1000
            x = self.t(p['x']['min'], p['x']['max'])
            y = self.t(p['y']['min'], p['y']['max'])
            
            # ========================
            self.mosemove(x, y)
            # ========================
            
            time.sleep(self.t(200, 600) / 1000)
            return True
        except:
            return False
    
    
    def mosemove(self, x: int, y: int):
        pos_xy = pg.position()
        
        
        G_0 = random.randint(self.mouse['G_0'] - 10, self.mouse['G_0'] + 10)
        W_0 = random.randint(self.mouse['W_0'] - 10, self.mouse['W_0'] + 10)
        M_0 = random.randint(self.mouse['M_0'] - 10, self.mouse['M_0'] + 10)
        D_0 = random.randint(self.mouse['D_0'] - 10, self.mouse['D_0'] + 10)    
        
        self.wind_mouse(pos_xy.x, pos_xy.y, x, y, G_0, W_0, M_0, D_0)
    
    
    def divide(self, value: int, parts: int) -> int:
        res = [random.random() for _ in range(int(parts))]
        coef = value / sum(res)
        return [int(x * coef) for x in res]


    def wind_mouse(self, start_x, start_y, dest_x, dest_y, G_0, W_0, M_0, D_0):
        
        sqrt3 = np.sqrt(2)
        sqrt5 = np.sqrt(10)

        current_x, current_y = start_x, start_y
        v_x = v_y = W_x = W_y = 0
        
        
        while (dist := np.hypot(dest_x - start_x, dest_y - start_y)) >= 1:
            W_mag = min(W_0, dist)
            if dist >= D_0:
                W_x = W_x / sqrt3 + (2 * np.random.random() - 1) * W_mag / sqrt5
                W_y = W_y / sqrt3 + (2 * np.random.random() - 1) * W_mag / sqrt5
            else:
                W_x /= sqrt3
                W_y /= sqrt3
                
                if M_0 < 3:
                    M_0 = np.random.random() * 3 + 3
                else:
                    M_0 /= sqrt5
                    
                    
            v_x += W_x + G_0 * (dest_x - start_x) / dist
            v_y += W_y + G_0 * (dest_y - start_y) / dist
            
            v_mag = np.hypot(v_x, v_y)
            if v_mag > M_0:
                v_clip = M_0 / 2 + np.random.random() * M_0 / 2
                v_x = (v_x / v_mag) * v_clip
                v_y = (v_y / v_mag) * v_clip
            start_x += v_x
            start_y += v_y
            move_x = int(np.round(start_x))
            move_y = int(np.round(start_y))
            
            if current_x != move_x or current_y != move_y:
                pg.moveTo(abs(move_x), abs(move_y), .1, self.speed_mouse_cur())
        
        return current_x, current_y
    
    
    def d_scroll(self, height, x = None, y = None):
        
        try:
            
            if x is not None and y is not None: self.mosemove(x, y)
            
            Print.log("[+] Scrolling")
            
            min = self.scroll['min']
            max = self.scroll['max']
            
            Print.log(f'[+] Min: {min} ; Max: {max}')
            
            if height != 0:
                
                height = self.divide(height, 8 * abs(height / 1000)) if height > 2000 or height < -2000 else self.divide(height, 8)

            for i in height:
                
                time.sleep(self.t(min, max) / 1000)
                pg.scroll(i)
                
            if height == 0: pg.scroll(height)
                
            time.sleep(self.t(min, max) / 1000)
            
            Print.ok("[+] Scrolling done.")
            
            return True
        
        except Exception as e:
            Print.error(e)
            return False
    
    
    def write_text(self, txt):
        
        try:
            
            for i in str(txt):
                pg.write(i, interval=random.randint(10, 40) / 100)
        
        except Exception as e:
            Print.error(e)
    
    
    def d_click(self, but):

        x = int(but['left'])
        y = int(but['top'])

        width = int(but['width'])
        height = int(but['height'])

        pr = (int((width / 100) * 35))
        pr_h = (int((height / 100) * 35))

        x = self.t(x + pr, x + (width - pr))
        y = self.t(y + pr_h, y + (height - pr_h)) + self.top
        
        time.sleep(self.t(200, 600) / 1000)

        self.mosemove(x, y)
        
        time.sleep(self.t(100, 300) / 1000)
        
        pg.click()
        
        time.sleep(self.t(100, 300) / 1000)
        
        if random.randint(0, 1): 
            
            viewport = pg.size()
            view_y = random.randint(0, viewport.height)
            view_x = random.randint(0, viewport.width)
            
            self.mosemove(view_x, view_y)
    
    


