import serial
import time

ser = serial.Serial('/dev/tty.usbserial-AQ01HXI0', 115200, timeout=1)

ser.write(b'MTI+EnableDevice\n')
time.sleep(3)  
soham = [
    # S 
    (0.50,  0.50), (0.30, 0.50), (0.20,  0.30), (0.30, 0.10), (0.50, 0.10),
    
    # O 
    (0.70,  0.50), (0.80, 0.40), (0.80,  0.20), (0.70, 0.10), (0.60, 0.20), (0.60, 0.40), (0.70, 0.50),

    # H 
    (0.10,  0.50), (0.10, 0.10), (0.10, 0.30), (0.30, 0.30), (0.30, 0.50), (0.30, 0.10),

    # A 
    (-0.10, 0.10), (-0.20, 0.50), (-0.30, 0.10), (-0.25, 0.30), (-0.15, 0.30),

    # M 
    (-0.50, 0.10), (-0.50, 0.50), (-0.40, 0.30), (-0.30, 0.50), (-0.30, 0.10)
]


for _ in range(3):  
    for x, y in soham:
        command = f"MTI+GoToDevicePosition {x:.2f} {y:.2f} 255\n"
        print(f"Position {command.strip()}")  # print position for tracking
        ser.write(command.encode())  # Send command
        time.sleep(0.2)  #delay here to not make movement instantneous

# After we are done, disable MEMS driver after completing movement
ser.write(b'MTI+DisableDevice\n')
ser.close()
