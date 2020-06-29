
import sys
import datetime
import time
import operator
import collections
import numpy as np
import matplotlib.pyplot as mplot
import matplotlib.mlab as mlab

#Variable declaration
sendingCount ={}
receivingCount = {}
sortedSendingCount = {}
sortedReceivingCount = {}
topSender = {}


with open(sys.argv[1],"r") as inputfile:
    for line in inputfile:
        items = line.replace('"','').split(",")
        if len(items) == 6:
            timeD,ID,sender,receiver,topic,mode = items
            listOfreceiver = receiver.split("|")
            if not sendingCount.has_key(sender):
                sendingCount[sender] = len(listOfreceiver)
            else:
                sendingCount[sender] = sendingCount[sender] + len(listOfreceiver)
            for listOfrec in listOfreceiver:
                if not receivingCount.has_key(listOfrec):
                    receivingCount[listOfrec] = 1
                else:
                    receivingCount[listOfrec] = receivingCount[listOfrec] + 1
                    
#Sorting the date based on email sent
sortedSendingCount = sorted(sendingCount.items(), key = lambda t: t[1], reverse=True)
sortedReceivingCount = sorted(receivingCount.items(), key = lambda t: t[1], reverse=True)

#Writing into the file named sent_received_email.csv
outputFile = open("sent_received_email.txt", "a")
outputFile.write("person")
outputFile.write(",")
outputFile.write("sent")
outputFile.write(",")
outputFile.write("received")
outputFile.write("\n");
for key,value in sortedSendingCount:    
    outputFile.write(key)
    outputFile.write(",")
    outputFile.write(str(value))
    outputFile.write(",")
    if receivingCount.has_key(key):
        outputFile.write(str(receivingCount.get(key)))
    else:
        outputFile.write("0")
    outputFile.write("\n")
for key, value in sortedReceivingCount:
    if not sendingCount.has_key(key):
        outputFile.write(key)
        outputFile.write(",")
        outputFile.write("0")
        outputFile.write(",")
        outputFile.write(str(value))
        outputFile.write(",")
        outputFile.write("\n")


#Get the top N person based on email sent
topN = 5
counter = 0
while (counter < topN and counter < len(sortedSendingCount)):
    key = sortedSendingCount[counter][0]
    topSender[key] = 1
    counter += 1
    
#Analyzing the email count over time for the top 5 person in terms of message sent
SenderCountOverTime = {}
yearHafly = collections.OrderedDict()
yearHafly = {'f1998':0,'s1998':1,'f1999':2,'s1999':3,'f2000':4,'s2000':5,'f2001':6,'s2001':7,'f2002':8,'s2002':9}
with open(sys.argv[1],"r") as inputfile:
    for line in inputfile:
        items = line.replace('"','').split(",")
        if len(items) == 6:
            timeSend,ID,sender,receiver,topic,mode = items
            if topSender.has_key(sender):
                listOfreceiver = receiver.split("|")
                countOverTime = {}
                formatTime = time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(float(timeSend)/1000))
                month,day,yearandtime = formatTime.split("/")
                year, exactTime = yearandtime.split(" ")
                if int(month) < 6:
                    haflyCount =  str("f") + str(year)
                else:
                    haflyCount =  str("s") + str(year)
                index = yearHafly.get(haflyCount)
                if not SenderCountOverTime.has_key(sender):
                    templist = [0,0,0,0,0,0,0,0,0,0]
                    templist[index] = len(listOfreceiver)
                    SenderCountOverTime[sender] = templist[:]
                else:   
                    templist[index] = SenderCountOverTime[sender][index] + len(listOfreceiver)                    
                    SenderCountOverTime[sender] = templist[:]

#Analyzing the received unique email/person name count over time for the 5 person
trackingunique = {}
uniqueReceivedCountOverTime = {}
with open(sys.argv[1],"r") as inputfile:
    for line in inputfile:
        items = line.replace('"','').split(",")
        if len(items) == 6:
            timeSend,ID,sender,receiver,topic,mode = items 
            formatTime = time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(float(timeSend)/1000.))
      
            month,day,yearandtime = formatTime.split("/")
            year, exactTime = yearandtime.split(" ")
            countreceiver = 0
            listOfreceiver = receiver.split("|")
            if int(month) < 6:
                haflyCount =  str("f") + str(year)
            else:
                haflyCount =  str("s") + str(year)
            index = yearHafly.get(haflyCount)
            while countreceiver < len(listOfreceiver):
                preceiver = listOfreceiver[countreceiver]
                if topSender.has_key(preceiver):
                    timeAndSender = str(preceiver) + str(sender) + str(haflyCount)
                    if not trackingunique.has_key(timeAndSender):
                        trackingunique[timeAndSender] = 1                     
                        if not uniqueReceivedCountOverTime.has_key(preceiver):
                            tempor = [0,0,0,0,0,0,0,0,0,0]
                            tempor[index] = 1
                            uniqueReceivedCountOverTime[preceiver] = tempor
                        else:
                            uniqueReceivedCountOverTime[preceiver][index] += 1
                    else:
                        trackingunique[timeAndSender] = 1
                countreceiver += 1


#Xaxis - shows the duration hafly(six months)
xAxisName = ['1998-1','1998-2','1999-1','1999-2','2000-1','2000-2','2001-1','2001-2','2002-1','2002-2']

#Get the person name, duration and email count
send = SenderCountOverTime.keys()
sendCount = SenderCountOverTime.values()
received = uniqueReceivedCountOverTime.keys()
receivedCount = uniqueReceivedCountOverTime.values()


#Show in image
receivingFigure = mplot.figure("Unique Email Receiving Count For Each Six Months")
mplot.figure(1, figsize = (8.5,11))
axes = mplot.gca()
axes.set_xlim([-2,11])
axes.set_ylim([-2,300])
yticks = np.arange(-2, 300, 10)
mplot.xticks(range(10), xAxisName)
mplot.yticks(yticks)
mplot.plot(range(10), receivedCount[0], 'b-', label = received[0])
mplot.plot(range(10), receivedCount[1], 'r-', label = received[1])
mplot.plot(range(10), receivedCount[2], 'g-', label = received[2])
mplot.plot(range(10), receivedCount[3], 'y-', label = received[3])
mplot.plot(range(10), receivedCount[4], 'm-', label = received[4])
mplot.legend()
mplot.xlabel('Duration(Six Months)')
mplot.ylabel('Receiving Count')

sendingFigure = mplot.figure("Sending Email Count For Each Six Months")
axes = mplot.gca()
axes.set_xlim([-2,11])
axes.set_ylim([-2,7500])
yticks = np.arange(-2, 7500, 1000)
mplot.xticks(range(10), xAxisName)
mplot.yticks(yticks)
mplot.plot(range(10), sendCount[0], 'b-', label = send[0])
mplot.plot(range(10), sendCount[1], 'r-', label = send[1])
mplot.plot(range(10), sendCount[2], 'g-', label = send[2])
mplot.plot(range(10), sendCount[3], 'y-', label = send[3])
mplot.plot(range(10), sendCount[4], 'm-', label = send[4])
mplot.legend()
mplot.xlabel('Duration(Six Months)')
mplot.ylabel('Sending Count')

#Saving the image file
receivingFigure.savefig("Unique Email Receiving Count For Each Six Months", dpi=1000)
sendingFigure.savefig("Sending Email Count For Each Six Months", dpi=1000)
receivingFigure.show()
sendingFigure.show()
