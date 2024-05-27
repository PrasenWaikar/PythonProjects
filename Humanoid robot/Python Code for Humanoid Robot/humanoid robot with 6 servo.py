import speech_recognition as sr
import pyfirmata
import time
 
# Set up the Arduino board
board = pyfirmata.Arduino('COM7')  # Change this to match your port
 
# Define servo pins
servo_pins = [8,9,10,11,12,13]
servos = [board.get_pin('d:{}:s'.format(pin)) for pin in servo_pins]
 
#pin 8 for neck
#pin 9 for hip
#pin 10 for right hand
#pin 11 for right shoulder
#pin 12 for left hand
#pin 13 for left shoulder
 
# Function to control servo angle
def set_servo_angles(angles):
    for servo, angle in zip(servos, angles):
        servo.write(angle)
    time.sleep(0.1)
# Function to initialize servo positions
def initialize_servos():
    set_servo_angles([80, 81, 0, 0, 180, 0])
 
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
        print("Try to Speak Again …")
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
            set_servo_angles([51, 51, 0, 0, 0, 180])
        elif 'turn left' in command:
            set_servo_angles([111, 111, 
                              0, 0, 0, 180])
        elif 'assemble' in command:
            set_servo_angles([80, 81, 0, 0, 180, 0])
        elif 'hello' in command:
            set_servo_angles([90, 81, 0, 90, 180, 180])
        elif 'hand' in command:
            set_servo_angles([90, 81, 90, 0, 180, 180])
        elif 'hd' in command:
            set_servo_angles([90, 81, 0, 0, 180, 180])
        elif 'rh' in command:
            set_servo_angles([90, 81, 90, 0, 180, 180])
        elif 'rd' in command:
            set_servo_angles([90, 81, 0, 0, 180, 180])
        elif 'lh' in command:
            set_servo_angles([90, 81, 0, 0, 90, 180])
        elif 'ld' in command:
            set_servo_angles([90, 81, 0, 0, 180, 180])
        elif 'walk' in command:
            for i in range(0, 5):
                set_servo_angles([0, 0, 0, 90, 0, 90]),
                set_servo_angles([0, 0, 0, 0, 0, 0])
                break
        elif 'exit' in command:
            break
