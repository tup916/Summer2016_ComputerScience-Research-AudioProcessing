#Author: Tushita Patel
#June, 2016
#Human Computer Interaction Lab
#Department of Computer Science
#University of Saskatchewan

#Semantics Metrics

#This file takes in a file (audioNames.txt). This txt file contains all the .wav files that need to be transcribed.
#This file must be saved in the same folder as the .wav files and
#the current directory of the terminal should be at this location as well

#What this piece of code does is: for each file, it transcribes and stores the transcription
#in a new txt file with the same name as the .wav file, with the .txt extension, of course.
#Uses IBM Watson's Speech to Text.

#Before using it, make sure to uncomment the line where the variable
#'transcript' is allotted the value of the actual transcription, using the username and password.

#imports
import speech_recognition as sr

#input .wav file to be transcribed from the user
#the file should be located at the same folder as this code
listFilesName = open("audioNames.txt",'r+')

# recognize speech using IBM Speech to Text
IBM_USERNAME = "a3fdd0fd-2b3d-46f4-9269-bfca54b7ecef"
# IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
IBM_PASSWORD = "PLC2gBqvVaJu" # IBM Speech to Text passwords are mixed-case alphanumeric strings

for fileName in listFilesName:
    # obtain path to fileName in the same folder as this script
    from os import path
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), fileName)

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source) # read the entire audio file
    fileName = fileName[0:-6]
    try:
        transcript = "temp transcription"
        #transcript = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
        text_file = open(fileName+".txt", "w")
        text_file.write(transcript)
        text_file.close()
    except sr.UnknownValueError:
        print("IBM Speech to Text could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from IBM Speech to Text service; {0}".format(e))

    print ("Done transcribing ", fileName)

listFilesName.close()
