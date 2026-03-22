import os
import time
import logging
import subprocess
import requests
import csv
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- THE TEAM CONFIGURATION ---
AUTHOR_USER = "Kali Student"
AUTHOR_AI = "Gemini"
MISSION = "To Save the World through Internet Safety"
VERSION = "2.0 (Collaborative Edition)"

USER_NAME = "kali"
BASE_DIR = f"/home/{USER_NAME}/safety_monitor_test"
BLACKLIST_FILE = f"{BASE_DIR}/blacklist.txt"
LOG_FILE = f"{BASE_DIR}/security_events.log"
REPORT_FILE = f"{BASE_DIR}/daily_report.csv"
THREAT_FEED_URL = "https://feodotracker.abuse.ch/downloads/ipblocklist.txt"

def generate_report(ip, action):
    """Logs every victory into a CSV report."""
    file_exists = os.path.isfile(REPORT_FILE)
    with open(REPORT_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Threat_IP", "Action_Taken", "Architects"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ip, 
            action, 
            f"{AUTHOR_USER} and {AUTHOR_AI}"
        ])

def update_blacklist():
    print(f"[*] {AUTHOR_AI}: Syncing with global threat intelligence...")
    try:
        response = requests.get(THREAT_FEED_URL, timeout=5)
        if response.status_code == 200:
            new_ips = [line.strip() for line in response.text.splitlines() if not line.startswith("#") and line.strip()]
            with open(BLACKLIST_FILE, "a") as f:
                for ip in new_ips:
                    f.write(f"{ip}\n")
            print(f"[+] {AUTHOR_USER}: Successfully added {len(new_ips)} threats to the shield.")
    except Exception as e:
        print(f"[!] Sync issue: {e}. Using local shield only.")

def kill_connection(ip):
    print(f"[!] SHIELD ACTIVE: Neutralizing {ip}...")
    try:
        pid_cmd = f"ss -ntup | grep {ip} | grep -oP 'pid=\\K\\d+'"
        pid_output = subprocess.check_output(pid_cmd, shell=True).decode().strip()
        if pid_output:
            for pid in pid_output.split('\n'):
                os.system(f"kill -9 {pid}")
        else:
            os.system(f"ss -K dst {ip}")
        # Record the victory
        generate_report(ip, "Connection Terminated")
    except Exception:
        os.system(f"ss -K dst {ip}")

def check_network():
    if not os.path.exists(BLACKLIST_FILE): return
    with open(BLACKLIST_FILE, 'r') as f:
        blacklist = set(line.strip() for line in f if line.strip())
    try:
        output = subprocess.check_output("ss -ntup state established", shell=True).decode()
        for line in output.split('\n'):
            for bad_ip in blacklist:
                if bad_ip in line and bad_ip != "":
                    kill_connection(bad_ip)
    except Exception:
        pass

if __name__ == "__main__":
    print("-" * 45)
    print(f"KALI SAFETY EDR - {VERSION}")
    print(f"Architect: {AUTHOR_USER}")
    print(f"Collaborator: {AUTHOR_AI}")
    print(f"Mission: {MISSION}")
    print("-" * 45)

    update_blacklist()
    
    observer = Observer()
    observer.schedule(FileSystemEventHandler(), BASE_DIR, recursive=False)
    observer.start()
    
    print(f"[*] {AUTHOR_USER}, the shield is active. Monitoring...")
    try:
        while True:
            check_network()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
