# Python program to translate
# speech to text and text to speech


import speech_recognition as sr
import pyttsx3
from playsound import playsound
import webbrowser
import platform
import os
import time as tm
import datetime
import openai
from bs4 import BeautifulSoup
import requests
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

openai.api_key = "please enter api key here"
model_engine = "gpt-3.5-turbo"

def ask_chatgpt(question):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        n=1,
        messages=[
            {"role": "system", "content": "You are a helpful assistant with exciting, interesting things to say."},
            {"role": "user", "content": question},
        ])

    message = response.choices[0]['message']
    return message['content']


# Function to convert text to
# speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init('nsss')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[15].id)  # changing index, changes voices. 1 for female
    engine.setProperty('rate', 110)  # setting up new voice rate
    engine.say(command)
    engine.runAndWait()


def doTask(MyText):
    if 'open' in MyText:
        if 'chrome' in MyText:
            SpeakText("Opening Chrome")
            user_OS = platform.system()
            chrome_path_windows = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            chrome_path_linux = '/usr/bin/google-chrome %s'
            chrome_path_mac = 'open -a /Applications/Google\ Chrome.app %s'
            chrome_path = ''
            link = 'https://www.google.com'

            if user_OS == 'Windows':
                chrome_path = chrome_path_windows
            elif user_OS == 'Linux':
                chrome_path = chrome_path_linux
            elif user_OS == 'Darwin':
                chrome_path = chrome_path_mac
            elif user_OS == 'Java':
                chrome_path = chrome_path_mac
            else:
                webbrowser.open_new_tab(link)

            webbrowser.get(chrome_path).open_new_tab(link)

        elif 'whatsapp' in MyText:
            SpeakText("Opening Whatsapp")
            os.system("open /Applications/Whatsapp.localized/WhatsApp.app")

        elif 'spotify' in MyText:
            SpeakText("Opening Spotify")
            os.system("open /Applications/Spotify.app")

        elif 'word' in MyText:
            SpeakText("Did you mean Microsoft Word")
            while(True):
                str = listen(1)
                if 'yes' in str[0]:
                    SpeakText("Opening Microsoft Word")
                    os.system("open /Applications/'Microsoft Word.app'")
                    break
                elif 'no' in str[0]:
                    SpeakText("Then please tell what do you mean")
                    break
                elif str[1]:
                    SpeakText("I did not got a response of Yes or No")

    elif 'temperature' in MyText or 'weather' in MyText:
        SpeakText("Please tell the name of the city")

        while True:
            city_data = listen(1)
            if city_data[1] == 0:
                continue
            city = city_data[0]
            city = city+" weather"
            city = city.replace(" ", "+")
            res = requests.get(
                f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',
                headers=headers)
            print("Searching...\n")
            soup = BeautifulSoup(res.text, 'html.parser')
            location = soup.select('#wob_loc')[0].getText().strip()
            time = soup.select('#wob_dts')[0].getText().strip()
            info = soup.select('#wob_dc')[0].getText().strip()
            weather = soup.select('#wob_tm')[0].getText().strip()
            print(f"Temperature of {city_data[0]} on {time} is {weather} °C with {info}.")
            SpeakText(f"Temperature of {city_data[0]} on {time} is {weather} °C with {info}.")
            break

    elif 'date' in MyText:
        print(datetime.date.today().strftime('%A %d %B %Y'))
        SpeakText(datetime.date.today().strftime('%A %d %B %Y'))

    elif 'time' in MyText:
        curr_time = tm.strftime("%H:%M:%S", tm.localtime())
        print(f"Current Time is : {curr_time}")
        SpeakText(f"Current Time is : {curr_time}")

    elif 'exit' in MyText:
        SpeakText("Are you sure you want to exit. Please answer in Yes or No!")
        while True:
            ext = listen(1)
            if ext[1] == 0:
                continue
            if 'yes' in ext[0]:
                exit(0)
            elif 'no' in ext[0]:
                break
            elif ext[1]:
                SpeakText("Please answer Yes or No")
    else:
        while True:
            try:
                x = ask_chatgpt(MyText)
                print(x)
                SpeakText(x)
                break
            except Exception as e:
                print("Error asking ChatGPT", e)

def listen(flag):
    lst = []
    # Initialize the recognizer
    r = sr.Recognizer()
    with sr.Microphone() as source2:
        try:
            # use the microphone as source for input.

            # for playing note.wav file
            if flag:
                playsound('sound.mp3')


            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.1)

            # listens for the user's input
            print("listening ...")
            audio2 = r.listen(source2)

            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            print("Did you say ", MyText)
            lst.append(MyText)
            flag = 1
            lst.append(flag)
            # SpeakText(MyText)

        except sr.RequestError as e:
            flag = 0
            lst.append(" ")
            lst.append(flag)
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            flag = 0
            lst.append(" ")
            lst.append(flag)
            print("Nothing to say")
        return lst

if __name__ == '__main__':
    SpeakText("Hello, I am KITT! powered with ChatGPT. How can I help you?")
    lst = listen(1)
    while(True):
        if lst[1]:
            doTask(lst[0])
        lst = listen(lst[1])

