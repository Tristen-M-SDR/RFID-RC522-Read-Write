import MFRC522
import signal
import json
import os

AUTHORIZED_UIDS_FILE = "authorized_uids.json"
continue_reading = True

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

# Handle Ctrl+C
def end_read(signal, frame):
    global continue_reading
    print("\nCtrl+C captured, exiting...")
    continue_reading = False

signal.signal(signal.SIGINT, end_read)

# Initialize reader
MIFAREReader = MFRC522.MFRC522()
authorized_uids = load_authorized_uids()

print("Place your RFID tag near the reader to add it to the authorized list.")
print("Press Ctrl+C to exit.\n")

while continue_reading:
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    if status == MIFAREReader.MI_OK:
        print("Tag detected.")

        (status, uid) = MIFAREReader.MFRC522_SelectTagSN()
        if status == MIFAREReader.MI_OK:
            uid_str = uid_to_string(uid)
            print(f"Detected UID: {uid_str}")

            if uid_str in authorized_uids:
                print("UID is already authorized.\n")
            else:
                authorized_uids.append(uid_str)
                save_authorized_uids(authorized_uids)
                print("UID added to authorized list.\n")

            break  # Exit after one successful scan
        else:
            print("Failed to read UID.\n")
