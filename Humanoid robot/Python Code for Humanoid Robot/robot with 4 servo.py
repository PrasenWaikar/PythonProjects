import speech_recognition as sr
import pyfirmata
import time
 
# Set up the Arduino board
board = pyfirmata.Arduino('COM6')  # Change this to match your port
 
# Define servo pins
servo_pins = [6,7,11,3]
servos = [board.get_pin('d:{}:s'.format(pin)) for pin in servo_pins]
led_pins= [8,9]
led = [board.get_pin('d:{}:s'.format(pin)) for pin in led_pins]
#pin 4  for neck
#pin 5 for hip
#pin 3 for right hand
#pin 11 for left hand
 
# Function to control servo angle
def set_servo_angles(angles):
    valid_angles = [min(max(angle, 0), 180) for angle in angles]
    for servo, angle in zip(servos, valid_angles):
        servo.write(angle)
    time.sleep(0.1)
# Function to initialize servo positions
def initialize_servos():
    set_servo_angles([90, 95, 90, 90])
def initialize_led():
    set_led_blink([True, True], 0.5)
 
# Function to recognize voice command
def recognize_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for 1 second
        audio = recognizer.listen(source)
 
    try:
        command = recognizer.recognize_google(audio).lower()
        print("Command:", command)
        return command
    except sr.UnknownValueError:
        print("Try to speak again...!")
        return None
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return None
# Main loop
initialize_servos()
while True:
    command = recognize_command()
    if command:
        if 'turn right' in command:
            set_servo_angles([55, 65, 90, 90])
        elif 'left' in command:
            set_servo_angles([115, 125, 90, 90])
        # elif 'assemble' in command:
        #     set_servo_angles([90, 95, 90, 90])
        elif 'hello' in command:
            set_servo_angles([90, 95, 90, 180])
        elif 'hand' in command:
            set_servo_angles([90, 95, 0, 180])
        elif 'exit' in command:
            break