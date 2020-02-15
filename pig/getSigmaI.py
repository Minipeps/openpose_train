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

############################################

jsons = os.listdir(valJsons)

with open(datasetFolder + jsonFile) as gtFile:
    gtData = json.load(gtFile)

sigmaIs = [0, 0, 0, 0, 0]
Eis = [0, 0, 0, 0, 0]
countIs = [0, 0, 0, 0, 0]

print "Reading validation data..."
for valFile in jsons[0:1]:
# for valFile in tqdm.tqdm(jsons):
    print "Reading " + valFile
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
    for gt in gtData:
        img_id = gt['image_id']
        numOtherPeople = gt['numOtherPeople']
        numKeypoints = gt['num_keypoints']
        PigCountGt = 1 + numOtherPeople
        if detectionList.has_key(img_id): # At least one detection for this frame
            PigCountPredict = len(detectionList[img_id])
        else: # No detection for this frame
            PigCountPredict = 0

        # SigmaI
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
            # Computing E for each keypoint of the current dt
            for k in range(PigCountGt):
                kpDt = detectionList[img_id][matchingMap[k]]['keypoints']
                kpDt = [ [ kpDt[3*j], kpDt[3*j+1], kpDt[3*j+2] ] for j in range(numKeypoints) ]
                for j in range(numKeypoints):
                    sd = squaredDistance( keypointsGt[k][j], kpDt[j] )
                    E = float(sd) / float(scalesGt[k]**2)
                    Eis[j] += E
                    countIs[j] += 1

print(Eis)
print(countIs)
sigmaIs = [ math.sqrt( Eis[i] / countIs[i] ) for i in range(len(Eis)) ]
print(sigmaIs)