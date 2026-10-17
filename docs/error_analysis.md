# Error analysis

Run: yolov8n, 50 epochs, imgsz 640, validation split 23 images, conf 0.25, IoU 0.5.
Evidence: `results/evidence/val_predictions/val_batch0_pred_grid.jpg` (real predictions from the run) and, after re-running the notebook, `results/evidence/errors/` (red = false positive, blue = false negative).

> **How to finish this file (10 min):** the patterns below are what the metrics and the prediction grid show. For each item, open the matching image in `results/evidence/errors/` (notebook cell 7), paste the real file name, and keep or correct the hypothesis. A hypothesis is only as good as the image you can point to.

## Three false positives (model predicts something that is not there)
| # | Image | What was predicted | Likely cause (hypothesis) |
|---|---|---|---|
| FP_11358_png_jpg.rf.3bd99770d0817ea25605ffb0e0e1be3f | many extra `Furniture` boxes (conf 0.3-0.5) stacked on the same area | Furniture is the least consistent class (P = 0.29). Symbols are not clearly defined and unlabelled furniture in the ground truth turns correct detections into "false" positives. Check for missing labels first. |
| FP_665_png_jpg.rf.a1ebe8395ea303f0a231f16cb94008bd | no `Window` boxes on wall lines / no `Door` boxes on wall lines | Too few negatives of this look-alike. |
| FN_712_png_jpg.rf.fb7dbc6fd4224a4539c85ffc54f7a13e | several overlapping `Room` boxes of different sizes in one space | Room boxes are huge and nested; weak ones survive NMS at conf 0.25 (visible in the grid). Inconsistent room labelling (sub-areas vs whole room) in the training data. | Errors in detecting stairs. |

## Three false negatives (model misses a real object)
| # | Image | What was missed | Likely cause (hypothesis) |
|---|---|---|---|
| FP_11358_png_jpg.rf.3bd99770d0817ea25605ffb0e0e1be3f | `Stairs` (recall 0.23, 14 of 40 found at best) | Only 40 stair instances and large style variation (hand-drawn vs CAD). |
| FP_665_png_jpg.rf.a1ebe8395ea303f0a231f16cb94008bd | `Walls` (3 instances, recall 0) | Walls are long thin structures; one box cannot represent them and there are almost no examples. |
| FN_712_png_jpg.rf.fb7dbc6fd4224a4539c85ffc54f7a13e | `Window` in old scanned or hand-drawn plans (recall 0.52) | Low-contrast scans, yellowed paper and hand-drawn symbols differ from the clean CAD plans in training; 640 px input shrinks thin symbols. |

## Three prioritised data improvements
| Priority | Concrete action | Gap it fixes | Success measure |
|---|---|---|---|
| 1 | Audit and fix labels: merge `Furnitures` into `Furniture`, define "Furniture" and "Room" rules in writing, add missing labels (review the 6 worst FP images), convert the 2 mixed polygon/box files to boxes | FP1, FP3 (precision about 0.5) | Furniture precision from 0.29 to above 0.5; fewer duplicate Room boxes |
| 2 | Add 40-60 labelled stair and 30+ hard window examples from different plan styles (scans, hand-drawn) plus 10-15 background images with hatching and dimension lines | FN1, FN3, FP2 | Stairs recall from 0.23 to above 0.5; Window precision from 0.50 to above 0.65 |
| 3 | Enlarge the validation set to 50+ images split by source plan (no near-duplicate augmentations across splits) and drop or redefine `Walls` | noisy 23-image metric; Walls = 3 instances | mAP50 varies less than 0.03 between two seeds |
