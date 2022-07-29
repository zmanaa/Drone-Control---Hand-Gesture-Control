# Import socket module
import socket
from djitellopy import Tello
import cv2
import time


# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 6789

# connect to the server on local computer
host = socket.gethostname()

s.connect((host, port))

tello = Tello()
tello.connect()
print(tello.get_battery())
tello.streamon()

take_off = str(s.recv(1024).decode())

if take_off == "TAKE_OFF_NOW":
    print("TAKEOFF")
    tello.takeoff()

while True:
    operation = str(s.recv(1024).decode())

    if operation == "BACKWARD":
        print(operation)
        tello.move_back(30)
        time.sleep(1)
    elif operation == "FORWARD":
        print(operation)
        tello.move_forward(30)
        time.sleep(1)
    elif operation == "UP":
        print(operation)
        tello.move_up(40)
        time.sleep(1)
    elif operation == "DOWN":
        print(operation)
        tello.move_down(40)
        time.sleep(1)
    elif operation == "YAW":
        print(operation)
        tello.rotate_counter_clockwise(90)
        time.sleep(1)
    elif operation == "LAND":
        print(operation)
        tello.land()
        time.sleep(1)
    elif operation == "None":
        print("No operation founded!")

    # Close the connection with the client


s.close()

