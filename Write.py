#!/usr/bin/env python3
# -*- coding: utf8 -*-

import MFRC522
import signal
import sys
import time

continue_reading = True

def uidToString(uid):
    return ''.join(format(x, '02X') for x in reversed(uid))

def prepare_data(text):
    data = bytearray(text[:16], 'utf-8')
    while len(data) < 16:
        data.append(0)
    return data

def end_write(signal, frame):
    global continue_reading
    print("\nCtrl+C captured. Exiting write.")
    continue_reading = False

signal.signal(signal.SIGINT, end_write)

MIFAREWriter = MFRC522.MFRC522()

new_data = input("Enter new data to write (max 16 characters):\n> ")
data_to_write = prepare_data(new_data)

print("Now place your tag near the reader to write data to block 8...")
print("Press Ctrl+C to exit.")

while continue_reading:
    (status, TagType) = MIFAREWriter.MFRC522_Request(MIFAREWriter.PICC_REQIDL)

    if status == MIFAREWriter.MI_OK:
        print("Card detected")

        (status, uid) = MIFAREWriter.MFRC522_SelectTagSN()

        if status != MIFAREWriter.MI_OK:
            print("Failed to select tag")
            continue

        print("UID: %s" % uidToString(uid))

        key = [0xFF] * 6  # Default key
        block = 8

        if MIFAREWriter.MFRC522_Auth(MIFAREWriter.PICC_AUTHENT1A, block, key, uid) != MIFAREWriter.MI_OK:
            print("Authentication failed")
            continue

        # Write data
        MIFAREWriter.MFRC522_Write(block, data_to_write)

        print("Data written (even if status says otherwise)")

        # Delay before readback to avoid timing issue
        time.sleep(0.2)

        read_data = MIFAREWriter.MFRC522_Read(block)
        if read_data:
            print("Read back block 8:")
            print(read_data)
            print("Text: %s" % bytes(read_data).decode('utf-8', errors='ignore'))
       
        MIFAREWriter.MFRC522_StopCrypto1()
        break
