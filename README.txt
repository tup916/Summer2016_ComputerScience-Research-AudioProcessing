#Written by: Tushita Patel
#May/June 2016
#NSERC Summer Research Project for
#Human Computer Interaction Lab
#Department of Computer Science
#University of Saskatchewan
#Supervisor: Dr. Regan Mandryk

My Supervisor asked me not to make the source files public. As a result, I cannot share them with you. Please contact me via email, and I would love to demonstrate them to you.

Abstract: 
Project TITLE: Awkward Silences: Investigating Relational Closeness using Auditory Analysis

DESCRIPTION: 
What makes a conversation awkward or pleasant? Can we computationally abstract information such as awkwardness and other features from recorded audio conversations? This research project is an attempt to extract information about people’s behavioural and emotional experience in one-to-one conversations using three types of metrics- signal metrics: using just the signals in a recorded audio, semantic metrics: transcribing the conversations and lexically calculating the effectiveness of the conversation, emotional speech: using the auditory features such as pitch and speed to infer emotions of the speaker. The extraction of such features in this project can be significantly useful in areas such as psychological and sociological research, speech pathology, quality control in costumer service and health. 
\


This project is to create analysis tools for all the projects that the department has going on in the area of distributed chat. 

Using audio chat as data, where each file has one side of the conversation recorded, I am extracting three types of metrics.
1. Signal Metrics
	Using just the audio, extracting number of features such as:
		-How many conversational turns
		-Average speaking time of participants
		-Average pause time (when a particular participant speaks, then pauses, then resumes to speak)
		-Silence time (when none of the participants are speaking, eg. pause between turns)
		-Relative dominance of one participant

2. Semantic metrics
	Transcribing the conversations
	Using the transcribed data, and automated tools( e.g. LIWC ) to do analysis on things like 
		-the use of personal pronouns, 
		-emotional content of words, etc. 

3. Emotional Speech
	Extracting emotional content form the audio properties of the speech signal, using features such as the speed, timbre, etc.




PART I: SIGNAL METRICS
The most updated file name: signal_stdDev_and_silenceCommonIntervals_V10.py

1. The code is written in Python.
2. Make sure you have the following libraries in python before you run it:
	- numpy
	- soundfile
	- matplotlib.pyplot (Not necessary, but helps in visualization. I have not put code for printing the waves)
3. I have also provided with two audio files of conversations, namely: 57x74_57_1459806354.wav and 57x74_74_1459806354.wav, and a couple more.
4. This only works for .wav files.
5. Make sure you go in and replace the path to the file, based on your downloaded location. This is done in the 20th and 21st line of the source code.
6. The samplerate of both audio files that I have provided are the same. If you are using your own audio files, make sure they have the same samplerate.
	With the files that I have provided, the samplerate is 44.1KHz for both. So this portion has been taken care of.
7. To run the program, type the following in the terminal and wait for a few seconds:
	python [path to the file]/signal_stdDev_and_silenceCommonIntervals_V10.py



