import os
import time
import psutil
import logging

# Setup Logging to a file
# This is the "Forensic Record" for security audits
LOG_FILE = "/var/log/kali-safety-edr.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - SECURITY_EVENT - %(message)s'
)

def monitor_and_defend():
    # Standard console output for service status
    print(f"EDR Active. Logging events to {LOG_FILE}...")
    logging.info("EDR Service Started - Monitoring Active.")
    
    # List of unauthorized processes to terminate
    THREAT_LIST = ["nmap", "netcat", "nc"]

    while True:
        # Iterate through all running processes
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # Check if process name is in our threat list
                if proc.info['name'].lower() in THREAT_LIST:
                    event_msg = f"THREAT NEUTRALIZED: Process {proc.info['name']} (PID: {proc.info['pid']}) terminated."
                    
                    # Print to terminal and save to formal log file
                    print(event_msg)
                    logging.warning(event_msg)
                    
                    # Terminate the unauthorized process
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Handle processes that close before we can scan them
                pass
        
        # Poll every 2 seconds to balance security and CPU usage
        time.sleep(2)

if __name__ == "__main__":
    monitor_and_defend()
