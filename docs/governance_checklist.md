# Governance checklist (one page)
Items marked **TODO(you)** need your real answer. Do not leave "N/A".

## 1. Privacy and consent
- [ ] Floor plans contain no personal data (owner names, addresses, signatures, plot numbers): **TODO(you): checked by / date**. The sample images show Finnish-language labels and some title-block text - blur or crop those if they identify people or properties.
- [ ] Source of every image: one public Roboflow Universe dataset (cad-drawings, subset); annotations created by the author. Main source: Roboflow Universe `train-yu3wc/cad-drawings`, licence MIT (checked 2026-10-16).
- [ ] No Roboflow / Google API keys committed (use Colab Secrets)
- [ ] Dataset visibility: public source dataset (cad-drawings, MIT); my Drive zip link is share-by-link

## 2. Data minimisation
- [ ] Only task-relevant images used (about 110 images, annotated for 6 classes)
- [ ] Title blocks, stamps and metadata removed or blurred: **TODO(you)**
- [ ] Retention: dataset reviewed or deleted at project end (**TODO(you): date**)

## 3. Limitations statement (when NOT to use this model)
- Trained on about 110 plans of limited styles (mostly Finnish residential plans); not validated on other countries, scales, drawing standards or non-residential buildings.
- Overall mAP50 is 0.39: it is a **first-pass assistant**, not a measuring tool. Do not use its counts for quotations, permits, compliance or fire-safety decisions without human verification.
- Unreliable for Stairs (recall 0.23), Furniture (precision 0.29) and Walls (not supported).
- Expect worse results on low-contrast scans and hand-drawn plans.

## 4. Risk note: false negatives vs false positives
- **False negative** (missed door/stair/window): under-counted quantities and potentially missed egress or accessibility elements. Severity: **high** for doors and stairs.
- **False positive** (invented window/furniture): over-counted quantities and extra review time. Severity: **medium**; visible and easy for a reviewer to delete.
- For this use case false negatives are worse, so prefer higher recall (lower confidence threshold, 0.15-0.25) and keep a human reviewing every plan.
- Mitigations: human-in-the-loop review, per-class thresholds, periodic re-evaluation on new plans.

## 5. Licence and data rights
- Code: MIT (copyright Cesare Della Corte)
- Dataset: **public** images (Roboflow Universe, single source) with own annotations; redistribution allowed: **yes for the main source (MIT, keep the notice and cite it)**
- Weights: derived from Ultralytics (AGPL-3.0); distributed through the GitHub Release.
