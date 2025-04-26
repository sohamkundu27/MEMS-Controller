import serial
import time
import math

#here we make the serial connection with the MEMS controller
ser = serial.Serial('/dev/tty.usbserial-AQ01HXI0', 115200, timeout=1)

#enable MEMS driver
ser.write(b'MTI+EnableDevice\n')
time.sleep(1)  # Allow time for initialization

# U pattern parameters
amplitude_x = 0.3   # width of the "U" shape
amplitude_y = 0.5   #  height of the "U" shape
points_per_arc = 100     # Number of points per arc (higher = smoother curve)
points_per_line = 20     # Number of points for the connecting lines
cycles = 5               

# make and send connected U and ∩ patterns
for cycle in range(cycles):
    # Starting position of the U
    start_x = amplitude_x
    end_x = -amplitude_x

    # For even cycles: Draw a "U" shape (semi-circle opening upwards)
    if cycle % 2 == 0:
        # Draw the U
        for i in range(points_per_arc + 1):
            angle = math.pi * i / points_per_arc  #0 to π for semi-circle
            x = amplitude_x * math.cos(angle)
            y = -amplitude_y * math.sin(angle)    # Arc opens upward ("U")

            command = f"MTI+GoToDevicePosition {x:.2f} {y:.2f}\n"
            print(f"Sending command: {command.strip()}") #print position
            ser.write(command.encode())
            time.sleep(0.01)

        # connecting line
        for j in range(points_per_line + 1):
            x = end_x + (2 * amplitude_x * j / points_per_line)
            y = 0.0  # Keep it flat at the bottom

            command = f"MTI+GoToDevicePosition {x:.2f} {y:.2f}\n"
            print(f"Sending command: {command.strip()}")
            ser.write(command.encode())
            time.sleep(0.01)

    # semi circle that opens downwards
    else:
        # Draw the arc
        for i in range(points_per_arc + 1):
            angle = math.pi * i / points_per_arc  # 0 to π for semi-circle
            x = amplitude_x * math.cos(angle)
            y = amplitude_y * math.sin(angle)     # Arc opens downward ("∩")

            command = f"MTI+GoToDevicePosition {x:.2f} {y:.2f} \n"
            print(f"Sending command: {command.strip()}")
            ser.write(command.encode())
            time.sleep(0.01)

        #Draw connecting line 
        for j in range(points_per_line + 1):
            x = start_x - (2 * amplitude_x * j / points_per_line)
            y = 0.0  # Keep it flat at the bottom horizontally

            command = f"MTI+GoToDevicePosition {x:.2f} {y:.2f}\n"
            print(f"Sending command: {command.strip()}")
            ser.write(command.encode())
            time.sleep(0.01)

#Disable MEMS driver 
ser.write(b'MTI+DisableDevice\n')
ser.close()
