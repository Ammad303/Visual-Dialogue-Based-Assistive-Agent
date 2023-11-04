import machine
import network
import urequests as requests
import json
import time

# WiFi settings
ssid = "F19"
password = "12345678"

# Server settings
serverURL = "http://192.168.172.171:5000/process_command"  # Replace with your Flask server's IP address

# Motor pin configuration
MOTOR_1_PIN_1 = 14  # GPIO 13
MOTOR_1_PIN_2 = 15  # GPIO 12
MOTOR_2_PIN_1 = 13  # GPIO 14
MOTOR_2_PIN_2 = 12  # GPIO 27

def setup():
    print("Connecting to WiFi...")
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, password)

    while not wifi.isconnected():
        pass

    print("Connected to WiFi")

    # Initialize motor pins as outputs
    motor_pins = [MOTOR_1_PIN_1, MOTOR_1_PIN_2, MOTOR_2_PIN_1, MOTOR_2_PIN_2]
    for pin in motor_pins:
        machine.Pin(pin, machine.Pin.OUT)

def motor_action(m1_p1, m1_p2, m2_p1, m2_p2):
    # Set motor pin values for different motor actions
    machine.Pin(MOTOR_1_PIN_1, value=m1_p1)
    machine.Pin(MOTOR_1_PIN_2, value=m1_p2)
    machine.Pin(MOTOR_2_PIN_1, value=m2_p1)
    machine.Pin(MOTOR_2_PIN_2, value=m2_p2)

setup()

while True:
    try:
        command = send_command("request")
        if command:
            if command == "forward":
                print("Forward")
                motor_action(1, 0, 1, 0)  # Adjust pin values for your motor's configuration
            elif command == "left":
                print("Left")
                motor_action(0, 1, 1, 0)  # Adjust pin values for your motor's configuration
            elif command == "right":
                print("Right")
                motor_action(1, 0, 0, 1)  # Adjust pin values for your motor's configuration
            elif command == "backward":
                print("Backward")
                motor_action(0, 1, 0, 1)  # Adjust pin values for your motor's configuration
            elif command == "stop":
                print("Stop")
                motor_action(0, 0, 0, 0)
            else:
                print("Invalid command received")
        else:
            print("Failed to get a valid command")

        time.sleep(3)  # Wait for a while before requesting the next command

    except Exception as e:
        print("Error:", e)
        time.sleep(1)  # Wait before retrying