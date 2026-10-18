# Reproducibility proof

## A. Full training run (produced `best.pt` v1.0, curves and metrics in this folder)
- Run: 2026-10-17, Google Colab, **Tesla T4** (15 GB)
- Python 3.13.15 · ultralytics 8.4.163 · torch 2.11.0+cu130
- Dataset: `cesare-della-corte/architectural_items_detection_v1` **v2** (same file as Release `dataset-v2`)
- Model / epochs / batch / imgsz / seed: `yolov8n.pt` / 50 / 16 / 640 / 0
- Training time: 86 s for 50 epochs (`curves/results.csv`) · total notebook runtime: about 2.4 min plus setup
- Output weights: Release `v1.0` → `best.pt`, SHA256 `65b7d90e13729e141e74d8871b8139fb27b51d93822a82c87e24a27876a3b571`

## B. Independent end-to-end verification (fresh machine, frozen data)
- Run: 2026-10-18 20:55 UTC, clean Linux machine, **CPU only**, `notebooks/02_train_eval.ipynb` executed top to bottom with `FAST_VERIFY = True`
- Python 3.13.16 · ultralytics 8.4.163 · torch 2.14.1
- Dataset zip SHA256 measured: `7e70aedcd900e5e7c4e0b7993dc7d33c736a4eaeeb239296382a768afdb2cb48` = expected ✅
- Released weights SHA256 measured: `65b7d90e…a3b571` = expected ✅
- Cleaning step: 7 → 6 classes (`Furnitures` → `Furniture`, 2,567 ids remapped), 3 polygon rows converted, 1 duplicate removed
- **Validation metrics reproduced exactly:** all classes P 0.587 · R 0.428 · mAP50 0.396 · mAP50-95 0.247 (24 images, 1135 instances), identical to `metrics.md`
- Runtime: 5.2 min on CPU (5 smoke-test epochs + evaluation + evidence)

Full parameter and version record: [`params.yaml`](params.yaml)
