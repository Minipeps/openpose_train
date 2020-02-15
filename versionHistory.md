# Version History & Work Progress

This gives an overview of the evolution of the training process, most of those experiments didn't not give any results but they demonstrate how I progressed through this project work, until I got the final trained model in experiment _pig_v4_.

## _pig5_21_

- duroc_6stk db, 21 images annotated, no background, no masks

## _pig5_v1_

- duroc_6stk db, 21 images annotated, with background, no masks

## _pig5_v2.1_

- duroc_3stk db, 22 images annotated, with background, with masks (maybe offset by 1)

## _pig5_v2.2_

- duroc_3stk db, 55 images annotated, with background, with masks (mistake -> masks are offset by 1)

## _pig5_v2.3_

- duroc_3stk db, 55 images annotated, with background, with masks

## _pig5_v2.4_

- same as v2.3 but fixed visibility and mask indexes

## _pig5_v2.5_

- Small tweaks done after v2.4, no real improvement over the result

## _pig5_v2.5.1_

- Same as v2.5, training resumed from checkpoint at 6k iterations

## _pig5_v3_

- now with 236% more images annotated! (55 -> 130)
- _Notes_: Training loss diverged after only 10k iterations

## _pig5_v4_ (best & final)

- another test without background and no scaling (as apparent size of the pigs does not change in the pen)
- Trained model download link: [pose_iter_124000.caffemodel](https://studntnu-my.sharepoint.com/:u:/g/personal/maximep_ntnu_no/EXjE4EzIMgZOsxjzj0-WDusB4hq60t4KBwR9xufSA3Wo4Q)

## Further work & Improvement ideas

- Images sequences are not ideal for traning because successive frames might be too similar from each other
- The nose is rarely visible, maybe try a new model (PIG_4) with only: LEar, REar, Neck and Tail? Or add other useful joints (shoulders, hips,...)
- Combine training data from multiples folders (3stk,6stk,10stk... duroc/landsvin...) for better generalization
- Tweak training hyperparameters

## Validation/Testing Metrics

- Average Precision (& Average Recall), using Keypoint Similarity Score OKS from [COCO](http://cocodataset.org/#keypoints-eval)
- Proportion of # tracked entity against the ground thruth # of entities
