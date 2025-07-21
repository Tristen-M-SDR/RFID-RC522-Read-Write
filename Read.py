#!/usr/bin/env python3
# -*- coding: utf8 -*-

import MFRC522
import signal

continue_reading = True

# Convert UID to string
def uidToString(uid):
    return ''.join(format(i, '02X') for i in uid)

# Convert list of integers to hex string
def dataToHexString(data):
    return ' '.join(format(i, '02X') for i in data)

# SIGINT handler
def end_read(signal, frame):
    global continue_reading
    print("\nCtrl+C captured, ending read.")
    continue_reading = False

# Hook SIGINT
signal.signal(signal.SIGINT, end_read)

# Init reader
MIFAREReader = MFRC522.MFRC522()

print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

while continue_reading:
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    if status == MIFAREReader.MI_OK:
        print("Card detected")

        (status, uid) = MIFAREReader.MFRC522_SelectTagSN()
        if status == MIFAREReader.MI_OK:
            print("Card UID: %s" % uidToString(uid))

            # Authenticate with default key for sector 8 (block 8)
            key = [0xFF]*6
            block = 8
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block, key, uid)

            if status == MIFAREReader.MI_OK:
                # Read block 8
                recvData = []
                recvData.append(MIFAREReader.PICC_READ)
                recvData.append(block)
                crc = MIFAREReader.CalulateCRC(recvData)
                recvData += crc
                (status, backData, backLen) = MIFAREReader.MFRC522_ToCard(MIFAREReader.PCD_TRANSCEIVE, recvData)

                if status == MIFAREReader.MI_OK and backData:
                    print("Raw block %d data:" % block, backData)
                    print("Hex block %d data:" % block, dataToHexString(backData))

                    try:
                        decoded_text = bytearray(backData).decode('utf-8').rstrip('\x00')
                        print("Decoded text:", decoded_text)
                    except UnicodeDecodeError:
                        print("Could not decode block data as UTF-8.")
                else:
                    print("Failed to read block %d" % block)
                MIFAREReader.MFRC522_StopCrypto1()
            else:
                print("Authentication error")
