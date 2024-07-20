import numpy as np
import matplotlib.pyplot as plt
import csv
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class eyelidTrial():
    def __init__(self,sweeplength):
        self.CSduration = 0
        self.USonset = 0
        self.trialName = ""
        self.sweep =  np.zeros(sweeplength,dtype=np.float32)
        self.keeper = 1
        self.CRamp = 0
        self.criterion = 0
        self.onset = 0
        self.maxAmp = 0
        self.isCR = 0

def basicInfo(file):
    filelength = len(file)
    bviFile = file[0:filelength-3]+"bvi"
    f = open(bviFile,'r')
    for i in range(0,6): # version is on the 6th line of bvi file
        line = f.readline() 
        if i == 3:
            temp = line.strip()
            trials = int(temp)
    f.close
    temp = line.strip()
    if temp == "None": 
        vers = "oldBT"
    elif temp =="cbm_sim": 
        vers = "cbm_sim"
    else: 
        vers = "newBT" 
    if vers != "oldBT":
        temp = np.fromfile(file,dtype=np.float32)
    else: 
        temp = np.fromfile(file,dtype=np.int16)
    sweeplength = int(len(temp)/trials)
    return vers, bviFile, trials, sweeplength

def read_bvi(bviFile, version, Data):
        temp = []
        f = open(bviFile,'r')
        while True: 
            line = f.readline() 
            if not line: 
                break 
            temp.append(line)
        f.close
        calib = float(temp[2].strip())
        if version == "cbm_sim":
            lineCount = 0
            trials = 0
            for i in temp:
                x = i.split(",")
                lineCount += 1
                if lineCount > 12:
                    Data[trials].trialName = x[0]
                    Data[trials].CSduration = int(x[1])
                    Data[trials].USonset = int(x[2])
                    trials +=1                
        if version == "newBT":
            lineCount = 0
            trials = 0
            for i in temp:
                x = i.split()
                lineCount += 1
                if x[0]=="Trial":
                    Data[trials].trialName = x[2]
                if x[0]=="AO_0:":
                    Data[trials].CSduration = int(x[3])
                if x[0]=="Ctr_0:":
                    Data[trials].USonset = int(x[2])+200
                    trials +=1  
        return calib

def read_dat(datFile, version, numTrials,cal, Data):
    if version != "oldBT":
        temp = np.fromfile(datFile,dtype=np.float32)
        s = len(temp)
        d = np.reshape(temp,(numTrials,int(s/numTrials)))
        for i in range(0,numTrials):
            Data[i].sweep = d[i,:]
        filterAndNormalize(Data,version,numTrials,cal)
    return

def waterfall(data,version, sweepLength,drawto, startTrial,stopTrial):
    if drawto == 0: drawto = sweepLength
    xSize, ySize = screenInfo()
    fig, ax = plt.subplots()
    ax.set_axis_off()
    windowmanager = plt.get_current_fig_manager()
    screenSize = str(ySize)+"x"+str(ySize)+"+0+0"
    windowmanager.window.wm_geometry(screenSize)
    xoffset = 0
    yoffset = 0
    xjump = int(drawto*.0045)
    sweepnum = stopTrial-startTrial+1
    xoffset = -1*xjump*(stopTrial-startTrial)
    xend = xoffset+drawto
    for i in range(stopTrial-1,startTrial-2,-1):
        if version != "oldBT": trace = np.add(data[i].sweep,(sweepnum*.12))
        xVals = range(xoffset,xend)
        ax.plot(xVals,trace[0:drawto],linewidth=2,color='gray')
        CSoff = int(data[i].CSduration) +200            
        ax.plot(xVals[200:CSoff],trace[200:CSoff],linewidth=2,color='black')
        sweepnum = sweepnum - 1
        xoffset = xoffset + xjump
        xend = xend + xjump
    plt.show()

def filterAndNormalize(data, version, numTrials, cal):
        # if version == "cbm_sim":
            # for trials in range(0,numTrials):
            #     data[trials].sweep = data[trials].sweep * .00085
        if version == "newBT":
            for trials in range(0,numTrials):
                baseline = np.average(data[trials].sweep[0:199])
                data[trials].sweep = data[trials].sweep - baseline
        # temp = np.zeros((2500,t))
        # for trials in range(0,t):
        #     temp[0,trials] = d[0,trials]*1.0
        #     temp[2499,trials]= d[2499,trials]
        #     for bins in range(1,2499):
        #         temp[bins,trials] = temp[bins-1,trials]+(.1*(d[bins,trials]-temp[bins-1,trials]))
        # for trials in range(0,t):
        #     baseline = 0
        #     for bins in range(1,200):
        #         baseline += temp[bins,trials]
        #     baseline = baseline/199.0
        #     for bins in range(0,2500):
        #         temp[bins,trials] -= baseline   # temp is in bits
        #         x = temp[bins,trials]/409.6     # bits/(bits/v) = v
        #         x = x/c                         # v / (mm/v) = mm
        #         temp[bins,trials]=x
        return 

def screenInfo():
    pygame.init()
    info = pygame.display.Info()
    width = info.current_w
    height = info.current_h
    return width, height

def doNumbers(data, version, numTrials, sweeplength, calib,outFile):
    if version == 'cbm_sim':
        for trials in range(0,numTrials):
            sweep = data[trials].sweep
            CSon = 201 #check this when Sean's format confirmed
            data[trials].maxAmp = np.max(sweep[CSon:sweeplength])
            if data[trials].USonset == 0:
                stopper = CSon + data[trials].CSduration #
            else:
                stopper = data[trials].USonset # 
            data[trials].CRamp = np.max(sweep[CSon:stopper])
            if data[trials].CRamp > .3: # it's a CR, so do criterion and latency too
                data[trials].isCR = 1
                for b in range(CSon,stopper):
                    if sweep[b]>.3:
                        data[trials].criterion = (b-200)
                        break
                while sweep[b]>.001:
                    b = b-1
                    if b < 200:
                        print("something went wrong with latency to onset on trial", trials)
                        break
                    data[trials].onset = (b-200)*2
            #print(trials, data[trials].maxAmp,data[trials].CRamp,data[trials].isCR,data[trials].criterion,data[trials].onset)
    with open(outFile+'.csv', 'w', newline='') as csvfile:
        fieldnames = ['TrialName', 'TrialNum', 'Keeper?', 'CR?','Onset','Peak','CRamp','URamp','Criterion','SLamp','maxAmp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for trials in range(0,numTrials):
            #print(trials, data[trials].maxAmp,data[trials].CRamp,data[trials].isCR,data[trials].criterion,data[trials].onset)
            writer.writerow({'TrialName': data[trials].trialName, 'TrialNum': trials+1, 'Keeper?': data[trials].keeper, 'CR?':data[trials].isCR ,'Onset':data[trials].onset ,'Peak': 'N/A','CRamp': data[trials].CRamp,'URamp': 'N/A','Criterion':data[trials].criterion ,'SLamp': 'N/A','maxAmp':data[trials].maxAmp })


