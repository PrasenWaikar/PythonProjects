import pyfirmata2
import speech_recognition as sr
import time

comport = 'COM8'
board = pyfirmata2.Arduino(comport)
servo_pin = 13
servo = board.get_pin('d:13:s')

def get_voice_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=2)  # Adjust for ambient noise for 2 seconds
        print("Listening...")
        audio = r.listen(source, timeout=5)  # Set a timeout for listening
    try:
        command = r.recognize_google(audio, language="en-US", show_all=False)
        print("You said: " + command)
        return command.lower()  # Convert command to lowercase for easier comparison
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return None
    except sr.WaitTimeoutError:
        print("Timeout waiting for audio")
        return None

while True:
    voice_command = get_voice_command()
    if voice_command:
        if "left" in voice_command:
            servo.write(0)
        elif "centre" in voice_command:
            servo.write(90)
        elif "right" in voice_command:
            servo.write(180)
        elif "hello" in voice_command:
            servo.write(180)
            time.sleep(0.5)  # Adjust the delay as needed
            servo.write(90)
            time.sleep(0.5)
            servo.write(0)
            time.sleep(0.5)
            servo.write(90)
            time.sleep(0.5)
            servo.write(180)
        elif "stop" in voice_command:
            break

board.exit()
