import platform
import psutil
import json
from datetime import datetime

def get_system_inventory():
    # Gather Disk info
    disk = psutil.disk_usage('/')
    
    # Gather Network info
    net_ifrs = psutil.net_if_addrs()
    ip_address = "Not Found"
    for interface, addrs in net_ifrs.items():
        for addr in addrs:
            if addr.family == 2 and not addr.address.startswith("127."): # IPv4
                ip_address = addr.address
                break

    inventory = {
        "audit_timestamp": str(datetime.now()),
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "hostname": platform.node(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "ram_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
        "disk_total_gb": round(disk.total / (1024**3), 2),
        "disk_free_gb": round(disk.free / (1024**3), 2),
        "primary_ipv4": ip_address
    }

    return inventory

if __name__ == "__main__":
    data = get_system_inventory()
    print(json.dumps(data, indent=4))
    
    with open("endpoint_audit_report.json", "w") as f:
        json.dump(data, f, indent=4)
    print("\nReport saved to endpoint_audit_report.json")
