#!/bin/bash
# Script to extract COCO JSON file for each trained model
clear && clear

echo "Parameters to change"
# NUMBER_FOLDER=
# NUMBER=${NUMBER_FOLDER}
EXPERIMENT=pig5_v4
# IMAGE_DIR=D:/Documents/Programmation/openpose_train/dataset/PigData/test/
IMAGE_DIR=D:/Documents/Programmation/openpose_train/dataset/PigData/duroc_10stk/RGB/
# IMAGE_DIR_CF="/home/gines/devel/images/car-fusion_val/"
# IMAGE_DIR_P3="/home/gines/devel/images/pascal3d+_val/"
# IMAGE_DIR_V7="/home/gines/devel/images/veri-776_val/"

# echo "Common parameters to both files a_*.sh and b_*.sh"
SHARED_FOLDER=D:/Documents/Programmation/openpose_train/training_results/${EXPERIMENT}/pig/pig_5/
# SHARED_FOLDER=/media/posefs3b/Users/gines/openpose_train/training_results/${EXPERIMENT}/car/car_${NUMBER}/
# echo " "

echo "Paths"
OPENPOSE_MODEL=PIG_5
OPENPOSE_MODEL_FILE_NAME=pose_iter_XXXXXX.caffemodel
OPENPOSE_FOLDER=D:/Documents/Programmation/openpose/
# OPENPOSE_FOLDER=/home/gines/Dropbox/Perceptual_Computing_Lab/openpose/openpose/

# echo "Sleeping for 8h..."
# sleep 27000
# echo "Awaken!"



# Remove last XXXXXX.caffemodel
temporaryModel=${SHARED_FOLDER}/${OPENPOSE_MODEL_FILE_NAME}
echo "Using ${temporaryModel} as temporary model..."
echo " "
rm $temporaryModel



# Different code than a_*.sh
echo "Running OpenPose for each model"
MODEL_FOLDER=$(dirname $(dirname ${SHARED_FOLDER}))/
pwd
cd $OPENPOSE_FOLDER
# Sorted in natural order (NAT sort)
modelPath=${SHARED_FOLDER}/pose_iter_222000.caffemodel
# Not NAT sort
# for modelPath in ${SHARED_FOLDER}*.caffemodel; do
# temporaryModel=$(dirname ${modelPath})/${OPENPOSE_MODEL_FILE_NAME}
modelName=$(basename ${modelPath})

echo "Processing $modelName in $EXPERIMENT"

# Rename file to OpenPose name
mv $modelPath $temporaryModel
# 1 scale CF
# Processing
# ./build/examples/openpose/openpose.bin \
# build/x64/Release/OpenPoseDemo.exe \
#     --model_folder ${MODEL_FOLDER} --model_pose ${OPENPOSE_MODEL} --video "D:\Downloads\duroc6stk-frames1000to1999-crf25.mp4" \
#     --render_pose 2 --display 2 --num_gpu -1 --write_video "D:/Downloads/duroc6stk-frames1000to1999-crf25-OUT.avi" --write_video_fps -1
build/x64/Release/OpenPoseDemo.exe \
    --model_folder ${MODEL_FOLDER} --model_pose ${OPENPOSE_MODEL} --image_dir ${IMAGE_DIR} \
    --render_pose 2 --display 2 --num_gpu -1 --write_video "D:/Downloads/duroc6stk-frames1000to1999-uncompressed-OUTv3.avi" --write_video_fps 25
# Move JSON after finished (so no Dropbox updating all the time)

# Rename back to original name
mv $temporaryModel $modelPath

# echo $modelPath
echo " "
echo " "


echo "Finished! Exiting script..."
echo " "