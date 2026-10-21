import re
import os
import csv

SAMPLE_SYSTEM_LOG = """
Oct 20 04:10:15 macbook kernel[0]: AppleIntelLpssI2CController::_serviceIsSuspended - Error
Oct 20 04:12:00 macbook WindowServer[300]: WARNING: CGXDisplayDidSetRefreshRate
Oct 20 04:15:22 macbook com.apple.xpc.launchd[1]: Service exited with abnormal code: 1 - Critical failure
Oct 20 04:20:01 macbook kernel[0]: USB device disconnected unexpectedly
Oct 20 04:25:10 macbook sysmond[45]: Disk space warning threshold reached
Oct 20 04:30:00 macbook kernel[0]: CORETRANSPORT: Fatal hardware exception - CRITICAL ERROR
"""

def setup_mock_log():
    if not os.path.exists("system_errors.log"):
        with open("system_errors.log", "w") as f:
            f.write(SAMPLE_SYSTEM_LOG.strip())

def triage_logs(log_file="system_errors.log"):
    setup_mock_log()
    print(f"[*] Triage analyzing: {log_file}")
    
    error_keywords = ["error", "critical", "abnormal", "fatal"]
    triage_results = []

    with open(log_file, "r") as f:
        for line_num, line in enumerate(f, 1):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in error_keywords):
                triage_results.append((line_num, line.strip()))

    print("\n--- SYSTEM ERROR & CRASH TRIAGE REPORT ---")
    print(f"{'Line':<6} | {'Event Details'}")
    print("-" * 60)
    for line_num, text in triage_results:
        print(f"{line_num:<6} | {text}")

    with open("triage_report.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Line Number", "Log Message"])
        writer.writerows(triage_results)
    print(f"\n[+] Triage report exported with {len(triage_results)} critical/error entries.")

if __name__ == "__main__":
    triage_logs()
