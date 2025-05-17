import speech_recognition as sr
import keyboard
import pyttsx3
import g4f
import traceback

# Stuff to help with request? Idk doesn't work for me very well on my crappy mac laptop where I did the initial writing for this
# TODO: Test this on my windows machine. My mac doesn't work very well and I don't have docker setup for this yet
if False:
    import os

    os.environ['CURL_CA_BUNDLE'] = ''
    os.environ['REQUESTS_CA_BUNDLE'] = ''

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

# initalize speech recognition
recognizer = sr.Recognizer()

# Set initial premise of AI conversation
system_prompt = "You are a helpful assistant chatbot trained by OpenAI.\
                \nYou answer questions.\nYou are friendly and excited to be able to help the user.\
                \nYou are talking to the user through a chat interface.\nRespond in English."

conversation_history = [{"role": "system", "content": system_prompt}]

# Setup g4f client
client = g4f.Client()

print('Setup complete!')
# Setup conditions to kill the program
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
            conversation_history.append({"role": "user", "content": f"{recognized_text}"})
            chat_completion = client.chat.completions.create(model="gpt-4o-mini", 
                                                            # max_tokens=100, 
                                                            temperature=0.9, 
                                                            top_p=1, 
                                                            top_k=0,
                                                            messages=conversation_history, 
                                                            stream=False)

            # Grab the message content from chat gpt
            response = chat_completion.choices[0].message.content
            print("ChatGPT : " + response)

            # Say message in TTS
            tts.say(response)
            tts.runAndWait()

            # Add it to the conversation history
            conversation_history.append({'role' : 'bot', 'content' : f"{response}"})

        except Exception:
            print('Error handling here')
            traceback.print_exc()