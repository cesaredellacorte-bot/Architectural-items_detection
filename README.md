# YOLOv11 Object Detection

**Objective:** train a custom object-detection model with [YOLOv11](https://github.com/ultralytics/ultralytics) that can recognize specific objects of interest in images. This repo is built so anyone can reproduce the exact same result — the dataset, training process, and evaluation are all automated and verifiable, not just described.

**What it does:**
1. Downloads the training dataset automatically from Google Drive, and verifies it hasn't been altered or corrupted using a SHA256 checksum
2. Trains a YOLOv11 model on that dataset
3. Evaluates the model and saves performance curves and prediction samples
4. Runs the trained model on new images

**Who it's for:** anyone who wants to reproduce this specific detection model, fine-tune it further, or use this repo as a template for training YOLOv11 on their own dataset. No GitHub or machine-learning experience is required to run it — see Usage below.

Everything runs through the [Ultralytics](https://docs.ultralytics.com/) library.

## Requirements

- Python 3.9+
- pip

## Installation

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME
pip install -r requirements.txt
```

## Dataset

This repository does not include the dataset itself (image datasets are too large for GitHub) — instead, it's hosted on Google Drive and `main.py` downloads and verifies it automatically.

### For anyone using this repo (no setup needed)

You don't have to do anything manually. Either:

- **Double-click** `setup_and_download.bat` (Windows) or `setup_and_download.command` (Mac/Linux), **or**
- Just run `python main.py` directly — it downloads the dataset automatically before training if it isn't there yet.

Either way, the dataset is fetched from Google Drive, its integrity is verified, and it's unzipped into `./dataset/` — reused on every run after that.

### For the repo owner: pointing this at your own dataset

1. Zip your dataset folder (the one containing `images/` and `labels/`) into a single `.zip` file.
2. Upload that zip to Google Drive.
3. Right-click it in Drive → **Share** → change access to **"Anyone with the link"** → Viewer.
4. Copy the link — it looks like `https://drive.google.com/file/d/1AbCdEf.../view?usp=sharing`. The long string between `/d/` and `/view` is the **file ID**.
5. Open `main.py` and paste that file ID into the `GOOGLE_DRIVE_FILE_ID` variable near the top. (Already done for the dataset you gave me: `1iVq3qa_xrTHb422iZmxqrK1AS8E2h0La`.)
6. Commit and push. From now on, anyone who clones the repo gets your dataset automatically.

### Verifying dataset integrity (SHA256 checksum)

Every time the dataset is downloaded, `main.py` computes its **SHA256 checksum** — a fingerprint that proves the file downloaded later is byte-for-byte identical to the one originally uploaded (and trained on).

- The checksum is printed after every download, and saved to `dataset/CHECKSUM.sha256`.
- **Recommended:** the first time you download it successfully, copy that printed checksum into the `EXPECTED_SHA256` variable in `main.py`, then commit and push. After that, every future download is automatically checked against it — if the file on Google Drive is ever accidentally replaced or corrupted, `main.py` detects the mismatch and stops before extracting it.
- To check by hand: Windows (PowerShell) `Get-FileHash dataset_download.zip -Algorithm SHA256`; Mac/Linux `shasum -a 256 dataset_download.zip`.

### Manual dataset setup (alternative)

If you'd rather use your own local dataset instead of the Google Drive download, organize it in the standard YOLO format:

```
dataset/
├── images/
│   ├── train/
│   └── val/
└── labels/
    ├── train/
    └── val/
```

Each `.txt` label file has one line per object: `class_id x_center y_center width height` (normalized between 0 and 1). Then copy the config template and edit it:

```bash
cp data.yaml.example data.yaml
```

## Usage

`main.py` has three modes, controlled with `--mode`:

```bash
# Only download + verify the dataset
python main.py --mode download

# Train (this is the default mode -- downloads the dataset automatically if missing)
python main.py
python main.py --mode train --epochs 50 --imgsz 640 --model yolo11n.pt

# Run inference with a trained model
python main.py --mode detect --source path/to/image_or_folder
python main.py --mode detect --weights runs/train/exp/weights/best.pt --source path/to/images --conf 0.25
```

Common options:

| Flag         | Description                                                | Default        | Used in mode      |
|--------------|-------------------------------------------------------------|-----------------|--------------------|
| `--mode`     | `download`, `train`, or `detect`                             | `train`         | all                |
| `--data`     | Path to your dataset YAML                                    | `data.yaml`     | train              |
| `--model`    | Base model (`yolo11n/s/m/l/x.pt`) or checkpoint               | `yolo11n.pt`    | train, detect      |
| `--epochs`   | Number of training epochs                                    | `100`           | train              |
| `--imgsz`    | Image size                                                    | `640`           | train              |
| `--batch`    | Batch size                                                    | `16`            | train              |
| `--device`   | `''` (auto), `0`, `0,1`, or `cpu`                             | auto            | train              |
| `--weights`  | Trained weights to use                                        | best.pt if found | detect           |
| `--source`   | Image, folder, video, or `0` for webcam (**required**)        | —               | detect             |
| `--conf`     | Confidence threshold                                          | `0.25`          | detect             |

Model weights (`yolo11n.pt`, etc.) download automatically the first time you run this. Training results (weights, metrics, plots) are saved to `runs/train/exp/`.

## Notebooks

For a guided, step-by-step walkthrough instead of the command line, see `notebooks/`:

- `01_baseline.ipynb` — runs the stock pretrained model as a reference point, before any training
- `02_training_eval.ipynb` — trains, evaluates, and saves curves/prediction samples into `results/`

## Project structure

```
.
├── main.py                       # Single entry point: download, train, and detect
├── setup_and_download.bat        # Windows one-click setup (installs deps + downloads dataset)
├── setup_and_download.command    # Mac/Linux one-click setup
├── data.yaml.example             # Dataset config template (copy -> data.yaml)
├── requirements.txt               # Python dependencies
├── README.md
│
├── notebooks/
│   ├── 01_baseline.ipynb          # Pretrained model, no training -- reference point
│   └── 02_training_eval.ipynb     # Fine-tuning + evaluation + saves results/
│
├── docs/
│   ├── problem_statement.md       # What problem this solves, dataset overview, scope
│   ├── class_definitions.md       # What each class means, labeling edge cases
│   ├── error_analysis.md          # Failure modes, root causes, next steps
│   └── governance.md              # Data provenance, licensing, limitations, monitoring
│
└── results/
    ├── curves/                    # Training curves, confusion matrix, PR/F1 curves
    └── samples/                   # Annotated prediction images (baseline vs fine-tuned)
```

## License

MIT License

Copyright (c) 2026 cesaredellacorte-bot
