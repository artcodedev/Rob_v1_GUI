import sys
sys.path.insert(1, '../')
from Print import Print
import pyautogui as pg
import random

class Move:
    
    
    @staticmethod
    async def move(act):
        
        try:
            
            Print.log("[+] Move rundom")
            count = random.randint(5, 15)
            
            Print.log(f'[+] Count move {count}')
            
            for i in range(0, count):
                view = pg.size()
                
                x = random.randint(0, view.width)
                y = random.randint(0, view.height)
                
                Print.log("[+] Move")
                act.mosemove(x, y)
            
            Print.ok("[+] Move rundom is done.")
        
        except Exception as e:
            Print.error("[+] Error in random_move class")
            Print.error(e)
        
        