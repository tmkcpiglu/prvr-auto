# -*- coding: utf-8 -*-
import subprocess
import sys
import os
import time

# 🛠️ CRITICAL: FORCE INSTALL DEPENDENCIES BEFORE IMPORTS
def prepare_environment():
    print("🔧 Installing Titan Dependencies...", flush=True)
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", 
                               "selenium", "selenium-stealth", "webdriver-manager"])
        print("✅ Environment Ready.", flush=True)
    except Exception as e:
        print(f"❌ Installation Failed: {e}", flush=True)

prepare_environment()

# Standard imports
import re, random, threading, gc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

# --- ⚙️ PILLAR CONFIG ---
THREADS = 4             # Optimized for 30GB RAM
PULSE_DELAY = 600       # 0.6s Stability
TOTAL_DURATION = 40000  # ~11 Hours

def get_driver():
    print("🛰️ Attempting to Auto-Locate Chrome Driver...", flush=True)
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    
    # Force Kaggle Internal Binary Path
    options.binary_location = "/usr/bin/google-chrome"
    
    driver = None
    
    # Strategy 1: Webdriver Manager (Download matching version)
    try:
        print("📥 Strategy 1: Downloading compatible driver...", flush=True)
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        print("✅ Strategy 1 Success.", flush=True)
    except Exception as e1:
        print(f"⚠️ Strategy 1 Failed: {e1}", flush=True)
        
        # Strategy 2: Use Kaggle's Pre-installed Path
        try:
            print("📁 Strategy 2: Checking system paths...", flush=True)
            service = Service("/usr/bin/chromedriver")
            driver = webdriver.Chrome(service=service, options=options)
            print("✅ Strategy 2 Success.", flush=True)
        except Exception as e2:
            print(f"❌ Strategy 2 Failed: {e2}. Attempting Final Fallback...", flush=True)
            # Strategy 3: Standard discovery
            try:
                driver = webdriver.Chrome(options=options)
                print("✅ Strategy 3 Success.", flush=True)
            except Exception as e3:
                print(f"🛑 ALL STRATEGIES FAILED: {e3}", flush=True)
                return None

    if driver:
        stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Linux armv8l", fix_hairline=True)
    return driver

def run_agent(agent_id, cookie, target_id, target_name):
    print(f"🚀 [Agent {agent_id}] Initializing...", flush=True)
    driver = get_driver()
    
    if not driver:
        print(f"🛑 [Agent {agent_id}] Driver creation failed. Skipping.", flush=True)
        return

    try:
        print(f"🔗 [Agent {agent_id}] Loading Instagram...", flush=True)
        driver.get("https://www.instagram.com/")
        time.sleep(5)
        
        # Inject Cookie
        sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
        driver.add_cookie({'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com'})
        
        # Go to Chat
        driver.get(f"https://www.instagram.com/direct/t/{target_id}/")
        time.sleep(8)
        print(f"🔥 [Agent {agent_id}] TARGET LOCKED: {target_name}. Starting Pillar Strike...", flush=True)
        
        # 🔱 THE JAVASCRIPT PILLAR INJECTOR
        driver.execute_script("""
            const name = arguments[0];
            const delay = arguments[1];
            const phrases = [
                `[${name}] 𝑻𝑬𝑹𝑰 𝑴𝑨𝑨 𝑲𝑨 𝑩𝑯𝑶𝑺𝑫𝑨 𝑷 𝑹 𝑽 𝑹 𝑷𝑨𝑷𝑨 𝑲𝑨 𝑮𝑼𝑳𝑨𝑴 🔥`,
                `[${name}] 𝑷 𝑹 𝑽 𝑹 𝑷𝑨𝑷𝑨 𝑵𝑬 𝑻𝑬𝑹𝑰 𝑴𝑨𝑨 𝑲𝑶 𝑵𝑨𝑵𝑮𝑨 𝑲𝑨𝑹 𝑫𝑰𝒀𝑨 😂`,
                `[${name}] 𝑹𝑼𝑵𝑫𝑰 𝑲𝑬 𝑩𝑨𝑪𝑪𝑯𝑬 𝑩𝑨𝑨𝑷 𝑺𝑬 𝑷𝑨𝑵𝑮𝑨 𝑵𝑨𝑯𝑰 𝑳𝑬𝑻𝑬 🤡`,
                `[${name}] 𝑷 𝑹 𝑽 𝑹 𝑷𝑨𝑷𝑨 𝑻𝑬𝑹𝑨 𝑲𝑯𝑨𝑨𝑵𝑫𝑨𝑨𝑵𝑰 𝑴𝑨𝑨𝑳𝑰𝑲 𝑯𝑨𝑰 👑`,
                `[${name}] 𝑻𝑬𝑹𝑰 𝑴𝑨𝑨 𝑲𝑰 𝑪𝑯𝑼𝑻 𝑴𝑨𝑰 𝑷 𝑹 𝑽 𝑹 𝑷𝑨𝑷𝑨 𝑲𝑨 𝑯𝑨𝑻𝑯𝑶𝑫𝑨 🔨`,
                `[${name}] 𝑱𝑨𝑳𝑫𝑰 𝑺𝑬 𝑷 𝑹 𝑽 𝑹 𝑷𝑨𝑷𝑨 𝑲𝑨 𝑳𝑨𝑼𝑫𝑨 𝑪𝑯𝑶𝑶𝑺 𝑳𝑬 𝑲𝑨𝑻𝑻𝑬 👅`
            ];
            
            setInterval(() => {
                const box = document.querySelector('div[role="textbox"], [contenteditable="true"]');
                if (box) {
                    const baseMsg = phrases[Math.floor(Math.random() * phrases.length)];
                    let pillar = "";
                    for(let i=0; i<15; i++) { pillar += baseMsg + "\\n"; }
                    const finalText = pillar + "🔱 ID: " + Math.random().toString(36).substring(7);
                    
                    box.focus();
                    document.execCommand('insertText', false, finalText);
                    box.dispatchEvent(new Event('input', { bubbles: true }));
                    
                    const enter = new KeyboardEvent('keydown', {
                        bubbles: true, cancelable: true, key: 'Enter', code: 'Enter', keyCode: 13
                    });
                    box.dispatchEvent(enter);
                }
            }, delay);
        """, target_name, PULSE_DELAY)
        
        time.sleep(TOTAL_DURATION) 
        
    except Exception as e:
        print(f"⚠️ Agent {agent_id} Error: {e}", flush=True)
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    # Secrets replaced by GitHub Action
    COOKIE = "REPLACE_COOKIE"
    THREAD = "REPLACE_THREAD"
    NAME = "REPLACE_NAME"
    
    print(f"🔱 P R V R PAPA SYSTEM STARTING...", flush=True)
    
    threads = []
    for i in range(THREADS):
        t = threading.Thread(target=run_agent, args=(i+1, COOKIE, THREAD, NAME))
        t.start()
        threads.append(t)
        time.sleep(5) 

    for t in threads:
        t.join()
