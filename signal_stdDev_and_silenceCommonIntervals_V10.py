#Author: Tushita Patel
#May, 2016
#Human Computer Interaction Lab
#Department of Computer Science
#University of Saskatchewan

#Signal Metrics

#==============================================================
#	      IMPORTS, LAMBDAS AND VARIABLES
#==============================================================

#imports
import numpy
import soundfile as sf
import matplotlib.pyplot as plt

#reading files
# two files for two conversations
data1, samplerate = sf.read('T:57x74_57_1459806354.wav')
data2, samplerate = sf.read('T:57x74_74_1459806354.wav')


#lambdas that I need:

#lambda sum
sum = lambda arg1, arg2: arg1 + arg2

#lambda sample to time
samples_to_time = lambda num_samples: num_samples/samplerate

#lambda percent of silence
percent_silence = lambda num_samples, length_of_data : num_samples / length_of_data

#lambda seconds to minutes
def seconds_to_minutes(seconds):
	return (seconds//60, seconds%60)



#Merge each file into one channel
#Merge the two channels of the first file into one channel
Data1 = []
for i in range(0, len(data1)):
    Data1.append(sum(data1[i][0], data1[i][1]))

#Merge the two channels of the second file into one channel
Data2 = []
for i in range(0, len(data2)):
    Data2.append(sum(data2[i][0], data2[i][1]))


#Merge the two FILES into one file
#For the following questions:
# average pause time
Data = []
for i in range(0, min(len(Data1), len(Data2))):
    Data.append(sum(Data1[i], Data2[i]))


#***************************************************
#===================================================
#===================================================
#		PRINT / PLOTS
#===================================================

#Given a list of intervals of samples, prints the time intervals
def printTimeIntervals(List):
    if (len(List) == 0):
        print ("No pauses in the participant's speech.")
        return;
    print ("[", end = " ")
    for i in range(0, len(List)-1):
        print ("(", (samples_to_time(List[i][0])), ", ", (samples_to_time(List[i][1])), "), ")
    print ("(", (samples_to_time(List[-1][0])), ", ", (samples_to_time(List[-1][1])), ")]")
    return;

#Given a list of intervals of samples, prints the sample intervals and the time intervals
def printDeetsOfOne(List):
    print ("Sample intervals:")
    print (List)
    printTimeIntervals(List)
    print ("\n\n")

#Given a tuple of List of Silence and List of Conversation,
#prints the sample intervals and time intervals of both
def printDeets(List):
    Silence = List[0]
    Convo = List[1]

    print ("===SILENCE===")
    printDeetsOfOne(Silence)

    print ("===CONVERSATION===")
    printDeetsOfOne(Convo)
    
	
#==============================================================
#==============================================================
# 		    SILENCES AND STUFF		
#==============================================================
#==============================================================

#Is this sample a silence?
#We can always change the definition/threshold of silence, 
#if it is something other than <0.25
def isSilence(value):
    if (abs(value) < 0.25):
        return True
    else:
        return False


#Upto what sample numbers is it considered a voice or a small disruption?
#Change this value to change the threshold.
def isDisruption(sample1, sample2):
    return (abs(sample2-sample1) < 22050)

#finds the next sample with a silence
def findNextSilence(d0, sample):
    x = sample + 1
    if (x >= (len(d0))):
        x = -1
    else:
        while ( (x < len(d0)) and (not isSilence(d0[x])) ):
            x = x + 1
        if (x == len(d0)):
            x = -1
    return x


#finds the next sample which is not a silence
def findNextConvo(d0, sample):
    x = sample + 1
    if (x >= (len(d0))):
        x = -1
    else:
        while ((x < len(d0)) and (isSilence(d0[x]))):
            x = x + 1
        if (x == (len(d0))):
            x = -1
    return x


#finds first sample where a convo starts
def findFirstConvo(d0):
    returnedValue = findNextConvo(d0, -1)
    if (returnedValue == -1):
        print("This is not a conversation. Just a silent audio file")
    return returnedValue

#Uses the already perfect Sil list to create a list of Convo
#Regions that are not Silent are regions that are convos
def fillUpConv(d0, Sil):
    Conv = []
    if (Sil[0][0] != 0):
        Conv.append((0, Sil[0][0]))
    for i in range(1, len(Sil)):
        Conv.append(((Sil[i-1][1] + 1), (Sil[i][0] -1)))

    if (Sil[-1][1] != (len(d0) -1)):
        Conv.append((Sil[-1][1], len(d0)-1))
    return Conv

def updateSilence(Silence, Pauses):
    for i in range (0, len(Pauses)):
        Silence.remove(Pauses[i])
    return Silence

# Get rid of backround little disruptions
# Disruption is dependent and could be changed
# by changing the threshold value in the
# isDisruption() function
def getRidOfSmallDisruptions(List):
    ReturnedList = []
    i = 0
    while (i< len(List)-1):
        if (isDisruption(List[i+1][0],List[i][1])):
            #merge the two
            ReturnedList.append((List[i][0], List[i+1][1]))
            i = i+1
        else:
            ReturnedList.append((List[i][0], List[i][1]))
        i = i + 1
    if ((ReturnedList[-1][1] != List[-1][1])):
        ReturnedList.append(List[-1])
    return ReturnedList


# makes silence intervals
# makes conversation intervals
# returns: a tuple of (a) list of silence intervals
#                     (b) list of conversation intervals
def silenceAndConvoInterval(d0):
    CalcSilence = False
    Sil = []
    Conv = []
    firstConvo = findFirstConvo(d0)
    if (firstConvo == -1):
        Sil.append((0, len(d0)-1))
    else:
        if (firstConvo != 0): #audio starts with a Silence
            Sil.append((0, firstConvo))
            
    #now we are all on the samepage, starting to calculate from the conversation
        
        x_cs = firstConvo
        x = x_cs
        while (x!= -1):
            if (CalcSilence == False):
                x_ss = findNextSilence(d0, x)
                #Conv.append((x_cs, x_ss))
                x = x_ss
            else:
                x_cs = findNextConvo(d0, x)
                if ((x_cs - x) > 22050):
                    Sil.append((x, x_cs))
                x = x_cs
            CalcSilence = not CalcSilence
        #print(x, "     ", x_ss, "     ", x_cs)
        Sil.append((x_ss, len(d0)-1))
    if (Sil[-1][1] == -1):
        temp = Sil[-1][0]
        Sil.pop()
        Sil.append((temp, len(d0)-1))
    #printTimeIntervals(Sil)
    Sil = getRidOfSmallDisruptions(Sil)
    Conv = fillUpConv(d0, Sil)
    return ((Sil, Conv))
	
#Does the provided 2d list have the provided integer within the range?
def has(integer, List):
    for i in range (0, len(List)):
        if (List[i][0] <= integer and integer <= List[i][1]):
            return True;
    return False;

def commonSilences(List1, List2):
    List3 = []

    for i in range (0, len(List1)):
        List3.append(List1[i][0])
        List3.append(List1[i][1])


    for i in range (0, len(List2)):
        List3.append(List2[i][0])
        List3.append(List2[i][1])

    List3.sort()    

    i=0
    while (i< len(List3)-1):
        if (List3[i] == List3[i+1]):
            List3.remove(List3[i])
        else:
            i +=1
            
    List4 = []
    for i in range (0, len(List3)):
        if (has(List3[i], List1) and has(List3[i], List2)):
            List4.append(List3[i])

    if (len(List4) %2 == 1):
            print ("Algorithm didn't work. There are odd number of interval candidates.")

    List5 = []
    for i in range (0, len(List4)//2):
        List5.append((List4[i*2], List4[i*2+1]))

    return List5

#====================================================
#====================================================

#----------WORKING WITH THE PROCESSSED DATA----------
#====================================================

#Calculates the total speaking samples for one list of intervals
def TotalSpeakingSamples(Interval):
    sum = 0
    for i in range (0, len(Interval)):
        sum += Interval[i][1] - Interval[i][0]
    return sum

#Given a person's Silences and Convo, returns the
#total speaking time for the person in seconds
# (or in minutes if more than 60 seconds)
#Note: Accepts the entire tuple of Silence and Convo
def TotalSpeakingTime(Person):
    num_samples = TotalSpeakingSamples(Person[1])
    time = samples_to_time(num_samples)
    if (time > 60):
        time = seconds_to_minutes(time)
    return time

#Given two Persons's Silences and Conversations,
# returns in a tuple, the total speaking times of both
def TotalSpeakingTimes(Person1, Person2, show = True):
    if (show):
        SpeakTime1 = TotalSpeakingTime(Person1)
        print("The total speaking time of Participant 1 was: ", SpeakTime1)
        SpeakTime2 = TotalSpeakingTime(Person2)
        print("The total speaking time of Participant 2 was: ", SpeakTime2)
    else:
        SpeakTime1 = TotalSpeakingTime(Person1, "")
        SpeakTime2 = TotalSpeakingTime(Person2, "")
    return (SpeakTime1, SpeakTime2)     

def AveragePauseTime(Person1):
    if (len(Person1[2]) == 0):
            print("There was no pause for this speaker")                
            return 0
    totalPauseSamples = TotalSpeakingSamples(Person1[2])
    avgPauseTime = totalPauseSamples / len(Person1[2])
    return samples_to_time(avgPauseTime)

#Insider function
#Given a List of Intervals of Conversation for a speaker-A,
# and the list of Silence of of the other(speaker-B),
#Calculates and returns the list intervals of pauses for the speaker-A
def calculatePauseIntervals(Silence1, Convo2):
    pause = []
    for i in range (0, len(Convo2)-1):
        for j in range(0, len(Silence1)):
            if (Convo2[i][1] > Silence1[j][0] and Convo2[i+1][0] < Silence1[j][1]):
                pause.append((Convo2[i][1]+1, Convo2[i+1][0]-1))
                break
    return pause

def calculateActualConvoInterval(Convo, PauseInterval):
    conv = []
    if (len(Convo) <=1):
        return;
    count = 0
    i = 0
    while (i< len(Convo)):
        conv.append((Convo[i][0], Convo[i][1]))
        if (count < len(PauseInterval)):
            while (conv[-1][1] == PauseInterval[count][0] - 1):
                tupletemp = conv.pop()
                conv.append((tupletemp[0], Convo[i+1][1]))
                count = count + 1
                i += 1
                if (count >= len(PauseInterval)):
                    break   
        i +=1
    return conv


#Given Silence and Conversational Intervals of two Persons,
# calculates, returns and prints(optional) the Puase Interval times
# for both Persons.
def PauseIntervals(Person1, Person2, show = False):
    Pause2 = calculatePauseIntervals(Person1[0], Person2[1])
    Pause1 = calculatePauseIntervals(Person2[0], Person1[1])
    if (show == True):
        print("Pause Intervals for Person 1:")
        if (len(Pause1) != 0):
            printTimeIntervals(Pause1)
        else:
            print("Person 1 did not pause in their conversations.")
        print("Pause Intervals for Person 2:")
        if (len(Pause2) != 0):
            printTimeIntervals(Pause2)
        else:
            print("Person 2 did not pause in their conversations.")
    return (Pause1, Pause2)


#Calculates and prints which speaker is more dominant
# in terms of the length of their speech, and
# in terms of the number of Conversational turns
# Does not return anything
def Dominance(SpeakTime1, SpeakTime2, numConv1, numConv2):
    print ("The dominating participant (in terms of length of speech) is:", end=" ")
    if (max(SpeakTime1, SpeakTime2) == SpeakTime1):
        print ("Participant 1")
    else:
        print ("Participant 2")

    print ("The dominating participant (in terms of the number of times the person spoke) is:", end=" ")
    if (max(numConv1, numConv2) == numConv1):
        print ("Participant 1")
    else:
        print ("Participant 2")

    return;


#Calculates the standard deviation of a person's speaking time.
def StandardDeviation1(Person):
    miu = TotalSpeakingSamples(Person[1])
    n = len(Person[1])
    miu = miu / n
    
    sum = 0
    for i in range(0, n):
        sum += (miu - (Person[1][i][1] - Person[1][i][0])) * (miu - (Person[1][i][1] - Person[1][i][0]))

    standardDev = pow((sum / (n)), 0.5)
    return samples_to_time(standardDev)

#Uses the python library numpy to calculate the standard deviation of speaking time
def StandardDeviation2(Person):
    Diff = []
    n = len(Person[1])
    for i in range (0, n):
        Diff.append(Person[1][i][1] - Person[1][i][0])

    return samples_to_time(numpy.std(Diff))
        
#=============================================
#=============================================

#--------------- MAIN ------------------------
#=============================================

#Main:

#Initialize: Raw Data --> processed Data
#Person* = (List of Silence Intervals, List of Convo Intervals) <==For now.
Person1 = silenceAndConvoInterval(Data1)

Person2 = silenceAndConvoInterval(Data2)

(PauseInterval1, PauseInterval2) = PauseIntervals(Person1, Person2)
#Person* = (List of Silence Intervals,
           #List of Convo Intervals(including Pause Intervals),
           #List of puase Intervals) <== For now
Person1 = [Person1[0], calculateActualConvoInterval(Person1[1], PauseInterval1), PauseInterval1]
Person2 = [Person2[0], calculateActualConvoInterval(Person2[1], PauseInterval2), PauseInterval2]


#Person* = (List of Silence Intervals(without the pauses),
           #List of Convo Intervals(including Pause Intervals),
           #List of puase Intervals) <== For now
Person1[0] = updateSilence(Person1[0], Person1[2])
Person2[0] = updateSilence(Person2[0], Person2[2])


#Average pause time
    #The same speaker stops speaking and then speaks again
print ("The Average Puase time for Participant1 is: ", AveragePauseTime(Person1))
print ("The Average Puase time for Participant2 is: ", AveragePauseTime(Person2))


#Conversational Turns
print("There were", end = " ")
numConv1 = len(Person1[1])
numConv2 = len(Person2[1])
ConversationalTurns = min(numConv1, numConv2)
print (ConversationalTurns, " conversational turns.")



#Average Speaking time
SpeakTime1, SpeakTime2 = TotalSpeakingTimes(Person1, Person2)
    #Average Speaking time of speaker 1:
AvgSpeakTime1 = SpeakTime1 / numConv1
print ("The Average Speaking Time of Participant 1 is: ", AvgSpeakTime1)
    #Average Speaking time of speaker 2:
AvgSpeakTime2 = SpeakTime2 / numConv2
print ("The Average Speaking Time of Participant 2 is: ", AvgSpeakTime2)

#Standard Deviation of speaking time: calculated two ways
print ("The following is the standard deviation of speaking time.\nParticipant1:", end=" ")
print (StandardDeviation1(Person1), "seconds or using the inbuilt method: ", end=" ")
print (StandardDeviation2(Person1), "seconds.")
print ("Participant2: ", StandardDeviation1(Person2), "seconds or using the inbuilt method: ", end=" ")
print (StandardDeviation2(Person2), "seconds.")

#Dominance of one participant
Dominance(SpeakTime1, SpeakTime2, numConv1, numConv2)

#Silence in the conversation
#Silence in both audios
#(Common silence)
printTimeIntervals(commonSilences(Person1[0], Person2[0]))

print ("*****************************************************")

print ("Silence Intervals of Participant1:")
printTimeIntervals(Person1[0])
print ("Conversational Intervals of Participant1:")
printTimeIntervals(Person1[1])
print ("Pause Intervals of Participant1:")
printTimeIntervals(Person1[2])

print ("*****************************************************")

print ("Silence Intervals of Participant2:")
printTimeIntervals(Person2[0])
print ("Conversational Intervals of Participant2:")
printTimeIntervals(Person2[1])
print ("Pause Intervals of Participant2:")
printTimeIntervals(Person2[2])

print ("*****************************************************")

	
#END of SIGNAL METRICS
