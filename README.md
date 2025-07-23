# RFID-RC522-Read-Write
The following repository allows for Read and Write function using the RFID-RC522 Board

## Start off by plugging in the RFID-RC522 Board to the Raspberry Pi to the following pins:

### Pins
You can use [this](http://i.imgur.com/y7Fnvhq.png) image for reference.

| Name | Pin # | Pin name   |
|:------:|:-------:|:------------:|
| SDA  | 24    | GPIO8      |
| SCK  | 23    | GPIO11     |
| MOSI | 19    | GPIO10     |
| MISO | 21    | GPIO9      |
| IRQ  | None  | None       |
| GND  | Any   | Any Ground |
| RST  | None  | None       |
| 3.3V | 1     | 3V3        |


## Enabling SPI
In the terminal, use the following command to access Raspberry Pi Configuration menu

<pre>
  sudo raspi-config
</pre>

Once the menu is open navigate to **Interface Settings** using the `arrow keys`, `ENTER` to confirm selection, and `ESC` to exit. Enable the **SPI**. 


## Installing the following libraries

<pre>
  sudo apt-get update
  sudo apt install python3-lgpio
  sudo apt-get install python3-pip --break-system-packages
  sudo pip3 install spidev --break-system-packages
  sudo pip3 install MFRC522 --break-system-packages
</pre>

## Setting up the RFID-RC522
**Step 1:** Download and navigate to the files using the following command:

<pre>
  cd Downloads/
  git clone https://github.com/Tristen-M-SDR/RFID-RC522-Read-Write
  cd RFID-RC522-Read-Write
</pre>

**Step 2:** Please run the following command to the Read your current RFID Tag

<pre>
  sudo python3 Read.py
</pre>

From here you can place your RFID Tag or Card near the sensor to read UID and current written data on it.

**Step 3:** Please run the following command to Write to your RFID Tag

<pre>
  sudo python3 Write.py
</pre>

**Step 4:** Please rerun the Read.py using the following command

<pre>
  sudo python3 Read.py
</pre>

