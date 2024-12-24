
import pyautogui as pg
import random
from Print import Print


class Scroll:
    
    
    @staticmethod
    async def scroll(page, act):
        
        try:
        
            Print.log("[+] Scroll")
           
            scroll_max = await page.evaluate("Math.max(document.body.scrollHeight, document.documentElement.scrollHeight,document.body.offsetHeight, document.documentElement.offsetHeight, document.body.clientHeight, document.documentElement.clientHeight)")
            
            Print.log(f'[+] Scroll size {scroll_max}')
            
            scroll_max = int(scroll_max)
        
            viewport = pg.size().height
        
            if viewport < scroll_max:
            
                Print.log('[+] Еthere is a possibility to scroll')
            
                count = random.randint(5, 10)
            
                Print.log(f'[+] Count scrolls: {count} ')
            
                for i in range(0, count):
                
                    act.f_move_random_scroll()

                    pos_scroll_now = await page.evaluate("window.pageYOffset")
                    
                    pos_scroll_now = 0 if pos_scroll_now == None else pos_scroll_now
                    
                    Print.log(f'[+] Position scroolY {pos_scroll_now}')
                    
                    pos_scroll_now = int(pos_scroll_now)

                    if pos_scroll_now < (scroll_max / 2):
                        act.d_scroll((random.randint(0, scroll_max - pos_scroll_now) - 1) * - 1)

                    if pos_scroll_now > (scroll_max / 2):
                        act.d_scroll(random.randint(0, pos_scroll_now))
                    
                    act.d_wait_random({"min": 1, "max": 3})
        
        except Exception as e:
            Print.error('[+] Error in Scroll class')
            Print.error(e)
        
        
        Print.ok("Scrolling is done.")