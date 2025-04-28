#!/usr/bin/env python

import sys
import os

def print_help_and_exit():
    print("Usage: python ping.py [PING_STS_ID]")
    print("PING_STS_ID must be an integer between 1 and 254. If not provided, defaults to 1.")
    sys.exit(1)

# Parse command line arguments
if len(sys.argv) > 2:
    print_help_and_exit()

if len(sys.argv) == 2:
    try:
        PING_STS_ID = int(sys.argv[1])
    except ValueError:
        print_help_and_exit()

    if not (1 <= PING_STS_ID <= 254):
        print_help_and_exit()
else:
    PING_STS_ID = 1

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

# Try to ping the STServo
sts_model_number, sts_comm_result, sts_error = packetHandler.ping(PING_STS_ID)
if sts_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(sts_comm_result))
else:
    print("[ID:%03d] ping Succeeded. STServo model number : %d" % (PING_STS_ID, sts_model_number))
if sts_error != 0:
    print("%s" % packetHandler.getRxPacketError(sts_error))

# Close port
portHandler.closePort()
