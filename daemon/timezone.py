
from datetime import datetime
import pytz

class Time:
    
    def getTimeZone(self, timezone: str):
        
        zone = pytz.timezone(timezone)
        
        hour = datetime.now(zone).strftime('%H')
        
        if len(hour) == 2 and hour[0] == '0': hour = hour[1]
        
        return hour
