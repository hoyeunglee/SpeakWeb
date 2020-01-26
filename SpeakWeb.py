# Copyright Reserved by Ho Yeung, Lee
# written in 26 Aug 2016
# python -m pip install pyttsx
# python -m pip install SpeechRecognition
# python -m pip install selenium-2.53.6
# python -m pip install PyAudio
# selenium version 2.53.6
# Latest firefox is not supported
# download driver from https://sites.google.com/a/chromium.org/chromedriver/downloads
# unzip and paste the executable driver to C:\Python27\Scripts

from __future__ import division
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import base64
import speech_recognition
import pyttsx

speech_engine = pyttsx.init('sapi5') # see http://pyttsx.readthedocs.org/en/latest/engine.html#pyttsx.init
speech_engine.setProperty('rate', 150)

recognizer = speech_recognition.Recognizer()

def listen():
	with speech_recognition.Microphone() as source:
		recognizer.adjust_for_ambient_noise(source)
		audio = recognizer.listen(source)

	try:
		return recognizer.recognize_google(audio)
		# or: return recognizer.recognize_google(audio) or return recognizer.recognize_sphinx(audio)
	except speech_recognition.UnknownValueError:
		print("Could not understand audio")
	except speech_recognition.RequestError as e:
		print("Recog Error; {0}".format(e))

	return ""


def speak(text):
	speech_engine.say(text)
	speech_engine.runAndWait()

#selenium = webdriver.Firefox()
selenium = webdriver.Chrome()
selenium.get("https://hello.com/login")
username = selenium.find_element_by_id("id_username")
password = selenium.find_element_by_id("id_password")

username.send_keys("")
password.send_keys("")

selenium.find_element_by_css_selector("button.btn").click()
selenium.implicitly_wait(7)

alllinks = selenium.find_elements(By.TAG_NAME, "a");
for alink in alllinks:
    print(alink.text);

#selenium.find_element_by_link_text(alink.text).click();
#selenium.find_element_by_link_text("Instances").click();
#selenium.implicitly_wait(7);

#alltables = selenium.find_elements(By.TAG_NAME, "table");
#table_id = ""
#for atable in alltables:
    #theads = atable.find_elements(By.TAG_NAME, "thead")
    #for thead in theads:
        #heads = thead.find_elements(By.TAG_NAME, "tr")
        #print(len(heads))
        #for head in heads:
            #ths = head.find_elements(By.TAG_NAME, "th")
            #for th in ths:           
                #print(th.text)

while True:
    try:
        commandlink = listen();
        print("you say");
        print(commandlink.lower());
        correct = False
        for alink in alllinks:
            if commandlink.lower() == alink.text.lower():
                correct = True
                selenium.find_element_by_link_text(alink.text).click();
                selenium.implicitly_wait(7)
                alllinks = selenium.find_elements(By.TAG_NAME, "a");
                alltables = selenium.find_elements(By.TAG_NAME, "table");
                table_id = ""
                for atable in alltables:
                    theads = atable.find_elements(By.TAG_NAME, "thead")
                    for thead in theads:
                        heads = thead.find_elements(By.TAG_NAME, "tr")
                        print(len(heads))
                        for head in heads:
                            ths = head.find_elements(By.TAG_NAME, "th")
                            for th in ths:           
                                print(th.text)
                                speak(th.text)
        if correct == False and len(commandlink.lower())>0:
            for alink in alllinks:
                if len(alink.text) > 0:
                    speak(alink.text)
            speak("which link would you like to choose?")
    except:
        print("exception");
