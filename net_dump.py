import subprocess
import platform
import datetime

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return result.stdout if result.returncode == 0 else f"Error running command: {result.stderr}"
    except Exception as e:
        return f"Exception: {str(e)}"

def export_netdump():
    current_os = platform.system()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"netdump_report_{timestamp}.txt"
    
    print(f"[*] Gathering network diagnostic snapshot for {current_os}...")

    netstat_cmd = ["netstat", "-rn"] if current_os in ["Darwin", "Linux"] else ["route", "print"]
    interface_cmd = ["ifconfig"] if current_os in ["Darwin", "Linux"] else ["ipconfig", "/all"]

    routing_table = run_command(netstat_cmd)
    interfaces = run_command(interface_cmd)

    report_content = f"""=== NETWORK DIAGNOSTIC SNAPSHOT (NETDUMP) ===
Timestamp: {datetime.datetime.now()}
Operating System: {current_os}

[1] ROUTING TABLE ({' '.join(netstat_cmd)})
{routing_table}

[2] INTERFACE CONFIGURATION ({' '.join(interface_cmd)})
{interfaces}
"""

    with open(report_filename, "w") as f:
        f.write(report_content)

    print(f"[+] NetDump bundle successfully exported to: {report_filename}")

if __name__ == "__main__":
    export_netdump()
