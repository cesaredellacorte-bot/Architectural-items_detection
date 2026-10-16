"""Helpers that produce every artefact the M4U3 assignment asks for.

Used by notebooks/02_train_eval.ipynb, but each function also works standalone.
"""
import csv
import datetime as dt
import glob
import os
import platform
import random
import shutil
import subprocess
import sys

IMG_EXT = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


# ------------------------------------------------------------------ geometry (pure, unit-testable)
def xywhn_to_xyxy(b, w, h):
    cx, cy, bw, bh = b
    return [(cx - bw / 2) * w, (cy - bh / 2) * h, (cx + bw / 2) * w, (cy + bh / 2) * h]


def iou(a, b):
    ix0, iy0, ix1, iy1 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    inter = max(0.0, ix1 - ix0) * max(0.0, iy1 - iy0)
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union if union > 0 else 0.0


def match(preds, gts, iou_thr=0.5):
    """preds: [(cls, conf, xyxy)], gts: [(cls, xyxy)].
    Greedy match by confidence. Returns (fp_indices, fn_indices, tp_count).
    A prediction with the right box but wrong class counts as BOTH an FP and an FN."""
    used, fp, tp = set(), [], 0
    for i, (pc, _conf, pb) in sorted(enumerate(preds), key=lambda t: -t[1][1]):
        best, best_j = 0.0, -1
        for j, (gc, gb) in enumerate(gts):
            if j in used or gc != pc:
                continue
            v = iou(pb, gb)
            if v > best:
                best, best_j = v, j
        if best >= iou_thr:
            used.add(best_j)
            tp += 1
        else:
            fp.append(i)
    fn = [j for j in range(len(gts)) if j not in used]
    return fp, fn, tp


# ------------------------------------------------------------------ metrics table
def metrics_table(model, data_yaml, split="val", imgsz=640, out_dir="results"):
    """Run validation and save a Markdown + CSV table: overall and per-class P / R / mAP50 / mAP50-95."""
    os.makedirs(out_dir, exist_ok=True)
    m = model.val(data=data_yaml, split=split, imgsz=imgsz, plots=True, project=out_dir, name=f"val_{split}", exist_ok=True)
    rows = [("ALL", m.box.mp, m.box.mr, m.box.map50, m.box.map)]
    for k, ci in enumerate(m.box.ap_class_index):
        p, r, ap50, ap = m.box.class_result(k)
        rows.append((m.names[int(ci)], p, r, ap50, ap))
    with open(os.path.join(out_dir, "metrics.csv"), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["class", "precision", "recall", "mAP50", "mAP50-95"])
        wr.writerows([(n, *(round(float(x), 4) for x in v)) for n, *v in rows])
    md = "| Class | Precision | Recall | mAP50 | mAP50-95 |\n|---|---|---|---|---|\n"
    md += "\n".join(f"| {n} | {p:.3f} | {r:.3f} | {a:.3f} | {b:.3f} |" for n, p, r, a, b in rows)
    open(os.path.join(out_dir, "metrics.md"), "w").write(md + "\n")
    print(md)
    return rows


# ------------------------------------------------------------------ curves
def copy_curves(run_dir, out_dir="results/curves"):
    os.makedirs(out_dir, exist_ok=True)
    wanted = ["results.png", "results.csv", "confusion_matrix.png", "confusion_matrix_normalized.png",
              "BoxPR_curve.png", "BoxF1_curve.png", "BoxP_curve.png", "BoxR_curve.png",
              "PR_curve.png", "F1_curve.png", "P_curve.png", "R_curve.png", "labels.jpg", "args.yaml"]
    copied = []
    for n in wanted:
        p = os.path.join(run_dir, n)
        if os.path.exists(p):
            shutil.copy(p, out_dir)
            copied.append(n)
    print("Copied:", copied)


# ------------------------------------------------------------------ evidence images
def _pick(paths, n, seed=0):
    paths = sorted(paths)
    random.Random(seed).shuffle(paths)
    return paths[:n]


def save_annotation_examples(img_dir, lbl_dir, names, n=5, out_dir="results/evidence/annotations", seed=0):
    """Draw ground-truth boxes on n random images (screenshots of your annotations)."""
    import cv2
    os.makedirs(out_dir, exist_ok=True)
    imgs = [p for p in glob.glob(os.path.join(img_dir, "*")) if p.lower().endswith(IMG_EXT)]
    for p in _pick(imgs, n, seed):
        im = cv2.imread(p)
        h, w = im.shape[:2]
        lp = os.path.join(lbl_dir, os.path.splitext(os.path.basename(p))[0] + ".txt")
        if os.path.exists(lp):
            for line in open(lp).read().splitlines():
                t = line.split()
                if len(t) < 5:
                    continue
                c = int(float(t[0]))
                vals = [float(v) for v in t[1:]]
                if len(vals) > 4:  # polygon row -> box
                    xs, ys = vals[0::2], vals[1::2]
                    vals = [(min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, max(xs) - min(xs), max(ys) - min(ys)]
                x0, y0, x1, y1 = map(int, xywhn_to_xyxy(vals[:4], w, h))
                col = _color(c)
                cv2.rectangle(im, (x0, y0), (x1, y1), col, 2)
                cv2.putText(im, str(names[c]), (x0, max(12, y0 - 4)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, col, 1)
        cv2.imwrite(os.path.join(out_dir, os.path.basename(p)), im)
    print(f"Saved {n} annotation examples to {out_dir}")


def _color(c):
    pal = [(66, 135, 245), (60, 180, 75), (245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230), (210, 245, 60)]
    return pal[c % len(pal)]


def save_predictions(model, src_dir, n, out_dir, conf=0.25, imgsz=640, seed=0):
    """Predict on n images from src_dir and save annotated copies (used for val AND new images)."""
    os.makedirs(out_dir, exist_ok=True)
    imgs = [p for p in glob.glob(os.path.join(src_dir, "*")) if p.lower().endswith(IMG_EXT)]
    if not imgs:
        print(f"[!] No images found in {src_dir}")
        return
    chosen = _pick(imgs, n, seed)
    for p in chosen:
        r = model.predict(p, conf=conf, imgsz=imgsz, verbose=False)[0]
        r.save(filename=os.path.join(out_dir, os.path.basename(p)))
    print(f"Saved {len(chosen)} predictions to {out_dir}")


# ------------------------------------------------------------------ error analysis helper
def find_errors(model, img_dir, lbl_dir, names, conf=0.25, imgsz=640, iou_thr=0.5, top=8,
                out_dir="results/evidence/errors"):
    """Rank validation images by number of FP and FN, save annotated versions
    (RED = false positive, BLUE = false negative) so you can pick 3 + 3 for docs/error_analysis.md."""
    import cv2
    os.makedirs(out_dir, exist_ok=True)
    stats = []
    for p in glob.glob(os.path.join(img_dir, "*")):
        if not p.lower().endswith(IMG_EXT):
            continue
        im = cv2.imread(p)
        h, w = im.shape[:2]
        gts = []
        lp = os.path.join(lbl_dir, os.path.splitext(os.path.basename(p))[0] + ".txt")
        if os.path.exists(lp):
            for line in open(lp).read().splitlines():
                t = line.split()
                if len(t) == 5:
                    gts.append((int(float(t[0])), xywhn_to_xyxy([float(v) for v in t[1:]], w, h)))
        r = model.predict(p, conf=conf, imgsz=imgsz, verbose=False)[0]
        preds = [(int(c), float(s), b) for c, s, b in zip(r.boxes.cls.tolist(), r.boxes.conf.tolist(), r.boxes.xyxy.tolist())]
        fp, fn, tp = match(preds, gts, iou_thr)
        stats.append((p, im, preds, gts, fp, fn, tp))
    by_fp = sorted(stats, key=lambda s: -len(s[4]))[:top]
    by_fn = sorted(stats, key=lambda s: -len(s[5]))[:top]
    report = []
    for tag, group in (("FP", by_fp), ("FN", by_fn)):
        for p, im, preds, gts, fp, fn, tp in group:
            vis = im.copy()
            for i in fp:
                c, s, b = preds[i]
                cv2.rectangle(vis, tuple(map(int, b[:2])), tuple(map(int, b[2:])), (0, 0, 255), 2)
                cv2.putText(vis, f"FP {names[c]} {s:.2f}", (int(b[0]), max(12, int(b[1]) - 4)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            for j in fn:
                c, b = gts[j]
                cv2.rectangle(vis, tuple(map(int, b[:2])), tuple(map(int, b[2:])), (255, 0, 0), 2)
                cv2.putText(vis, f"FN {names[c]}", (int(b[0]), max(12, int(b[1]) - 4)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            fn_out = f"{tag}_{os.path.basename(p)}"
            cv2.imwrite(os.path.join(out_dir, fn_out), vis)
            report.append((tag, os.path.basename(p), len(fp), len(fn), tp))
    for row in report:
        print("%s  %-60s FP=%d FN=%d TP=%d" % row)
    return report


# ------------------------------------------------------------------ reproducibility proof
def write_run_info(path="results/run_info.md", extra=None):
    """Writes the facts the 'Reproducibility Proof' note needs: timestamp, hardware, versions, runtime."""
    import ultralytics
    try:
        import torch
        gpu = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU only"
        tv = torch.__version__
    except Exception:
        gpu, tv = "unknown", "unknown"
    pip = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True).stdout.splitlines()
    key = [l for l in pip if l.split("==")[0].lower() in ("ultralytics", "torch", "torchvision", "opencv-python", "numpy", "roboflow", "pandas")]
    lines = ["# Reproducibility proof (auto-generated)", "",
             f"- Last successful run: {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
             f"- Hardware: {gpu}", f"- Python: {platform.python_version()}",
             f"- ultralytics: {ultralytics.__version__}", f"- torch: {tv}"]
    for k, v in (extra or {}).items():
        lines.append(f"- {k}: {v}")
    lines += ["", "```", *key, "```", ""]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write("\n".join(lines))
    print("\n".join(lines))
