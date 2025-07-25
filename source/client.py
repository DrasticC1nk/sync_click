#DEPENDECIES
import requests
import time
from datetime import datetime
import pyautogui

#CONFIG
ID = "68762d08bb9a9d26e899fb2d"
HEADERS = {"X-Master-Key": "$2a$10$TT0MR0B7t3rMs/O05cZ1O.T3TDdiy4Jf9wAA9mFkfYDie7anZwky2"}
URL = f"https://api.jsonbin.io/v3/b/{ID}"

def fetch_click_time():
    
    try:
        
        res = requests.get(f"{URL}/latest", headers=HEADERS)
        
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
    
    try:
        
        res = requests.get(f"{URL}/latest", headers=HEADERS)
        
        if res.status_code == 200:
            
            data = res.json()
            logs = data['record'].get('logs', [])
            logs.append({
                "user": username,
                "clicked_time_utc": clicked_time
            })

            payload = {
                "click_time_utc": data['record']['click_time_utc'],
                "logs": logs
            }

            update = requests.put(URL, json=payload, headers=HEADERS)
            
            if update.status_code == 200:
                
                print("[LOG] Click time logged to JSONBin.")
                
            else:
                
                print("[LOG] Failed to update log:", update.text)
        else:
            
            print("[LOG] Failed to read current bin.")
            
    except Exception as e:
        
        print("[ERROR] Could not send log:", e)

#DRIVER
click_time = fetch_click_time()

if not click_time:
    print("[CLIENT] Could not fetch click time.")
    
else:
    wait_until(click_time)

    while True:
        
        username = input("Enter your name (or press Enter to stop): ").strip()
        
        if not username:
            
            print("[CLIENT] Exiting user log loop.")
            
            break

        pyautogui.click()
        
        clicked_at = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
        
        print(f"[CLIENT] {username} clicked at {clicked_at} UTC")
        
        send_log(username, clicked_at)

