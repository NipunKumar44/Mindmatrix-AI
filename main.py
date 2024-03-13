import speech_recognition as sr
import os
import webbrowser
import openai
from configuration import apikey
import datetime
import random
import numpy as np
import pyttsx3  # Import the pyttsx3 library

engine = pyttsx3.init()  # Initialize the pyttsx3 engine

chatStr = ""

def say(text):
    engine.say(text)
    engine.runAndWait()


def chat(query):
    global chatStr
    openai.api_key = apikey
    print(chatStr)  # Print the current chat history before appending

    # Generate AI response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "system", "content": chatStr}, {"role": "user", "content": query}],
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract AI response
    ai_response = response["choices"][0]["message"]["content"]

    # Say AI response
    say(ai_response)

    # Append both user query and AI response to the chat history
    chatStr += f"text: {query}\n Mindmatrix: {ai_response}\n"

    return ai_response


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text += response["choices"][0]["message"]["content"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}\n")
            return query
        except Exception as e:
            print("Some Error Occurred. Sorry from Mindmatrix")
            return "Some Error Occurred. Sorry from Mindmatrix"

if __name__ == '__main__':
    print('Mindmatrix')
    say("Hello, I am Mindmatrix.")
    chatStr = ""

    while True:
        print("Listening...")
        query = takeCommand().lower()  # Convert query to lower case to improve matching

        # Define sites
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"]]
        for site in sites:
            if f"open {site[0]}".lower() in query:
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                break

        if "open music" in query:
            # Adjust path to your music file
            musicPath = "your_music_path_here"
            os.startfile(musicPath)

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} hours and {min} minutes")

        elif "open [Write any application name]" in query:
            os.system('start "" "Application path goes here"')

        elif "using artificial intelligence" in query:
            response = chat("How can I assist you?")

        elif "Mindmatrix quit" in query:
            say("Goodbye.")
            exit()

        elif "reset chat" in query:
            chatStr = ""

        else:
            print("Chatting...")
            response = chat(query)
