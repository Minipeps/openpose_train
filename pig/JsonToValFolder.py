
import json
import tqdm
from shutil import copyfile


jsonFile = "annotations_final_v3.json"
datasetFolder = "../dataset/PigData/"
imgFolder = datasetFolder + "duroc_3stk/RGB/"
valFolder = datasetFolder  + "validation/"

with open(datasetFolder + jsonFile) as file:
    data = json.load(file)
    file.close()

for d in tqdm.tqdm(data):
    imgPath = d['img_paths']
    copyfile(imgFolder + imgPath, valFolder + imgPath)

