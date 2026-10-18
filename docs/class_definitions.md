# Class definitions and labelling rules

**Dataset:** Roboflow project `cesare-della-corte/architectural_items_detection_v1`, **version 2**. It is frozen as GitHub Release [`dataset-v2`](https://github.com/cesaredellacorte-bot/Architectural-items_detection/releases/tag/dataset-v2), SHA256 `7e70aedcd900e5e7c4e0b7993dc7d33c736a4eaeeb239296382a768afdb2cb48`.
**Annotation tool:** Roboflow (boxes drawn by hand, plus the Roboflow label assistant; every box was checked by the author).
**Annotator:** one person (the author). Labelling is consistent within one annotator, but no second annotator checked it.

## General rule (all classes)
Each box is the **tightest axis-aligned rectangle around the drawn lines of the element**. It holds only the lines that identify the element and no surrounding context: no text labels, no dimension lines, no hatching outside the element.
Label an element when at least about 50% of it is visible and you can recognise it without guessing. When unsure, do **not** label it, and write it down for review.

## Final classes (after cleaning)

| ID | Class | Draw the box around | Include | Exclude | Train / Valid instances* |
|---|---|---|---|---|---|
| 0 | **Door** | the door leaf **and its swing arc** (or the sliding leaf) | single, double, sliding and folding doors | empty wall openings with no leaf drawn; garage doors drawn as dashed lines only | 1011 / 269 |
| 1 | **Furniture** | one movable or fixed furniture / sanitary / kitchen symbol | beds, tables, sofas, wardrobes, WC, basin, shower, bathtub, sauna bench, stove, fridge, kitchen counter units | built-in walls, stairs, room text, hatching | 1043 / 270 |
| 2 | **Room** | the inner outline of one enclosed space (wall face to wall face) | rooms, corridors, balconies or terraces only when they are enclosed on 3+ sides | the whole building outline; sub-zones inside a room (for example a kitchen corner inside a living room) | 1023 / 293 |
| 3 | **Stairs** | the whole stair run, including all treads and the landing drawn with it | straight, L-shaped and spiral stairs; external steps of 3+ treads | handrail-only lines; ramps | 113 / 40 |
| 4 | **Walls** | one straight wall segment | thick (structural) walls drawn as filled or double lines | thin partition lines inside furniture | 131 / 16 |
| 5 | **Window** | the window symbol inside the wall (the 2-3 parallel lines across the wall thickness) | windows, glazed doors' fixed side panes, roof windows | doors; wall openings with no glazing lines | 687 / 247 |

\* Counts after `scripts/prepare_dataset.py` (merge + polygon-to-box conversion + duplicate removal) on dataset v2. Test split (12 images): not used for training or for the metrics in the README.

## Fix: `Furniture` / `Furnitures` (duplicate class)
The Roboflow v2 export has **7** class names: `['Door', 'Furniture', 'Furnitures', 'Room', 'Stairs', 'Walls', 'Window']`.
`Furnitures` (raw id 2) is a typo duplicate of `Furniture` (raw id 1), created by mistake while labelling. It has only 12 train + 5 valid boxes, and they show the same symbols as `Furniture`.

| Raw id (Roboflow export) | Raw name | Final id | Final name |
|---|---|---|---|
| 0 | Door | 0 | Door |
| 1 | Furniture | 1 | Furniture |
| **2** | **Furnitures** | **1** | **Furniture** (merged) |
| 3 | Room | 2 | Room |
| 4 | Stairs | 3 | Stairs |
| 5 | Walls | 4 | Walls |
| 6 | Window | 5 | Window |

**How it is fixed:** the notebook calls `prepare_dataset.prepare(root, merge={"Furnitures": "Furniture"})`. This rewrites every label file with the new ids and writes `data_fixed.yaml` with **6** classes. The frozen zip stays exactly as exported, so its SHA256 still matches, and the fix can be reproduced in code.
**Permanent fix (next dataset version):** in Roboflow, use Classes -> rename `Furnitures` to `Furniture` (this merges them), then generate version 3 and freeze it as a new release.

## Other cleaning applied
- 2 label files mix polygon rows and box rows (`5568_png...` in train, `5531_png...` in valid). The polygon rows are converted to their bounding box, so Ultralytics no longer skips these files.
- Exact duplicate boxes are removed, and boxes smaller than 0.2% of the image are dropped.

## Known ambiguities (to resolve in v3)
- **Room vs Furniture:** large kitchen blocks and saunas were sometimes boxed as Room.
- **Stairs vs Furniture:** the model confuses them (see error analysis, FP-2). Rule: parallel treads plus an arrow or a break line means Stairs.
- **Walls:** a box is a poor shape for long thin walls, and only a few walls are labelled. Either label every wall segment or drop the class (see error analysis, improvement 3).
