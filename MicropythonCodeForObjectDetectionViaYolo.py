import machine
import network
import urequests as requests
import json
import time

ssid = "F19"
password = "12345678"
serverURL = "http://192.168.172.171:5000/process_command"  # Replace with your Flask server's IP address

MOTOR_1_PIN_1 = 14
MOTOR_1_PIN_2 = 15
MOTOR_2_PIN_1 = 13
MOTOR_2_PIN_2 = 12

def setup():
    print("Connecting to WiFi...")
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, password)

    while not wifi.isconnected():
        pass

    print("Connected to WiFi")

    motor_pins = [MOTOR_1_PIN_1, MOTOR_1_PIN_2, MOTOR_2_PIN_1, MOTOR_2_PIN_2]
    for pin in motor_pins:
        machine.Pin(pin, machine.Pin.OUT)

def send_command(command):
    payload = {"requestFromESP": command}
    payload_str = json.dumps(payload)

    response = requests.post(serverURL, headers={"Content-Type": "application/json"}, data=payload_str)
   
    if response.status_code == 200:
        response_data = response.json()

        if "command" in response_data:
            return response_data["command"]
        else:
            print("Invalid response received from server")
    else:
        print("Error on sending POST request:", response.status_code)

    response.close()
    return None

def motor_action(m1_p1, m1_p2, m2_p1, m2_p2):
    machine.Pin(MOTOR_1_PIN_1, value=m1_p1)
    machine.Pin(MOTOR_1_PIN_2, value=m1_p2)
    machine.Pin(MOTOR_2_PIN_1, value=m2_p1)
    machine.Pin(MOTOR_2_PIN_2, value=m2_p2)

setup()

while True:
    command = send_command("request")
    if command:
        if command == "forward":
            print("Forward")
            motor_action(1, 0, 1, 0)
        elif command == "left":
            print("Left")
            motor_action(0, 1, 1, 0)
        elif command == "right":
            print("Right")
            motor_action(1, 0, 0, 1)
        elif command == "backward":
            print("Backward")
            motor_action(0, 1, 0, 1)
        elif command == "stop":
            print("Stop")
            motor_action(0, 0, 0, 0)
        else:
            print("Invalid command received")
    else:
        print("Failed to get a valid command")

    time.sleep(3)  # Wait for a while before requesting the next command 
