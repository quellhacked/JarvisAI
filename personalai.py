import cv2
import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import threading

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return ""

# Function to authenticate user using face detection
def authenticate_user():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('Video', frame)

        if len(faces) > 0:  # If a face is detected
            video_capture.release()
            cv2.destroyAllWindows()
            return True

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return False

# Function to handle voice commands
def handle_commands():
    while True:
        command = recognize_speech()
        if "hello" in command.lower():
            speak("Hello! How can I assist you today?")
        elif "exit" in command.lower():
            speak("Goodbye!")
            break

# Function to start the application
def start_application():
    if authenticate_user():
        speak("Authentication successful. Welcome!")
        threading.Thread(target=handle_commands).start()
    else:
        messagebox.showerror("Authentication Failed", "Face not recognized.")

# Create the main application window
app = tk.Tk()
app.title("Jarvis AI")
app.geometry("300x200")

# Create a start button
start_button = tk.Button(app, text="Start Jarvis", command=start_application)
start_button.pack(pady=20)

# Run the application
app.mainloop()