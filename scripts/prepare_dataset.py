"""Clean a YOLO dataset before training: merge duplicate classes, convert polygon rows to boxes,
remove duplicate / degenerate boxes, compact class ids, write data_fixed.yaml.
Keeps the original train/valid split (assignment: 80/20)."""
import glob
import os
from collections import Counter

import yaml


def _poly_to_box(v):
    xs, ys = v[0::2], v[1::2]
    return [(min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, max(xs) - min(xs), max(ys) - min(ys)]


def prepare(root, merge=None, train="train", val="valid"):
    merge = merge or {}
    cfg = yaml.safe_load(open(os.path.join(root, "data.yaml")))
    names = cfg["names"]
    names = [names[i] for i in sorted(names)] if isinstance(names, dict) else list(names)
    new_names = []
    for n in names:
        t = merge.get(n, n)
        if t not in new_names:
            new_names.append(t)
    id_map = {i: new_names.index(merge.get(n, n)) for i, n in enumerate(names)}
    stats = Counter()
    for split in (train, val):
        for lp in glob.glob(os.path.join(root, split, "labels", "*.txt")):
            rows, seen = [], set()
            for line in open(lp).read().splitlines():
                p = line.split()
                if len(p) < 5:
                    continue
                try:
                    c, v = int(float(p[0])), [float(x) for x in p[1:]]
                except ValueError:
                    continue
                if c not in id_map:
                    continue
                if len(v) == 4:
                    b = v
                elif len(v) >= 6 and len(v) % 2 == 0:
                    b = _poly_to_box(v); stats["polygons_converted"] += 1
                else:
                    stats["rows_dropped"] += 1; continue
                b = [min(max(x, 0.0), 1.0) for x in b]
                if b[2] <= 0.002 or b[3] <= 0.002:
                    stats["rows_dropped"] += 1; continue
                key = (id_map[c], *[round(x, 4) for x in b])
                if key in seen:
                    stats["duplicates_removed"] += 1; continue
                seen.add(key)
                if id_map[c] != c:
                    stats["ids_remapped"] += 1
                rows.append(f"{id_map[c]} " + " ".join(f"{x:.6f}" for x in b))
            open(lp, "w").write("\n".join(rows))
    out = {"path": root, "train": f"{train}/images", "val": f"{val}/images",
           "names": {i: n for i, n in enumerate(new_names)}}
    path = os.path.join(root, "data_fixed.yaml")
    yaml.safe_dump(out, open(path, "w"), sort_keys=False)
    print("Classes:", new_names, "| changes:", dict(stats))
    return path, new_names
