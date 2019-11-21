import json
import tqdm
import cv2
import math

### Begin Definitions ###

def fixPathName(pathName):
    ''' "123 .jpg" -> "123.jpg" '''
    return ''.join(pathName.split(' '))

def getObjPos(keypoints):
    tail = keypoints[-1]
    nose = keypoints[-2]

    return [ (nose[0] + tail[0]) / 2, (nose[1] + tail[1]) / 2 ]

def getScale(keypoints):
    ''' return scale with respect to 200px '''
    nose = keypoints[-2]
    tail = keypoints[-1]

    size = math.sqrt((nose[0]-tail[0])**2 + (nose[1]-tail[1])**2)

    return size/200

### End Definitions ###

datasetFolder = "D:/Documents/Programmation/openpose_train/dataset/PigData/"
# exportFolder = datasetFolder + "pig21/"
imagesFolder = datasetFolder + "duroc_3stk/RGB/"

raw = "annotations.json"
# fixed = "annotations_fixed.json"
final = "annotations_final_v2.5.json"


with open(raw) as fileRaw:
    dataRaw = json.load(fileRaw)
    fileRaw.close()

# with open(fixed) as fileFixed:
#     dataFixed = json.load(fileFixed)
#     fileFixed.close()

# modified = 0
# print "Raw data length:", len([x for x in dataRaw if x != []])
# print "Fixed data length:", len([x for x in dataFixed if x != []])
# for i in tqdm.tqdm(range(len(dataRaw))):
#     if dataRaw[i] != []:
#         # Check for annotations in the wrong place (to avoid duplicates of annotations on the same image)
#         assert dataRaw[i]['image_id'] == i, "Something is wrong with this annotation: " + str(dataRaw[i]['image_id'])
#         dataRaw[i]['img_paths'] = fixPathName(dataRaw[i]['img_paths'])
#         if i < len(dataFixed):
#             if dataFixed[i] != dataRaw[i]:
#                 if dataFixed[i] != []:
#                     a = raw_input("\nDo you want to override annotation " + str(dataRaw[i]['image_id']) + "? [y/N]: ")
#                     if a.lower() != 'y':
#                         print "Annotation " + str(dataRaw[i]['image_id']) + " skipped"
#                     else:
#                         print "Annotation " + str(dataRaw[i]['image_id']) + " updated"
#                         dataFixed[i] = dataRaw[i]
#                         modified += 1
#                 else:
#                     dataFixed[i] = dataRaw[i]
#                     modified += 1
#         else:
#             for j in range(len(dataFixed), i+1):
#                 dataFixed.append([])
#             dataFixed[i] = dataRaw[i]
#             dataFixed[i]['img_paths'] = fixPathName(dataRaw[i]['img_paths'])
#             print "Annotation " + str(dataRaw[i]['image_id']) + " updated"
#             modified += 1

# json.dump(dataFixed, open('annotations_fixed.json', 'w+'))

# print modified, "annotations modified"
# if modified > 0:
#     print "New fixed data length:", len([x for x in dataFixed if x != []])

try:
    file = open(datasetFolder + final)
    dataBackup = json.load(file)
    existingData = [x["img_paths"] for x in dataBackup]
    file.close()
except:
    print "Error reading " + final
    existing = []
    dataBackup = []


# Completing annotations format
dataFinal = dataBackup + [x for x in [x for x in dataRaw if x != []] if x["img_paths"] not in existingData]
for i in range(len(dataFinal)):
    numOtherPeople = dataFinal[i]["numOtherPeople"]
    dataFinal[i]["people_index"] = dataFinal[i]["image_id"]
    dataFinal[i]["annolist_index"] = dataFinal[i]["image_id"]
    dataFinal[i]["objpos"] = getObjPos(dataFinal[i]["joint_self"])
    dataFinal[i]["scale_provided"] = getScale(dataFinal[i]["joint_self"])

    dataFinal[i]["objpos_other"] = [ getObjPos(dataFinal[i]["joint_others"][j]) for j in range(numOtherPeople) ]
    dataFinal[i]["scale_provided_other"] = [ getScale(dataFinal[i]["joint_others"][j]) for j in range(numOtherPeople) ]

with open(datasetFolder + final, 'w+') as finalFile:
    print("Total number of images annotated: " + str(len(dataFinal)))
    json.dump(dataFinal, finalFile)
    finalFile.close()