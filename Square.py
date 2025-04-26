import serial
import time

# Establish serial connection with the MEMS controller
ser = serial.Serial('/dev/tty.usbserial-AQ01HXI0', 115200, timeout=1)

# Enable MEMS driver
ser.write(b'MTI+EnableDevice\n')
time.sleep(1)  # Allow time for initialization

# Define square corner positions
square_positions = [
    (0.50,  0.50),  # Top-right
    (-0.50,  0.50), # Top-left
    (-0.50, -0.50), # Bottom-left
    (0.50, -0.50),  # Bottom-right
    (0.50,  0.50)   # Back to start
]

# Repeat the square pattern multiple times
for _ in range(10):  # Change the number for more repetitions
    for x, y in square_positions:
        command = f"MTI+GoToDevicePosition {x:.2f} {y:.2f} 255\n"
        print(f"Sending command: {command.strip()}")  # Debug output
        ser.write(command.encode())  # Send command
        time.sleep(0.5)  # Delay for movement

# Disable MEMS driver after completing the pattern
ser.write(b'MTI+DisableDevice\n')
ser.close()