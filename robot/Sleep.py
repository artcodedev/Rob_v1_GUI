

import time
import random
import sys
sys.path.insert(1, '../')
from Print import Print


class Sleep:
    
    @staticmethod
    def zZz(sl):
        
        try:
            for i in range(0, int(sl)):
                zs = ''
                for i1 in range(0, random.randint(3, 7)):
                    time.sleep(.30)
                    z = ['z', 'Z'][random.randint(0, 1)]
                    zs += z
                    print(f'\r[+] Sleep {sl}s! {zs}', end='')
        
        except Exception as e:
            Print.error('[+] Error in method zZz')
            Print.error(e)