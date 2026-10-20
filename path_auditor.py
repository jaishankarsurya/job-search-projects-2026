import os
import shutil

ESSENTIAL_TOOLS = ["git", "python3", "curl", "ssh", "pip3"]

def audit_path_directories():
    path_env = os.environ.get("PATH", "")
    directories = path_env.split(os.pathsep)
    
    print("--- PATH DIRECTORY AUDIT ---")
    valid_count = 0
    broken_count = 0

    for directory in directories:
        if not directory:
            continue
        exists = os.path.isdir(directory)
        status = "[VALID]" if exists else "[BROKEN / MISSING]"
        if exists:
            valid_count += 1
        else:
            broken_count += 1
        print(f"{status} : {directory}")

    print(f"\nSummary: {valid_count} valid directory/directories, {broken_count} missing directory/directories found in PATH.\n")

def audit_essential_tools():
    print("--- ESSENTIAL UTILITY AUDIT ---")
    for tool in ESSENTIAL_TOOLS:
        path_found = shutil.which(tool)
        if path_found:
            print(f"[FOUND]     {tool:<10} -> {path_found}")
        else:
            print(f"[MISSING]   {tool:<10} -> Not found on PATH")

if __name__ == "__main__":
    audit_path_directories()
    audit_essential_tools()
