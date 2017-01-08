#Author: Tushita Patel
#June, 2016
#Human Computer Interaction Lab
#Department of Computer Science
#University of Saskatchewan

#Semantic Metrics

#NOTE: IMPORTANT:
#THIS PIECE OF CODE ONLY TRANSCRIBES THE FIRST FEW SENTENCES OF THE SPEAKER IN THE FILE
#UNTIL THE SPEAKER PAUSES.
#THIS PROBLEM HAS BEEN ADDRESSED TO MICROSOFT VIA Msdf forums.
#Link: https://social.msdn.microsoft.com/Forums/azure/en-US/1e78d891-02ca-4bca-ba68-42f0ee13be40/speech-to-text-incomplete?forum=mlapi 


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

# recognize speech using Microsoft Bing Voice Recognition
BING_KEY = "" #"a2c50164d4d74b979547db64e6c4eb79" # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
try:
    print("Microsoft Bing Voice Recognition thinks you said: \n" + r.recognize_bing(audio, key=BING_KEY))
except sr.UnknownValueError:
    print("Microsoft Bing Voice Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
