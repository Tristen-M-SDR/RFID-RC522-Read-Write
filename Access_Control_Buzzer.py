import MFRC522
import signal
import json
import os
import time
from gpiozero import PWMOutputDevice

continue_reading = True

# GPIO pin where the piezo buzzer is connected (BCM 17 = Pin 11)
BUZZER_PIN = 17
buzzer = PWMOutputDevice(BUZZER_PIN)

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

# Play tone for "Access Granted" using PWM for louder passive buzzer output
def play_denial_tone():
    buzzer.frequency = 3000  # 3 kHz is often loudest for passive buzzers
    buzzer.value = .5       # 50% duty cycle
    time.sleep(0.3)
    buzzer.value = 0
    time.sleep(0.1)
    buzzer.value = .5
    time.sleep(0.3)
    buzzer.value = 0
    
def play_success_tone():
    buzzer.frequency = 3000  # 3 kHz is often loudest for passive buzzers
    buzzer.value = .5       # 50% duty cycle
    time.sleep(1.25)
    buzzer.value = 0

# Function to cleanly exit on Ctrl+C
def end_read(signal, frame):
    global continue_reading
    print("\nCtrl+C captured, ending read.")
    continue_reading = False
    buzzer.value = 0

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
                play_success_tone()
            else:
                print("Access Denied.\n")
                play_denial_tone()
        else:
            print("Could not read UID.\n")
