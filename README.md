# Architectural-items_detection - detecting doors, windows, furniture, stairs, rooms and walls in plan views (AECO)

> Author: **Cesare Della Corte** (individual work) · Course: M4U3 · Last updated: 17/10/2026
> Slides: [pdf_pack/slides.pdf](pdf_pack/slides.pdf) · Mini report: [pdf_pack/mini_report.pdf](pdf_pack/mini_report.pdf)

## 1. Problem and success criteria
**Problem (AECO):** Identifying architectural elements (doors, windows, furniture, stairs, rooms, walls) on plan views is done by hand. This project trains an object detector (YOLO) to recognise these elements in floor-plan images, as a first step towards a workflow for fast, automatic recognition of architectural elements (for example quantity take-off or plan review). The plans are heterogeneous (scanned, hand-drawn, CAD exports; Finnish-language labels such as KERROS, KT, OH).

**Success criteria (proposed - edit to your own)**
- Main classes (Door, Window, Room): mAP50 >= 0.60 and recall >= 0.60 on the validation split
- Inference < 0.1 s per image on a free Colab T4 GPU (measured: about 12 ms end to end)
- Failures are understood and a data-improvement plan exists ([docs/error_analysis.md](docs/error_analysis.md))

## 2. Classes and label rules
| ID | Class | Validation instances (first run) |
|---|---|---|
| 0 | Door | 249 |
| 1 | Furniture (merged with the duplicate class `Furnitures`) | 259 |
| 2 | Room | 272 |
| 3 | Stairs | 40 |
| 4 | Walls (kept, but very rare: 3 instances) | 3 |
| 5 | Window | 221 |

**Label rule (all classes):** the box contains only the basic lines that identify the element, with no surrounding context. Full definitions: [docs/class_definitions.md](docs/class_definitions.md). The cleaning step (`scripts/prepare_dataset.py`) merges `Furnitures` into `Furniture`, converts polygon rows to boxes and removes duplicate boxes.

## 3. Dataset
- Dataset zip (YOLO format, Roboflow export): https://drive.google.com/file/d/1iVq3qa_xrTHb422iZmxqrK1AS8E2h0La/view?usp=sharing (public copy of Roboflow version 2)
- Roboflow project: https://app.roboflow.com/cesare-della-corte/architectural_items_detection_v1/2 (workspace `cesare-della-corte`, project `architectural_items_detection_v1`, **version 2**). The link needs a Roboflow login, so the Drive zip above is the public copy used by the notebook.
- **Origin:** a small subset (about 110 images) cloned from the public Roboflow Universe dataset [cad-drawings](https://universe.roboflow.com/train-yu3wc/cad-drawings) (2,587 images, original classes door / window / zone, MIT licence). The author **re-annotated the images with six own classes** (Door, Furniture, Room, Stairs, Walls, Window) and made the train/valid split. The original labels were not used as they are. Citation and licence: section 8.
- Split: train 88 images (87 usable) / valid 24 images (23 usable) = **about 80 / 20**
- Two label files mix polygon and box rows and were skipped by Ultralytics (1 train, 1 val).
- Rights: public images (MIT) with the author's own annotations; see section 8.

## 4. How to reproduce (Google Colab, no local install)
1. Open [`notebooks/02_train_eval.ipynb`](https://colab.research.google.com/github/cesaredellacorte-bot/Architectural-items_detection/blob/main/notebooks/02_train_eval.ipynb)
2. Runtime -> Change runtime type -> **T4 GPU**
3. Nothing to edit: `DATA_SOURCE="gdrive"` downloads the dataset automatically (no key needed).
4. **Runtime -> Restart runtime -> Run all** (about 3-6 min on a T4 including setup; training itself took 1.6 min)
5. Expected outputs: training curves, metrics table, `results/` evidence images, `results/run_info.md`
No GPU? Set `FAST_VERIFY = True`: it runs 5 epochs and loads the real weights from the release below.

**Weights:** (https://github.com/cesaredellacorte-bot/Architectural-items_detection/releases/tag/v1.0): GitHub Release link to `best.pt`
Baseline (pretrained, no fine-tuning): [`notebooks/01_baseline_inference.ipynb`](notebooks/01_baseline_inference.ipynb)

## 5. Results summary (validation split, 23 images, 1044 instances)

| Class | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| ALL | 0.587 | 0.428 | 0.396 | 0.247 |
| Door | 0.652 | 0.697 | 0.723 | 0.449 |
| Furniture | 0.340 | 0.400 | 0.276 | 0.170 |
| Room | 0.603 | 0.787 | 0.740 | 0.526 |
| Stairs | 0.397 | 0.250 | 0.210 | 0.133 |
| Walls | 1.000 | 0.000 | 0.003 | 0.002 |
| Window | 0.530 | 0.433 | 0.425 | 0.202 |

Curves: ![curves](results/curves/results.png) · [metrics.md](results/metrics.md) · [evidence](results/evidence/)

**Key takeaways**
1. Large, distinctive objects work best: Room (mAP50 0.75) and Door (0.71), with high recall (0.84 / 0.78).
2. Precision is the weak point for most classes (about 0.5): many low-confidence duplicate or overlapping boxes, especially Furniture (P 0.29) and Window. Stairs and Walls are the opposite problem: too few examples (40 and 3), so recall is 0.23 and 0.
3. The model is **under-trained and data-limited**: all curves were still improving at epoch 50 (mAP50 0.39 and rising), and the validation set is only 23 images, so the numbers are noisy. More and cleaner data matters more than a bigger model.

## 6. Reproducibility checklist
- [ ] Dataset: Google Drive zip `1iVq3qa_xrTHb422iZmxqrK1AS8E2h0La` (Roboflow export), train/valid about 80/20 - Roboflow version 2
- [ ] Model variant: yolov8n.pt - the run above used `yolo11n.pt`; the assignment asks for YOLOv8, so re-run with `yolov8n.pt` (notebook default) and update the numbers above
- [ ] Epochs / batch / imgsz: `50 / 16 / 640`, seed `0`
- [ ] Ultralytics version: `8.4.163` (pinned in `requirements.txt`; Python 3.13, torch 2.11, T4)
- [ ] Weights available at: (https://github.com/cesaredellacorte-bot/Architectural-items_detection/releases/tag/v1.0)
- [ ] Notebook opens from GitHub and runs end-to-end after "Restart runtime -> Run all"

### Reproducibility proof
- Last successful run: 2026-10-17 15:33 UTC (the original run was on Colab, Tesla T4, 15 GB)
- Hardware: Tesla T4 GPU (Colab)
- Expected runtime: about 2 min training (50 epochs) + about 2-4 min setup and download
- Mode: full training

## 7. Documentation
[Class definitions](docs/class_definitions.md) · [Error analysis](docs/error_analysis.md) · [Governance checklist](docs/governance_checklist.md) · [SAM notes](docs/sam_notes.md)

## 8. Licence and data rights
- **Code:** MIT (see [LICENSE](LICENSE)), copyright Cesare Della Corte.
- **Dataset:** images from one public Roboflow Universe dataset; labels by the author. The images come from a single source, below, licensed MIT: reuse and redistribution are allowed if the copyright notice is kept and the source is cited. The annotations (6 classes) were created by the author. Code and annotations are released under MIT.

| Source dataset | URL | Licence |
|---|---|---|
| "cad drawings Dataset" by `train` (Roboflow Universe, Mar 2024) | https://universe.roboflow.com/train-yu3wc/cad-drawings | MIT (per the dataset page, checked 2026-10-16) |
- **Pretrained weights:** Ultralytics models are AGPL-3.0; check obligations for commercial use.

### Dataset citation
```
@misc{ cad-drawings_dataset,
  title = { cad drawings Dataset },
  type = { Open Source Dataset },
  author = { train },
  howpublished = { \url{ https://universe.roboflow.com/train-yu3wc/cad-drawings } },
  url = { https://universe.roboflow.com/train-yu3wc/cad-drawings },
  journal = { Roboflow Universe },
  publisher = { Roboflow },
  year = { 2024 },
  month = { mar },
  note = { visited on 2026-10-16 },
}
```
