#!/bin/bash
# Script to copy models from GPU-6 to local

SSH_LOGIN=user1@128.39.140.213

function verify_copy {
    if [ -f $2$(basename $1) ]; then
        echo "$2$(basename $1) already exists!"
    else
        echo "Copying $1 to $2..."
        scp $1 $2
    fi
    echo " "
}


echo "Common parameters to both files a_*.sh and b_*.sh"
EXPERIMENT=pig5_v4
SHARED_FOLDER=D:/Documents/Programmation/openpose_train/training_results/${EXPERIMENT}/pig/pig_5/
echo " "

echo "Paths"
TRAINING_FOLDER=/home/user1/Documents/openpose_train/
MODELS_RELATIVE_FOLDER=training_results/pose/model/
PROTOTXT_RELATIVE_FOLDER=training_results/pose/
echo " "

echo "File names"
PROTOTXT_NAME=*.prototxt
TRAINING_LOG_NAME=*.txt
SET_LAYERS_FILE_NAME1=training/d_setLayers_pig.py
SET_LAYERS_FILE_NAME2=training/generateProtoTxt.py
SET_LAYERS_FILE_NAME3=training/getResNetProtoTxt.py
echo " "

SLEEPING_TIME=120
SLEEPING_TIME_MIN=2


# Different code than b_*.sh
echo "Creating shared folder $SHARED_FOLDER..."
mkdir -p $SHARED_FOLDER
echo " "

while true
do
    echo "Copying prototxt and training log from ${TRAINING_FOLDER}${MODELS_RELATIVE_FOLDER}..."
    for prototxtFile in $(ssh ${SSH_LOGIN} "ls ${TRAINING_FOLDER}${PROTOTXT_RELATIVE_FOLDER}${PROTOTXT_NAME}"); do
        verify_copy ${SSH_LOGIN}:${prototxtFile} ${SHARED_FOLDER}
    done
    scp ${SSH_LOGIN}:${TRAINING_FOLDER}${PROTOTXT_RELATIVE_FOLDER}${TRAINING_LOG_NAME} ${SHARED_FOLDER} # always overwrite training log
    echo " "

    echo "Copying ${SET_LAYERS_FILE_NAME1} from ${TRAINING_FOLDER}${MODELS_RELATIVE_FOLDER}..."
    verify_copy ${SSH_LOGIN}:${TRAINING_FOLDER}${SET_LAYERS_FILE_NAME1} ${SHARED_FOLDER}
    verify_copy ${SSH_LOGIN}:${TRAINING_FOLDER}${SET_LAYERS_FILE_NAME2} ${SHARED_FOLDER}
    verify_copy ${SSH_LOGIN}:${TRAINING_FOLDER}${SET_LAYERS_FILE_NAME3} ${SHARED_FOLDER}
    echo " "

    echo "Copying models from ${TRAINING_FOLDER}${MODELS_RELATIVE_FOLDER}..."
    for caffemodelFile in $(ssh ${SSH_LOGIN} "ls ${TRAINING_FOLDER}${MODELS_RELATIVE_FOLDER}*.caffemodel"); do
        verify_copy ${SSH_LOGIN}:${caffemodelFile} ${SHARED_FOLDER}
    done
    echo " "

    # Sleeping
    echo "Sleeping ${SLEEPING_TIME} seconds (${SLEEPING_TIME_MIN} minutes)..."
    sleep $SLEEPING_TIME
    echo "Copying again in 10 seconds"
    sleep 10
done





echo "Finished! Exiting script..."
echo " "
