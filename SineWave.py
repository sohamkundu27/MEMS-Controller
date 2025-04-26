import serial
import time
import math

# make serial connection with the MEMS controller
ser = serial.Serial('/dev/tty.usbserial-AQ01HXI0', 115200, timeout=1)

# Enable MEMS driver
ser.write(b'MTI+EnableDevice\n')
time.sleep(3)  # allow time for initialization

# Sine wave info
amplitude = 0.5 # Max change from center (range: -1.0 to 1.0)
frequency = 1          # Hz
points_per_cycle = 100 # points per sine wave cycle
cycles = 10            # Number of sine wave cycles

# Generate and send sine wave positions
for i in range(points_per_cycle * cycles):
    #calculate the current angle in radians
    angle = (2 * math.pi * frequency * i) / points_per_cycle

    # sine wave for X-axis, constant Y-axis (centered)
    x = amplitude * math.sin(angle)
    y = 0.0  # this makes a horizontal sine wave

    command = f"MTI+GoToDevicePosition {x:.2f} {y:.2f} 255\n"
    print(f"Sending command: {command.strip()}")  # print position for tracking

    # Send the command to controller
    ser.write(command.encode())
    
    # Adjust delay to control speed
    time.sleep(0.01)

# Disable MEMS driver after the sine wave is complete
ser.write(b'MTI+DisableDevice\n')
ser.close()
