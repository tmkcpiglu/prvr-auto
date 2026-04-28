# -*- coding: utf-8 -*-
import os, time, re, random, threading, gc, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

# --- ⚙️ PILLAR V130.8 CONFIG ---
THREADS = 4             
PULSE_DELAY = 600       
SESSION_MAX_SEC = 1200  
TOTAL_DURATION = 40000  

sys.stdout.reconfigure(encoding='utf-8')

def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.page_load_strategy = 'eager'
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Linux armv8l", fix_hairline=True)
    return driver

def run_agent(agent_id, cookie, target_id, target_name):
    global_start = time.time()
    while (time.time() - global_start) < TOTAL_DURATION:
        driver = None
        try:
            driver = get_driver()
            driver.get("https://www.instagram.com/")
            sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
            driver.add_cookie({'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{target_id}/")
            time.sleep(7)

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
                        const finalText = pillar + "⚡ ID: " + Math.random().toString(36).substring(7);
                        box.focus();
                        document.execCommand('insertText', false, finalText);
                        box.dispatchEvent(new Event('input', { bubbles: true }));
                        const enter = new KeyboardEvent('keydown', {bubbles: true, key: 'Enter', keyCode: 13});
                        box.dispatchEvent(enter);
                    }
                }, delay);
            """, target_name, PULSE_DELAY)
            time.sleep(SESSION_MAX_SEC)
        except: pass
        finally:
            if driver: driver.quit()
            gc.collect()

if __name__ == "__main__":
    os.system('pip install selenium-stealth webdriver-manager')
    COOKIE = "REPLACE_COOKIE"
    THREAD = "REPLACE_THREAD"
    NAME = "REPLACE_NAME"
    threads = [threading.Thread(target=run_agent, args=(i+1, COOKIE, THREAD, NAME)) for i in range(THREADS)]
    for t in threads: t.start()
    for t in threads: t.join()
