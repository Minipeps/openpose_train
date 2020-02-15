import tqdm
import os
import json
import re
import itertools
import math

import matplotlib.pyplot as plt


jsonFile = "annotations_final_v3.json"
datasetFolder = "../dataset/PigData/"
imgFolder = datasetFolder + "duroc_3stk/RGB/"
valFolder = datasetFolder  + "validation/"

experiment = "pig5_v4"
valJsons = "../training_results/{}/pig/pig_5/scale_1/".format(experiment)

############################################

def squaredDistance(a, b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2

def distance(a, b):
    return math.sqrt( squaredDistance(a, b))

def OKS(gt, dt, s, sigmas):
    oks = 0
    numKeypoints = len(gt)
    for j in range(numKeypoints):
        sd = squaredDistance(gt[j], dt[j])
        k = 2 * sigmas[j]
        oks += math.exp( -sd / (2 * (s**2) * (k**2)) )
    return float(oks) / float(numKeypoints)

############################################

jsons = os.listdir(valJsons)

with open(datasetFolder + jsonFile) as gtFile:
    gtData = json.load(gtFile)

nbIterations = []
nbDetectedAccuracies = []
mOKSAccuracies = []
mAPAccuracies_loose = []
mAPAccuracies_strict = []
mAPAccuracies = []

nbEntitiesGt = sum([ 1 + x['numOtherPeople'] for x in gtData ])

OKS_threshold_loose = 0.5
OKS_threshold_strict = 0.75
OKS_threshold = [ 0.5 + x*0.05 for x in range(10) ]

# SigmaIs (from getSigmaI.py)
sigmaIs = [4.625654216624336, 4.372026004823843, 3.8980391564885464, 5.624214508297167, 3.6135681752396245]

print "Reading validation data..."
# for valFile in jsons[0:1]:
for valFile in tqdm.tqdm(jsons):
    # print "Reading " + valFile
    # Reading validation json
    try:
        with open(valJsons + valFile) as file:
            data = json.load(file)
    except:
        print "\nError reading " + valFile
        continue
    # Building detection dictionnary 
    detectionList = dict()
    for detect in data:
        img_id = detect['image_id']
        if not detectionList.has_key(img_id):
            detectionList[img_id] = []
        detectionList[img_id].append(detect)
    
    # print detectionLists
    # Nb of entities detected:
    correctPigNb = 0
    mOKS = 0
    mCorrectDt_loose = 0
    mCorrectDt_strict = 0
    mCorrectDt = [ 0 for i in range(len(OKS_threshold)) ]
    for gt in gtData:
        img_id = gt['image_id']
        numOtherPeople = gt['numOtherPeople']
        numKeypoints = gt['num_keypoints']
        if detectionList.has_key(img_id): # At least one detection for this frame
            PigCountPredict = len(detectionList[img_id])
        else: # No detection for this frame
            PigCountPredict = 0

        # Nb of entities detected
        PigCountGt = 1 + numOtherPeople
        if PigCountPredict == PigCountGt:
            correctPigNb += 1
    
        # Object Keypoint Similarity (OKS)
        if detectionList.has_key(img_id):
            keypointsGt = [gt['joint_self']] + [gt['joint_others'][i] for i in range(numOtherPeople)]
            scalesGt = [gt['scale_provided']] + [gt['scale_provided_other'][i] for i in range(numOtherPeople)]
            # Entities can be scrambled between gt and dt, so we need to get the closest gt for each dt
            scoreMap = [1e20 for i in range(PigCountGt)] # keeps track of the minScores for each gt-dt match
            matchingMap = [-1 for i in range(PigCountGt)] # map the gt with the dt for the current frame (to eliminate false positives from AP computation)
            for i in range(PigCountPredict):
                kpDt = detectionList[img_id][i]['keypoints']
                kpDt = [ [ kpDt[3*j], kpDt[3*j+1], kpDt[3*j+2] ] for j in range(numKeypoints) ]
                # Looking for matching gt
                kmin = -1
                scoreMin = 1e20
                for k in range(len(keypointsGt)):
                    sd = [ squaredDistance(keypointsGt[k][j], kpDt[j]) for j in range(numKeypoints) if kpDt[j][2] > 0 ]
                    score = float(sum(sd)) / float(len(sd))
                    if score < scoreMin:
                        scoreMin = score
                        kmin = k
                # Update scoreMap if better match found
                if scoreMap[kmin] > scoreMin:
                    scoreMap[kmin] = scoreMin
                    matchingMap[kmin] = i
            # OKS / AP
            for k in range(len(keypointsGt)):
                if matchingMap[k] == -1:
                    continue # No match for this gt
                kpDt = detectionList[img_id][matchingMap[k]]['keypoints']
                kpDt = [ [ kpDt[3*j], kpDt[3*j+1], kpDt[3*j+2] ] for j in range(numKeypoints) ]
                # Computing OKS
                precision = OKS( keypointsGt[k], kpDt, scalesGt[k], sigmaIs )
                # Checks for AP computation
                if precision > OKS_threshold_loose:
                    mCorrectDt_loose += 1
                if precision > OKS_threshold_strict:
                    mCorrectDt_strict += 1
                mCorrectDt = [ ( mCorrectDt[i] + 1 if precision > OKS_threshold[i] else mCorrectDt[i] ) for i in range(len(OKS_threshold)) ]
                # For mean OKS
                mOKS += precision

            

    # Compute the detection accuracy
    nbDetectedAcc = float(correctPigNb) / float(len(gtData)) * 100
    nbDetectedAccuracies.append(nbDetectedAcc)
    # Compute the mOKS
    mOKSAcc = float(mOKS) / float(len(data)) * 100
    mOKSAccuracies.append(mOKSAcc)
    # mAP OKS=0.5 (loose)
    mAP_loose = float(mCorrectDt[0]) / float(nbEntitiesGt) * 100
    mAPAccuracies_loose.append(mAP_loose)
    # mAP OKS=0.75 (strict)
    mAP_strict = float(mCorrectDt[5]) / float(nbEntitiesGt) * 100
    mAPAccuracies_strict.append(mAP_strict)
    # mAP OKS=0.5:0.05:0.95
    mAP = sum(mCorrectDt) / float(len(mCorrectDt) * nbEntitiesGt) * 100
    mAPAccuracies.append(mAP)
    # Get the iteration nb of the model
    nbIterations.append(int(re.split(r'\_|\.', valFile)[2]))

# Sorting accuracies in natural order
tmp = zip(nbIterations, nbDetectedAccuracies, mOKSAccuracies, mAPAccuracies_loose, mAPAccuracies_strict, mAPAccuracies)
tmp.sort()
nbIterations, nbDetectedAccuracies, mOKSAccuracies, mAPAccuracies_loose, mAPAccuracies_strict, mAPAccuracies = zip(*tmp)

# Plot accuracies
# plt.plot(nbIterations, nbDetectedAccuracies)
plt.plot(nbIterations, mOKSAccuracies)
plt.plot(nbIterations, mAPAccuracies_loose)
plt.plot(nbIterations, mAPAccuracies_strict)
plt.plot(nbIterations, mAPAccuracies)

# plt.xscale('log')
plt.title('OKS Metrics ({})'.format(experiment))
plt.xlabel("Nb iterations")
plt.ylabel("Score")
plt.legend([
    # 'Detection Accuracies',
    'Mean OKS',
    'mAP OKS=.5 (loose)',
    'mAP OKS=.75 (strict)',
    'mAP OKS=.5:.05:.95 (COCO challenge)'
])
plt.grid(which='minor', axis='both')
plt.grid(which='major', axis='both')

plt.show()