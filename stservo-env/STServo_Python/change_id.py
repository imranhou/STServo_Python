#!/usr/bin/env python

import sys
import os

def print_help_and_exit():
    print("Usage: python change_id.py <current_STS_ID> <new_STS_ID>")
    print("Both CURRENT_STS_ID and NEW_STS_ID must be integers between 1 and 254 and must not be the same.")
    sys.exit(1)

# Check command line arguments
if len(sys.argv) != 3:
    print_help_and_exit()

try:
    CURRENT_STS_ID = int(sys.argv[1])
    NEW_STS_ID = int(sys.argv[2])
except ValueError:
    print_help_and_exit()

if not (1 <= CURRENT_STS_ID <= 254) or not (1 <= NEW_STS_ID <= 254) or CURRENT_STS_ID == NEW_STS_ID:
    print_help_and_exit()

BAUDRATE = 1000000
DEVICENAME = "COM5"  # Adjust this based on your system

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

sys.path.append("..")
from STservo_sdk import *  # Uses STServo SDK library

# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
packetHandler = sts(portHandler)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Try to change the ID

print("Changing from ID:%02d to ID:%02d." %(CURRENT_STS_ID, NEW_STS_ID))
sts_comm_result, sts_error = packetHandler.changeId(CURRENT_STS_ID, NEW_STS_ID)
if sts_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(sts_comm_result))
else:
    print("[ID:%03d] change id to [ID:%03d] Succeeded." % (CURRENT_STS_ID, NEW_STS_ID))
if sts_error != 0:
    print("%s" % packetHandler.getRxPacketError(sts_error))

# Close port
portHandler.closePort()
