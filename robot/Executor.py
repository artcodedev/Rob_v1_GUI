
import sys
sys.path.insert(1, '../')
from Print import Print

class Executor:
    
    @staticmethod
    async def locator_href(page, tag):
        
        try:
            
            qu = f'''let s = []; for (i of [...document.querySelectorAll("{tag}")])'''
            ob_qu = '''{
                
                if (i.attributes) {
                    if (i.attributes.href) {
                        s.push(i.attributes.href.value)
                    }
                }
                
                };s;'''
            
            return await page.evaluate(f'{qu}{ob_qu}')
        
        except Exception as e:
            Print.error(e)
            return None
    
    
    
    @staticmethod
    async def locator(page, el):
        
        try:
            
            qu = f'''var s = []; for (i of [...document.querySelectorAll("{el}")])'''
            
            ob_qu = '''
                    {
                                        
                        var coords = {
                            "left": i.offsetLeft,
                            "top": i.offsetTop,
                            "height": i.clientHeight,
                            "width": i.clientWidth
                        }
                        s.push(coords)
                                    
                    };
                    s;
                    '''
            
            return await page.evaluate(f'{qu}{ob_qu}')
            
        except Exception as e:
            Print.error(e)
            return None
    
    
    
    @staticmethod
    async def coords(page, tag, pos):
        
        try:
            
            qu = f'var qwerqwer = document.querySelectorAll("{tag}")[{pos}];'
            
            ob_coords = '''
            
                    var coords = {
                        "left": qwerqwer.getBoundingClientRect().left,
                        "top": qwerqwer.getBoundingClientRect().top,
                        "width": qwerqwer.getBoundingClientRect().width,
                        "height":  qwerqwer.getBoundingClientRect().height
                    };
                    
                    delete qwerqwer;
                    coords;
                    
                    '''
                     
            return await page.evaluate(f'{qu}{ob_coords}')
        
        except Exception as e:
            Print.error("[+] Cannot read properties of undefined")
            return None