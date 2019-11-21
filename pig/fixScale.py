import json, math

datasetFolder = "../dataset/PigData/"

source = "annotations_final_v2.4.json"
output = "annotations_final_v2.5.json"


def getScale(keypoints):
    ''' return scale with respect to 200px '''
    nose = keypoints[-2]
    tail = keypoints[-1]

    size = math.sqrt((nose[0]-tail[0])**2 + (nose[1]-tail[1])**2)

    return size/200



with open(datasetFolder + source) as sourceFile:
    data = json.load(sourceFile)
    sourceFile.close()

for i in range(len(data)):
    # self
    keypoints = data[i]["joint_self"]
    data[i]["scale_provided"] = getScale(keypoints)
    # other
    for j in range(data[i]["numOtherPeople"]):
        keypoints = data[i]["joint_others"][j]
        data[i]["scale_provided_other"][j] = getScale(keypoints)

with open(datasetFolder + output, 'w+') as outFile:
    json.dump(data, outFile)
    outFile.close()