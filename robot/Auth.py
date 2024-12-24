
import sys
sys.path.insert(1, '../')
from Print import Print
from Executor import Executor

class Auth:
    
    
    @staticmethod
    async def auth(page, act, auth_data):
        
        try:
            Print.log("[+] Auth")
        
            logged_user = await page.evaluate(f'''document.querySelectorAll("a[href='/popup-messagebox']")''')
            
            if logged_user != None:
                Print.warning("[+] User is logged")
                return
        
            Print.log("[+] User is not logged")
        
            
            act.d_wait_random({"min": 1, "max": 2})
            
            popup_login = await page.evaluate(f'''document.querySelectorAll("a[href='/popup-login']")''')
            
            Print.log(popup_login)
            
            if len(popup_login) == 0:
                Print.error("[+] Eleme /popup-login not found")
                return
            
            Print.log("[+] Click /popup-login")
            
            login = await Executor.coords(page, "a[href='/popup-login']", 0)
            
            act.d_click(login)
            
            Print.log("[+] Random wait")
            act.d_wait_random({"min": 1, "max": 2})
            
            type_login = await Executor.coords(page, f"div[data-popup-tabs-name='{auth_data['type']}']", 0)
            
            if type_login == None:
                Print.error("[+] Eleme {type_login} not found")
                return
            
            if len(type_login) == 0:
                Print.error("[+] Eleme {type_login} not found")
                return
            
            act.d_click(type_login)
            
            act.d_wait_random({"min": 1, "max": 2})
            
            sign_in = await Executor.coords(page, f"input[id='sign-in-{auth_data['type']}']", 0)
            
            if sign_in == None:
                Print.error("[+] Eleme {type_login} not found")
                return
            
            if len(sign_in) == 0:
                Print.error("[+] Eleme {type_login} not found")
                return
            
            act.d_click(sign_in)
            
            act.d_wait_random({"min": 1, "max": 2})
            
            act.write_text(auth_data['login'])
            
            act.d_wait_random({"min": 1, "max": 2})
            
            pass_s = 'sign-in-password' if auth_data['type'] == 'email' else f'sign-in-{auth_data['type']}-password'
            
            pass_input = await Executor.coords(page, f"input[id='{pass_s}']", 0)
            
            if pass_input == None:
                Print.error(f"[+] Eleme {pass_s} not found")
                return 
            
            if len(pass_input) == 0:
                Print.error(f"[+] Eleme {pass_s} not found")
                return
            
            act.d_click(pass_input)
            
            act.d_wait_random({"min": 1, "max": 2})
            
            act.write_text(auth_data['pass'])
            
            act.d_wait_random({"min": 1, "max": 2})
            
            submit = await Executor.coords(page, f"button[data-test='submit_button']", 0)
            
            if submit == None:
                Print.error("[+] Eleme {submit_button} not found")
                return
            
            if len(submit) == 0:
                Print.error("[+] Eleme {submit_button} not found")
                return
            
            act.d_click(submit)
            
            act.d_wait_random({"min": 4, "max": 5})
                       
            
        except Exception as e:
            Print.error("[+] Error in AUTH")
            Print.error(e)



