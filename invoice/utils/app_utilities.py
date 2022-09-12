from datetime import datetime
import pytz

def app_time():
    return datetime.now(pytz.timezone('Africa/Nairobi')
                         ).strftime("%Y-%m-%d %H:%M:%S")

def app_date():
    return datetime.now(pytz.timezone('Africa/Nairobi')).strftime("%Y-%m-%d")