import eyelid01 as eyelid

datFilename = 'sim.dat'
outFileName = 'simData'

task = 2        # 0=waterfall only,  1 = numbers only  2 = both
drawto = 0      # how many point to draw for each sweep, 0 means all points (sweeplength)
waterfallStartTrial = 1
waterfallEndTrial = 100

Data = []
version, bviFileName, numTrials, sweeplength = eyelid.basicInfo(datFilename)
if drawto == 0 or drawto > sweeplength : drawto = sweeplength
for i in range(0,numTrials): Data.append(eyelid.eyelidTrial(sweeplength))
calib = eyelid.read_bvi(bviFileName,version,Data)
eyelid.read_dat(datFilename,version,numTrials,Data)
eyelid.filterAndNormalize(Data, version, numTrials, sweeplength, calib)
if task > 0: eyelid.doNumbers(Data, version, numTrials, sweeplength, calib,outFileName)
if task != 1: eyelid.waterfall(Data, version, sweeplength, drawto, waterfallStartTrial,waterfallEndTrial)
