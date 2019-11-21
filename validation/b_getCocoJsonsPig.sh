#!/bin/bash
# Script to extract COCO JSON file for each trained model
clear && clear

echo "Parameters to change"
# NUMBER_FOLDER=
# NUMBER=${NUMBER_FOLDER}
EXPERIMENT=pig5_v4
IMAGE_DIR=D:/Documents/Programmation/openpose_train/dataset/PigData/validation/
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

JSON_FOLDER_1=${SHARED_FOLDER}scale_1/
# JSON_FOLDER_CF_1=${SHARED_FOLDER}scaleCF_1/
# JSON_FOLDER_P3_1=${SHARED_FOLDER}scaleP3_1/
# JSON_FOLDER_V7_1=${SHARED_FOLDER}scaleV7_1/
JSON_FOLDER_4=${SHARED_FOLDER}scale_4/
# JSON_FOLDER_P3_4=${SHARED_FOLDER}scaleP3_4/
# JSON_FOLDER_V7_4=${SHARED_FOLDER}scaleV7_4/
mkdir $JSON_FOLDER_1
# mkdir $JSON_FOLDER_P3_1
# mkdir $JSON_FOLDER_V7_1
# mkdir $JSON_FOLDER_4
# mkdir $JSON_FOLDER_P3_4
# mkdir $JSON_FOLDER_V7_4
echo " "

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
for modelPath in `ls -v ${SHARED_FOLDER}*.caffemodel`; do
# Not NAT sort
# for modelPath in ${SHARED_FOLDER}*.caffemodel; do
    # temporaryModel=$(dirname ${modelPath})/${OPENPOSE_MODEL_FILE_NAME}
    modelName=$(basename ${modelPath})
    temporaryJsonFile=${SHARED_FOLDER}/temporaryJson_${EXPERIMENT}_${modelName}.json
    finalJsonFile1=${JSON_FOLDER_1}${modelName}_1.json
    # finalJsonFileP31=${JSON_FOLDER_P3_1}${modelName}_1.json
    # finalJsonFileV71=${JSON_FOLDER_V7_1}${modelName}_1.json
    finalJsonFile4=${JSON_FOLDER_4}${modelName}_4.json
    # finalJsonFileP34=${JSON_FOLDER_P3_4}${modelName}_4.json
    # finalJsonFileV74=${JSON_FOLDER_V7_4}${modelName}_4.json

    echo "Processing $modelName in $EXPERIMENT"
    # JSON file does exist (already created)
    # if [ -f $finalJsonFileCF1 ]; then
    # if [ -f $finalJsonFileCF1 ] && [ -f $finalJsonFileP31 ] && [ -f $finalJsonFileV71 ] && [ -f $finalJsonFileCF4 ]; then
    # rm $finalJsonFile1

    if [ -f $finalJsonFile1 ] && [ -f $finalJsonFile4 ]; then
        echo "JSONs files already exists!"
    else
        # Rename file to OpenPose name
        mv $modelPath $temporaryModel
        
        # 1 scale
        if [ -f $finalJsonFile1 ]; then
            echo "JSON scale-1 file already exists!"
        # JSON file does not exist
        else
            # Processing
            # ./build/examples/openpose/openpose.bin \
            build/x64/Release/OpenPoseDemo.exe \
                --model_folder ${MODEL_FOLDER} --model_pose ${OPENPOSE_MODEL} --image_dir ${IMAGE_DIR} \
                --write_coco_json_variants 1 --write_coco_json $temporaryJsonFile --render_pose 2 --display 2 --num_gpu -1
            # Move JSON after finished (so no Dropbox updating all the time)
            mv $temporaryJsonFile $finalJsonFile1
        fi
        # # 4 scale
        # if [ -f $finalJsonFile4 ]; then
        #     echo "JSON file already exists!"
        # # JSON file does not exist
        # else
        #     # Processing
        #     # ./build/examples/openpose/openpose.bin \
        #     build/x64/Release/OpenPoseDemo.exe \
        #         --model_folder ${MODEL_FOLDER} --model_pose ${OPENPOSE_MODEL} --image_dir ${IMAGE_DIR} \
        #         --write_coco_json_variants 1 --write_coco_json $temporaryJsonFile --render_pose 2 --display 2 --num_gpu -1
        #     # Move JSON after finished (so no Dropbox updating all the time)
        #     mv $temporaryJsonFile $finalJsonFile4
        # fi

        # Rename back to original name
        mv $temporaryModel $modelPath
    fi
    # echo $modelPath
    echo " "
done
echo " "


echo "Finished! Exiting script..."
echo " "
