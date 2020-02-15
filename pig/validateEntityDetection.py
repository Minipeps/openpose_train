import tqdm
import os
import json
import re
import itertools
import math
import matplotlib.pyplot as plt



datasetFolder = "../dataset/PigData/"
experiment = "pig5_v4"
valNbEntities = [ 3, 6, 10 ]

########################################################################################

for nbEntities in valNbEntities:
    valFolder = datasetFolder  + "validation_{}stk/".format(nbEntities)
    valJsons = "../training_results/{}/pig/pig_5/{}stk/".format(experiment, nbEntities)

    # Get json in the valJson folder
    jsons = os.listdir(valJsons)
    # Get image ids
    img_names = os.listdir(valFolder)

    img_ids = [ int(img_id.split('.')[0]) for img_id in img_names ]

    nbIterations = []
    nbDetectedAccuracies = []
    nbDetectErrors = []

    print "Reading validation_{}stk data...".format(nbEntities)
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
        nbDetectedError = 0
        for img_id in img_ids:
            if detectionList.has_key(img_id): # At least one detection for this frame
                PigCountPredict = len(detectionList[img_id])
            else: # No detection for this frame
                PigCountPredict = 0

            # Nb of entities detected
            # if PigCountPredict == nbEntities:
            #     correctPigNb += 1
            # Nb of entities detected -+1
            if abs(PigCountPredict - nbEntities) < 2:
                correctPigNb += 1

            nbDetectedError += abs(PigCountPredict - nbEntities)

        # Entity Detection Error
        nbDetectErrors.append(float(nbDetectedError) / float(len(img_ids)))
        # Compute the detection accuracy
        nbDetectedAcc = float(correctPigNb) / float(len(img_ids)) * 100
        nbDetectedAccuracies.append(nbDetectedAcc)
        # Get the iteration nb of the model
        nbIterations.append(int(re.split(r'\_|\.', valFile)[2]))

    # Sorting accuracies in natural order
    tmp = zip(nbIterations, nbDetectedAccuracies, nbDetectErrors)
    tmp.sort()
    nbIterations, nbDetectedAccuracies, nbDetectErrors = zip(*tmp)

    # Plot accuracies
    plt.plot(nbIterations, nbDetectErrors)
    # plt.plot(nbIterations, nbDetectedAccuracies)

# plt.xscale('log')
plt.title('Entity Detection Error ({})'.format(experiment))
plt.xlabel("Nb iterations")
plt.ylabel("Average Error")
plt.legend([ 'duroc_{}stk'.format(nbEntities) for nbEntities in valNbEntities ])
plt.grid(which='minor', axis='both')
plt.grid(which='major', axis='both')

plt.show()