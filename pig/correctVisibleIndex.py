import json, tqdm

dataFolder = "../dataset/PigData/"

final = dataFolder + "annotations_final_v2.2.json"
exported = dataFolder + "annotations_final_v2.4.json"


with open(final) as file:
    data = json.load(file)
    file.close()


for i in tqdm.tqdm(range(len(data))):
    # Correcting joint self
    for k in range(data[i]['num_keypoints']):
        data[i]['joint_self'][k][2] -= 1
    # Correcting joint others
    for j in range(data[i]['numOtherPeople']):
            for k in range(data[i]['num_keypoints']):
                data[i]['joint_others'][j][k][2] -= 1

with open(exported, 'w+') as fileExp:
    json.dump(data, fileExp)
    fileExp.close()