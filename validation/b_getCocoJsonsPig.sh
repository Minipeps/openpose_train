#!/bin/bash
# Script to extract COCO JSON file for each trained model
clear && clear

echo "Parameters to change"
# NUMBER_FOLDER=
# NUMBER=${NUMBER_FOLDER}
EXPERIMENT=pig5_v4
IMAGE_DIR=D:/Documents/Programmation/openpose_train/dataset/PigData/validation/
IMAGE_DIR_3STK=D:/Documents/Programmation/openpose_train/dataset/PigData/validation_3stk/
IMAGE_DIR_6STK=D:/Documents/Programmation/openpose_train/dataset/PigData/validation_6stk/
IMAGE_DIR_10STK=D:/Documents/Programmation/openpose_train/dataset/PigData/validation_10stk/

# echo "Common parameters to both files a_*.sh and b_*.sh"
SHARED_FOLDER=D:/Documents/Programmation/openpose_train/training_results/${EXPERIMENT}/pig/pig_5/
# echo " "

echo "Paths"
OPENPOSE_MODEL=PIG_5
OPENPOSE_MODEL_FILE_NAME=pose_iter_XXXXXX.caffemodel
OPENPOSE_FOLDER=D:/Documents/Programmation/openpose/

JSON_FOLDER_1=${SHARED_FOLDER}scale_1/
JSON_FOLDER_3stk=${SHARED_FOLDER}3stk/
JSON_FOLDER_6stk=${SHARED_FOLDER}6stk/
JSON_FOLDER_10stk=${SHARED_FOLDER}10stk/

mkdir $JSON_FOLDER_1
mkdir $JSON_FOLDER_3stk
mkdir $JSON_FOLDER_6stk
mkdir $JSON_FOLDER_10stk
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
    finalJsonFile3stk=${JSON_FOLDER_3stk}${modelName}_3stk.json
    finalJsonFile6stk=${JSON_FOLDER_6stk}${modelName}_6stk.json
    finalJsonFile10stk=${JSON_FOLDER_10stk}${modelName}_10stk.json

    echo "Processing $modelName in $EXPERIMENT"

    if [ -f $finalJsonFile1 ] && [ -f $finalJsonFile3stk ] && [ -f $finalJsonFile6stk ] && [ -f $finalJsonFile10stk ]; then
        echo "JSONs files already exists!"
    else
        # Rename file to OpenPose name
        mv $modelPath $temporaryModel
        
        # 1 scale / validation
        if [ -f $finalJsonFile1 ]; then
            echo "JSON scale-1 file already exists!"
        # JSON file does not exist
        else
            # Processing
            # ./build/examples/openpose/openpose.bin \
            build/x64/Release/OpenPoseDemo.exe \
                --model_folder ${MODEL_FOLDER} --model_pose ${OPENPOSE_MODEL} --image_dir ${IMAGE_DIR} \
                --write_coco_json_variants 1 --write_coco_json $temporaryJsonFile --render_pose 0 --display 0 --num_gpu -1
            # Move JSON after finished (so no Dropbox updating all the time)
            mv $temporaryJsonFile $finalJsonFile1
        fi
        # duroc_3stk
        if [ -f $finalJsonFile3stk ]; then
            echo "JSON file already exists!"
        # JSON file does not exist
        else
            # Processing
            # ./build/examples/openpose/openpose.bin \
            build/x64/Release/OpenPoseDemo.exe \
                --model_folder ${MODEL_FOLDER} --model_pose ${OPENPOSE_MODEL} --image_dir ${IMAGE_DIR_3STK} \
                --write_coco_json_variants 1 --write_coco_json $temporaryJsonFile --render_pose 0 --display 0 --num_gpu -1
            # Move JSON after finished (so no Dropbox updating all the time)
            mv $temporaryJsonFile $finalJsonFile3stk
        fi
        # duroc_6stk
        if [ -f $finalJsonFile6stk ]; then
            echo "JSON file already exists!"
        # JSON file does not exist
        else
            # Processing
            # ./build/examples/openpose/openpose.bin \
            build/x64/Release/OpenPoseDemo.exe \
                --model_folder ${MODEL_FOLDER} --model_pose ${OPENPOSE_MODEL} --image_dir ${IMAGE_DIR_6STK} \
                --write_coco_json_variants 1 --write_coco_json $temporaryJsonFile --render_pose 0 --display 0 --num_gpu -1
            # Move JSON after finished (so no Dropbox updating all the time)
            mv $temporaryJsonFile $finalJsonFile6stk
        fi
        # duroc_10stk
        if [ -f $finalJsonFile10stk ]; then
            echo "JSON file already exists!"
        # JSON file does not exist
        else
            # Processing
            # ./build/examples/openpose/openpose.bin \
            build/x64/Release/OpenPoseDemo.exe \
                --model_folder ${MODEL_FOLDER} --model_pose ${OPENPOSE_MODEL} --image_dir ${IMAGE_DIR_10STK} \
                --write_coco_json_variants 1 --write_coco_json $temporaryJsonFile --render_pose 0 --display 0 --num_gpu -1
            # Move JSON after finished (so no Dropbox updating all the time)
            mv $temporaryJsonFile $finalJsonFile10stk
        fi

        # Rename back to original name
        mv $temporaryModel $modelPath
    fi
    # echo $modelPath
    echo " "
done
echo " "


echo "Finished! Exiting script..."
echo " "
