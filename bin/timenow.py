from datetime import datetime

def TimeNow():
    now = datetime.now()
    current_time = now.strftime("%m/%d/%y %H:%M:%S")
    return f"[{current_time}]"
