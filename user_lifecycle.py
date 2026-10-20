import csv
import os
import logging
from datetime import datetime

logging.basicConfig(filename="lifecycle_audit.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def onboard_user(username, department, manager):
    home_dir = os.path.join(os.getcwd(), "mock_enterprise", department, username)
    try:
        os.makedirs(home_dir, exist_ok=True)
        # Simulate creating an account and setting a temp password
        msg = f"SUCCESS: Provisioned account for {username} in {department}. Home dir created at {home_dir}. Manager: {manager}"
        print(msg)
        logging.info(msg)
    except Exception as e:
        print(f"ERROR: Failed to onboard {username}: {e}")
        logging.error(f"Failed to onboard {username}: {e}")

def offboard_user(username):
    msg = f"SUCCESS: Account {username} disabled, moved to 'Disabled_Users' OU, and credentials revoked."
    print(msg)
    logging.info(msg)

def process_roster(csv_file):
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found.")
        return

    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            action = row["Action"].strip().lower()
            username = row["Username"].strip()
            if action == "onboard":
                onboard_user(username, row["Department"], row["Manager"])
            elif action == "offboard":
                offboard_user(username)

if __name__ == "__main__":
    process_roster("users.csv")
