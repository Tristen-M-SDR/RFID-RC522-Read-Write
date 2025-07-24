import MFRC522
import signal
import json
import os

continue_reading = True

# Path to the JSON file with authorized UIDs
AUTHORIZED_UIDS_FILE = "authorized_uids.json"

# Convert UID list to hex string
def uid_to_string(uid):
    return ''.join(format(x, '02X') for x in uid)

# Load authorized UIDs from file
def load_authorized_uids():
    if os.path.exists(AUTHORIZED_UIDS_FILE):
        with open(AUTHORIZED_UIDS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Warning: UID list file is corrupted. Starting with empty list.")
                return []
    return []

# Save authorized UIDs to file
def save_authorized_uids(uids):
    with open(AUTHORIZED_UIDS_FILE, "w") as file:
        json.dump(uids, file, indent=2)

# Function to cleanly exit on Ctrl+C
def end_read(signal, frame):
    global continue_reading
    print("\nCtrl+C captured, ending read.")
    continue_reading = False

# Set up signal capture
signal.signal(signal.SIGINT, end_read)

# Init RFID reader
MIFAREReader = MFRC522.MFRC522()
authorized_uids = load_authorized_uids()

print("RFID Access Control System")
print("Waiting for RFID tag. Press Ctrl-C to exit.")

# Main loop
while continue_reading:
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    if status == MIFAREReader.MI_OK:
        print("Tag detected. Attempting to read...")

        (status, uid) = MIFAREReader.MFRC522_SelectTagSN()

        if status == MIFAREReader.MI_OK:
            uid_str = uid_to_string(uid)
            print(f"Card UID: {uid_str}")

            if uid_str in authorized_uids:
                print("Access Granted.\n")
            else:
                print("Access Denied.\n")
        else:
            print("Could not read UID.\n")
