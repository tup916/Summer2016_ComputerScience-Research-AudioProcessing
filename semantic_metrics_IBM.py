
#Author: Tushita Patel
#June, 2016
#Human Computer Interaction Lab
#Department of Computer Science
#University of Saskatchewan

#Semantic Metrics

#imports
import speech_recognition as sr

#input .wav file to be transcribed from the user
#the file should be located at the same folder as this code
fileName = input('Enter the name of the file in the same directory as this script: ')

# obtain path to fileName in the same folder as this script
from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), fileName)

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source) # read the entire audio file

# recognize speech using IBM Speech to Text
IBM_USERNAME = "a3fdd0fd-2b3d-46f4-9269-bfca54b7ecef" # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
IBM_PASSWORD = "PLC2gBqvVaJu" # IBM Speech to Text passwords are mixed-case alphanumeric strings
try:
    print("IBM Speech to Text thinks you said: \n" + r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD))
except sr.UnknownValueError:
    print("IBM Speech to Text could not understand audio")
except sr.RequestError as e:
    print("Could not request results from IBM Speech to Text service; {0}".format(e))


