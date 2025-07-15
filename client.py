#DEPENDECIES
import requests
import time
from datetime import datetime
import pyautogui

#CONFIG
ID = "68762d08bb9a9d26e899fb2d"
HEADERS = {"X-Master-Key": "$2a$10$TT0MR0B7t3rMs/O05cZ1O.T3TDdiy4Jf9wAA9mFkfYDie7anZwky2"}
URL = "https://webhook.site/f45055db-2642-4f54-884c-3d55eb5fabb8"  # <-- REPLACE THIS

def fetch_click_time():
    
    url = f"https://api.jsonbin.io/v3/b/{ID}/latest"
    
    try:
        
        res = requests.get(url, headers=HEADERS)
        
        if res.status_code == 200:
            
            data = res.json()
            return data['record']['click_time_utc']
        
    except Exception as e:
        
        print("[ERROR] Failed to fetch time:", e)
        
    return None

def wait_until(target_time_str):
    
    target = datetime.strptime(target_time_str, "%H:%M:%S.%f").time()
    
    print(f"[CLIENT] Waiting for click at {target_time_str} UTC...")
    
    while True:
        
        now = datetime.utcnow().time()
        
        if now >= target:
            
            break

def send_log(username, clicked_time):
    
    payload = {
        "user": username,
        "clicked_time_utc": clicked_time
    }
    
    try:
        
        res = requests.post(URL, json=payload)
        
        if res.status_code in (200, 201):
            
            print("[LOG] Click time sent successfully.")
        else:
            
            print("[LOG] Failed to send log:", res.status_code)
            
    except Exception as e:
        
        print("[ERROR] Could not send log:", e)

#DRIVER
username = input("Enter your name: ").strip()
click_time = fetch_click_time()

if click_time:
    
    wait_until(click_time)
    
    pyautogui.click()
    
    clicked_at = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
    
    print(f"[CLIENT] Clicked at {clicked_at} UTC")
    send_log(username, clicked_at)
    
else:
    
    print("[CLIENT] Could not fetch click time.")
