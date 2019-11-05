import json
import tqdm
import cv2

### Begin Definitions ###

def fixPathName(pathName):
    ''' "123 .jpg" -> "123.jpg" '''
    return ''.join(pathName.split(' '))

def getObjPos(keypoints):
    tail = keypoints[-1]
    nose = keypoints[-2]

    return [ (nose[0] + tail[0]) / 2, (nose[1] + tail[1]) / 2 ]

### End Definitions ###

datasetFolder = "/home/maxime/Documents/openpose_train/dataset/PigData/"
exportFolder = datasetFolder + "pig21/"
imagesFolder = datasetFolder + "duroc_6stk/RGB/"

raw = "annotations.json"
fixed = "annotations_fixed.json"
final = "annotations_final.json"


with open(raw) as fileRaw:
    dataRaw = json.load(fileRaw)
    fileRaw.close()

with open(fixed) as fileFixed:
    dataFixed = json.load(fileFixed)
    fileFixed.close()

modified = 0
print "Raw data length:", len([x for x in dataRaw if x != []])
print "Fixed data length:", len([x for x in dataFixed if x != []])
for i in tqdm.tqdm(range(len(dataRaw))):
    if dataRaw[i] != []:
        # Check for annotations in the wrong place (to avoid duplicates of annotations on the same image)
        assert dataRaw[i]['image_id'] == i, "Something is wrong with this annotation: " + str(dataRaw[i]['image_id'])
        dataRaw[i]['img_paths'] = fixPathName(dataRaw[i]['img_paths'])
        if i < len(dataFixed):
            if dataFixed[i] != dataRaw[i]:
                if dataFixed[i] != []:
                    a = raw_input("\nDo you want to override annotation " + str(dataRaw[i]['image_id']) + "? [y/N]: ")
                    if a.lower() != 'y':
                        print "Annotation " + str(dataRaw[i]['image_id']) + " skipped"
                    else:
                        print "Annotation " + str(dataRaw[i]['image_id']) + " updated"
                        dataFixed[i] = dataRaw[i]
                        modified += 1
                else:
                    dataFixed[i] = dataRaw[i]
                    modified += 1
        else:
            for j in range(len(dataFixed), i+1):
                dataFixed.append([])
            dataFixed[i] = dataRaw[i]
            dataFixed[i]['img_paths'] = fixPathName(dataRaw[i]['img_paths'])
            print "Annotation " + str(dataRaw[i]['image_id']) + " updated"
            modified += 1

json.dump(dataFixed, open('annotations_fixed.json', 'w+'))

print modified, "annotations modified"
if modified > 0:
    print "New fixed data length:", len([x for x in dataFixed if x != []])

# Completing annotations format
dataFinal = [x for x in dataFixed if x != []]
for i in range(len(dataFinal)):
    numOtherPeople = dataFinal[i]["numOtherPeople"]
    dataFinal[i]["people_index"] = 0
    dataFinal[i]["annolist_index"] = 0
    dataFinal[i]["objpos"] = getObjPos(dataFinal[i]["joint_self"])
    dataFinal[i]["scale_provided"] = 1

    dataFinal[i]["objpos_other"] = [ getObjPos(dataFinal[i]["joint_others"][j]) for j in range(numOtherPeople) ]
    dataFinal[i]["scale_provided_other"] = [ 1 for j in range(numOtherPeople) ]

with open(final, 'w+') as finalFile:
    json.dump(dataFinal, finalFile)
    finalFile.close()