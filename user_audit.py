import pwd
import grp
import platform
import csv

def audit_local_users():
    print("--- LOCAL USER & PRIVILEGE AUDIT ---")
    current_os = platform.system()
    if current_os not in ["Darwin", "Linux"]:
        print("[-] This script currently supports Unix-based systems (macOS/Linux).")
        return

    # Determine admin/sudo group name based on OS
    admin_group_name = "admin" if current_os == "Darwin" else "sudo"
    try:
        admin_group = grp.getgrnam(admin_group_name)
        admin_members = set(admin_group.gr_mem)
    except KeyError:
        admin_members = set()

    print(f"{'Username':<20} | {'UID':<6} | {'Shell':<25} | {'Admin/Sudo?':<12}")
    print("-" * 70)

    user_records = []
    for user in pwd.getpwall():
        # Filter low-level system accounts for cleaner reporting
        if user.pw_uid < 500 and current_os == "Darwin": 
            continue
        if user.pw_uid < 1000 and current_os == "Linux" and user.pw_name != "root": 
            continue

        is_admin = "YES" if (user.pw_name in admin_members or user.pw_uid == 0) else "NO"
        print(f"{user.pw_name:<20} | {user.pw_uid:<6} | {user.pw_shell:<25} | {is_admin:<12}")
        user_records.append([user.pw_name, user.pw_uid, user.pw_shell, is_admin])

    # Export to CSV
    with open("user_privilege_audit.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Username", "UID", "Shell", "Is Admin"])
        writer.writerows(user_records)
    print("\n[+] Audit saved to user_privilege_audit.csv")

if __name__ == "__main__":
    audit_local_users()
