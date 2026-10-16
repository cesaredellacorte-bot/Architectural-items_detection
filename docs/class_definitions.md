# Class definitions and labelling rules

**General rule (author):** each box contains only the basic lines that identify the element, with no surrounding context.
Final class ids after cleaning (`scripts/prepare_dataset.py` merges `Furnitures` into `Furniture`; `Walls` is kept):

| ID | Class | Box contains | Validation instances (first run) | Note |
|---|---|---|---|---|
| 0 | Door | the lines that draw the door (leaf, and arc if drawn) | 249 | works best among small classes |
| 1 | Furniture | the lines of the furniture/fixture symbol | 259 | lowest precision: symbols are varied and ambiguous |
| 2 | Room | the outline of the space | 272 | large boxes that overlap other classes |
| 3 | Stairs | the lines of the stair run | 40 | under-represented |
| 4 | Walls | the lines of the wall | 3 | kept by choice; too few examples to learn |
| 5 | Window | the lines of the window symbol | 221 | |

Annotation tool: Roboflow. Source images: subset of the public Roboflow Universe dataset cad-drawings (MIT); all six classes were labelled by the author, so labelling is consistent by one annotator (no inter-annotator check).
