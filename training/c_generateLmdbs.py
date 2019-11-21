import os
# from my_generateLmdbFile import generateLmdbFile, generateNegativesLmdbFile
from generateLmdbFile import generateLmdbFile, generateNegativesLmdbFile


sCaffePythonPath = os.path.join('/home/user1/Documents/openpose_caffe_train', 'python/')
sDatasetFolderLmdb = '/home/user1/Documents/openpose_train/dataset/'
sDatasetFolder = '/home/user1/Documents/openpose_train/dataset/'

# # COCO
sCocoDatasetFolder = sDatasetFolder + 'COCO/'
sCocoLmdbPath = sDatasetFolderLmdb + 'lmdb_coco/'
sCocoImagesFolder = sCocoDatasetFolder + 'cocoapi/images/'
sCocoJsonFile = sCocoDatasetFolder + 'json/COCO.json'

# # MPII
# sMpiiDatasetFolder = sDatasetFolder + 'MPII/'
# sMpiiLmdbPath = sDatasetFolderLmdb + 'lmdb_mpii/'
# sMpiiImagesFolder = sMpiiDatasetFolder + 'images/'
# sMpiiMaskFolder = sMpiiDatasetFolder + 'mask/'
# sMpiiJsonFile = sMpiiDatasetFolder + 'json/root_mpii.json'

# Pig
sPigDatasetFolder = sDatasetFolder + 'PigData/'
sPigLmdbPath = sDatasetFolderLmdb + 'lmdb_pig5_v3/' # v2.2 had mask offset of 1...
sPigImagesFolder = sPigDatasetFolder + 'duroc_3stk/RGB/'
sPigMaskFolder = sPigDatasetFolder + 'duroc_3stk/MASKS/'
sPigJsonFile = sPigDatasetFolder + 'annotations_final_v3.json' # v2.2 had bad visibility index, v2.5 gives more accurate scales

# # Negatives
# # COCO background
sBackgroundLmdbPath = sDatasetFolderLmdb + 'lmdb_background/'
sBackgroundImagesFolder = sCocoImagesFolder + 'train2017/'
sBackgroundJsonFile = sCocoDatasetFolder + 'json/coco_negatives.json'
# # COCO car background
# sCarBackgroundLmdbPath = sDatasetFolderLmdb + 'lmdb_car_background/'
# sCarBackgroundImagesFolder = sCocoImagesFolder + 'train2017/'
# sCarBackgroundJsonFile = sCocoDatasetFolder + 'json/coco_negatives_cars.json'



if __name__ == "__main__":
    # Positives
    # Body and/or foot
    # generateLmdbFile(sCocoLmdbPath, sCocoImagesFolder, sCocoJsonFile, sCaffePythonPath)
    # Pig
    generateLmdbFile(sPigLmdbPath, sPigImagesFolder, sPigJsonFile, sCaffePythonPath, sPigMaskFolder)

    # Negatives
    # generateNegativesLmdbFile(sBackgroundLmdbPath, sBackgroundImagesFolder, sBackgroundJsonFile, sCaffePythonPath)
    # generateNegativesLmdbFile(sCarBackgroundLmdbPath, sCarBackgroundImagesFolder, sCarBackgroundJsonFile, sCaffePythonPath)
