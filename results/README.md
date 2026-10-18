# results/

| What | Where |
|---|---|
| Training curves (loss, P, R, mAP per epoch) | [`curves/results.png`](curves/results.png), raw [`curves/results.csv`](curves/results.csv) |
| PR / F1 / P / R curves, confusion matrix | [`curves/`](curves/) |
| Metrics table (P, R, mAP50, mAP50-95, per class) | [`metrics.md`](metrics.md) · [`metrics.csv`](metrics.csv) |
| 10 validation predictions (+ batch grid) | [`evidence/val_predictions/`](evidence/val_predictions/) |
| 5 annotation screenshots (ground truth) | [`evidence/annotations/`](evidence/annotations/) |
| 5 predictions on new, unlabelled plans | [`evidence/new_predictions/`](evidence/new_predictions/) |
| FP / FN images for the error analysis | [`evidence/errors/`](evidence/errors/) |
| Versions, parameters, hashes | [`run_info.md`](run_info.md) · [`params.yaml`](params.yaml) |

All of these are produced by [`notebooks/02_train_eval.ipynb`](../notebooks/02_train_eval.ipynb) (cells 5-8).

## Metrics (validation split, 24 images, 1135 instances, released `best.pt`)

| Class | Instances | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|---|
| **ALL** | 1135 | 0.587 | 0.428 | 0.396 | 0.247 |
| Door | 269 | 0.652 | 0.697 | 0.723 | 0.449 |
| Furniture | 270 | 0.340 | 0.400 | 0.276 | 0.170 |
| Room | 293 | 0.603 | 0.787 | 0.740 | 0.526 |
| Stairs | 40 | 0.397 | 0.250 | 0.210 | 0.133 |
| Walls | 16 | 1.000* | 0.000 | 0.003 | 0.002 |
| Window | 247 | 0.530 | 0.433 | 0.425 | 0.202 |

\* Walls: P = 1.000 is not meaningful. The model makes (almost) no Walls predictions above threshold, and Ultralytics then reports precision as 1. Recall 0 shows the class is not learned.

![training curves](curves/results.png)
