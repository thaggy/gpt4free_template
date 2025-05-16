import speech_recognition as sr
import keyboard
import pyttsx3
import os
import re
import g4f

def exit_conditions():
    return keyboard.is_pressed('esc') or keyboard.is_pressed('q')

# Initialize TTS
tts = pyttsx3.init()

# Get TTS Voices 
voices = tts.getProperty('voices')

# Set TTS Properties
tts.setProperty('voice', voices[0].id)
tts.setProperty('voice', 'en-US')
tts.setProperty('volume', 1.0)  
tts.setProperty('rate', 200)  

# How to run TTS
#tts.say('Hello! This is a test')
#tts.runAndWait()

# initalize speech recognition
recognizer = sr.Recognizer()

conversation_history = []

while not exit_conditions():
    
    # Audio recording done with space
    if keyboard.is_pressed('space'):
        
        # Get audio from microphone
        with sr.Microphone() as source:

            # Get audio from user...
            print('Recording input...')
            audio = recognizer.listen(source, phrase_time_limit=100)
        
        try:
            # Parse Audio
            recognized_text = recognizer.recognize_google(audio, language="en-US")
            print('User Recognized Speech : ' + recognized_text)
            
            # Send conversation to Chat GPT
            conversation_history.append({{"role": "user", "content": f"{recognized_text}"}})
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                messages=[conversation_history],
            )

            # TTS Response
            tts.say(response)
            tts.runAndWait()
            conversation_history.append({'role' : 'bot', 'content' : f"{response}"})

        except:
            print('Error Handling Here')