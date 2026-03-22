import os
import time
import psutil
import logging

LOG_FILE = "/var/log/kali-safety-edr.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - SECURITY_EVENT - %(message)s'
)

def monitor_and_defend():
    print(f"EDR Active. Logging events to {LOG_FILE}...")
    logging.info("EDR Service Started - Monitoring Active.")
    
    # Expanded list to catch all variants of Netcat
    THREAT_LIST = ["nc", "ncat", "netcat", "netcat-traditional", "netcat-openbsd"]

    while True:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # We check if the process name STARTS with or IS one of our threats
                proc_name = proc.info['name'].lower()
                if any(threat in proc_name for threat in THREAT_LIST):
                    event_msg = f"THREAT NEUTRALIZED: Process {proc_name} (PID: {proc.info['pid']}) terminated."
                    print(event_msg)
                    logging.warning(event_msg)
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        time.sleep(1) # Faster polling (1 second) for better response
