import os
import hashlib
import json
from pathlib import Path

BASELINE_FILE = "baseline.json"
MONITOR_DIR = "./monitored_configs"

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return None

def setup_mock_environment():
    os.makedirs(MONITOR_DIR, exist_ok=True)
    sample_file = Path(MONITOR_DIR) / "settings.conf"
    if not sample_file.exists():
        with open(sample_file, "w") as f:
            f.write("server_port=8080\ndebug_mode=false\n")

def generate_baseline():
    setup_mock_environment()
    baseline = {}
    target_path = Path(MONITOR_DIR)
    
    for file_path in target_path.rglob("*"):
        if file_path.is_file():
            file_hash = calculate_sha256(file_path)
            if file_hash:
                baseline[str(file_path)] = file_hash

    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)
    print(f"[+] Baseline created successfully with {len(baseline)} file(s) tracked in '{BASELINE_FILE}'.")

def verify_integrity():
    if not os.path.exists(BASELINE_FILE):
        print("[-] No baseline found! Run with 'baseline' argument first.")
        return

    with open(BASELINE_FILE, "r") as f:
        old_baseline = json.load(f)

    current_baseline = {}
    target_path = Path(MONITOR_DIR)
    
    for file_path in target_path.rglob("*"):
        if file_path.is_file():
            file_hash = calculate_sha256(file_path)
            if file_hash:
                current_baseline[str(file_path)] = file_hash

    print("\n--- FILE INTEGRITY MONITORING REPORT ---")
    modified = []
    added = []
    deleted = []

    # Check for modified or deleted files
    for path, old_hash in old_baseline.items():
        if path not in current_baseline:
            deleted.append(path)
        elif current_baseline[path] != old_hash:
            modified.append(path)

    # Check for newly added files
    for path in current_baseline:
        if path not in old_baseline:
            added.append(path)

    if not (modified or added or deleted):
        print("[+] INTEGRITY CHECK PASSED: No changes detected.")
    else:
        if modified:
            print(f"[!] MODIFIED FILES: {modified}")
        if added:
            print(f"[!] ADDED FILES: {added}")
        if deleted:
            print(f"[!] DELETED FILES: {deleted}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "baseline":
        generate_baseline()
    else:
        verify_integrity()
