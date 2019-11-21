import json

AnnotationFolder = "../dataset/PigData/"
source = AnnotationFolder + "annotations_final_v2.json"

with open(source) as fileSource:
    data = json.load(fileSource)
    fileSource.close()


for i in range (len(data)):
    data[i]["annolist_index"] = i
    data[i]["people_index"] = i

with open(AnnotationFolder + "annotations_final_v2.2", 'w+') as file:
    json.dump(data, file)
    file.close()

