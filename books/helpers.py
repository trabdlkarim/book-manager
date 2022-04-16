from datetime import datetime,timedelta

def get_expiry_date(days=21):
    return datetime.today() + timedelta(days=days)
    
def extend_expiry_date(expiry, days=21):
    return expiry + timedelta(days=days)