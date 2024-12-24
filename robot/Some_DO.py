
import sys
sys.path.insert(1, '../')
from Print import Print
from Executor import Executor


class Some_DO:
    
    @staticmethod
    async def some_do(page, act, s):
        
        for i in  s:
            
            try:
                
                Print.log("[+] Start Some Do")
                
                el = await Executor.locator(page, i['el'])
                
                if el == None:
                    Print.warning(f"[+] Elem {i['el']} is None")
                    continue
                
                if len(el) == 0:
                    Print.warning(f"[+] Not found elem {i['el']}")
                    continue
                
                coords = await Executor.coords(page, i['el1'], 0)
                
                if coords == None:
                    Print.warning(f'[+] Can not get coords elem {i['el1']}')
                    continue
                
                if len(coords) > 0:
                    Print.log('[+] Some do elem is > 0')
                        
                    Print.log(f'[+] Link {coords}')
                            
                    if coords != None: act.d_click(coords)
                
                Print.log('[+] Next step Some_DO')
                
            except Exception as e:
                Print.error('[+] Error in Some DO')
                Print.error(e)
