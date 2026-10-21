import os
import platform
from pathlib import Path

def audit_startup_items():
    print("--- STARTUP ITEM & PERSISTENCE AUDIT ---")
    current_os = platform.system()
    
    paths_to_check = []
    if current_os == "Darwin":
        home = Path.home()
        paths_to_check = [
            home / "Library/LaunchAgents",
            Path("/Library/LaunchAgents"),
            Path("/Library/LaunchDaemons")
        ]
    elif current_os == "Linux":
        home = Path.home()
        paths_to_check = [
            home / ".config/systemd/user",
            Path("/etc/systemd/system"),
            Path("/etc/cron.d")
        ]
    else:
        print("[-] Unsupported OS for startup persistence scanning.")
        return

    total_items = 0
    for target_dir in paths_to_check:
        print(f"\nScanning directory: {target_dir}")
        if not target_dir.exists():
            print("  -> Directory does not exist or is not accessible.")
            continue
        
        count = 0
        for item in target_dir.iterdir():
            if item.is_file():
                print(f"  [Found] {item.name}")
                count += 1
                total_items += 1
        if count == 0:
            print("  -> No items found.")

    print(f"\n[+] Persistence audit complete. Total items identified: {total_items}")

if __name__ == "__main__":
    audit_startup_items()
