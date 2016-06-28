
#Author: Tushita Patel
#June, 2016
#Human Computer Interaction Lab
#Department of Computer Science
#University of Saskatchewan

#Semantic Metrics

#NOTE:
#Sphinx IS NOT VERY ACCURATE WITH THE TRANSCRIPTIONS. 10-15%

#imports
import speech_recognition as sr

#input .wav file to be transcribed from the user
#the file should be located at the same folder as this code
fileName = input('Enter the name of the .wav file in the same directory as this script: ')

# obtain path to fileName in the same folder as this script
from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), fileName)

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source) # read the entire audio file

# recognize speech using Sphinx
try:
    print("Sphinx thinks you said: \n" + r.recognize_sphinx(audio))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))
