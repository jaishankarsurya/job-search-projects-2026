import psutil
import subprocess
import time
import datetime
import logging

logging.basicConfig(filename="watchdog_audit.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Target process name to watch (e.g., 'python3', 'nginx', 'sshd')
TARGET_SERVICE = "python3" 

def check_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def restart_service():
    print(f"[-] Service '{TARGET_SERVICE}' is down! Attempting restart...")
    logging.warning(f"Service '{TARGET_SERVICE}' detected down. Triggering restart sequence.")
    
    # Example restart command (adjust based on your environment)
    # For a real service: subprocess.run(["sudo", "systemctl", "restart", "your-service"])
    print("[+] Restart command executed successfully (mock).")
    logging.info(f"Restart sequence completed for '{TARGET_SERVICE}'.")

def run_watchdog():
    print(f"[*] Starting Watchdog monitor for service: '{TARGET_SERVICE}' (Press Ctrl+C to stop)...\n")
    try:
        while True:
            is_running = check_process_running(TARGET_SERVICE)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if is_running:
                print(f"[{timestamp}] STATUS: HEALTHY ({TARGET_SERVICE} is running)")
            else:
                print(f"[{timestamp}] STATUS: CRITICAL ({TARGET_SERVICE} is NOT running)")
                restart_service()
                
            time.sleep(5) # Check every 5 seconds for demonstration
    except KeyboardInterrupt:
        print("\n[*] Watchdog stopped by user.")

if __name__ == "__main__":
    run_watchdog()
