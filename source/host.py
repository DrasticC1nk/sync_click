#DEPENDECIES
import requests
from datetime import datetime, timedelta, timezone

#CONFIG
KEY = "$2a$10$TT0MR0B7t3rMs/O05cZ1O.T3TDdiy4Jf9wAA9mFkfYDie7anZwky2"
ID = "68762d08bb9a9d26e899fb2d"
HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": KEY
}
URL = f"https://api.jsonbin.io/v3/b/{ID}"

#IST TO UTC
def ist_to_utc(ist_time_str):
    
    ist = timezone(timedelta(hours=5, minutes=30))
    ist_now = datetime.now(ist)
    time_part = datetime.strptime(ist_time_str, "%H:%M:%S.%f").time()
    ist_dt = datetime.combine(ist_now.date(), time_part).replace(tzinfo=ist)
    utc_dt = ist_dt.astimezone(timezone.utc)
    
    return utc_dt.strftime("%H:%M:%S.%f")[:-3] 

#SENDING PAYLOAD
def update_time(new_time_utc):
    
    data = {
        "click_time_utc": new_time_utc,
        "logs": []  # Reset logs for fresh round
    }

    res = requests.put(URL, json=data, headers=HEADERS)
    
    if res.status_code == 200:
        print(f"[HOST] Set click time to: {new_time_utc} UTC and cleared logs.")
        
    else:
        print("[ERROR] Failed to set time:", res.text)

#DRIVER
ist_input = input("Enter click time in IST (HH:MM:SS.mmm): ").strip()

try:
    
    utc_time = ist_to_utc(ist_input)
    
    print(f"[INFO] Converted to UTC: {utc_time}")
    update_time(utc_time)
    
except Exception as e:
    
    print("[ERROR] Invalid time format. Use HH:MM:SS.mmm (e.g., 15:01:00.000)")
    
    print(e)  
