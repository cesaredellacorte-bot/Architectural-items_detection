# Governance checklist

Project: floor-plan element detector (YOLOv8n, 6 classes) · Owner: Cesare Della Corte · Reviewed: 2026-10-18
Status legend: [x] done / checked · [ ] open (with the action and owner)

## 1. Personal data (PII) and privacy
- [x] **PII inventory done.** Floor plans are not personal data by themselves. They *can* become personal data under GDPR Art. 4(1) when they can be linked to an identifiable person: owner or architect names, signatures, street addresses, property / plot numbers, building-permit stamps.
- [x] **Dataset checked (124 images, v2).** No faces and no e-mail or phone numbers were found. Some plans carry **title-block text and stamps** that could link a plan to a property. Example: a Finnish building-permit stamp ("Rakennuslupa N:o ... 26.2.62") at the bottom of valid image `4831_png_jpg...`. Other plans show architect lettering, and one image has a `CUBICASA` watermark.
- [x] **Risk judged low.** The images were already published as a public dataset (Roboflow Universe *cad-drawings*, MIT). Room labels are generic (MH, OH, K, KT). No street address or owner name could be read at 640 px.
- [ ] **Action before any real-world use:** blur or crop title blocks and stamps in all images (data improvement 1 in the error analysis). Owner: author · when: dataset v3.
- [x] **No secrets in the repo.** No Roboflow or Google API key is committed. The notebook needs no key, because the dataset is downloaded from a public GitHub Release.
- [x] **Source of every image recorded:** one source, Roboflow Universe `train-yu3wc/cad-drawings` (MIT, checked 2026-10-16). All annotations are the author's own (README section 3).

## 2. Data minimisation and retention
- [x] Only task-relevant data: 124 floor-plan images resized to 640x640, plus box labels for 6 classes. No metadata kept: Roboflow stripped EXIF on export.
- [x] The dataset is frozen and versioned (Release `dataset-v2` + SHA256), so it is clear exactly which data the model saw.
- [x] **Retention:** the frozen zip and the weights stay public for as long as the course repository exists, and are reviewed at project end (course close). If the source dataset is withdrawn or a rights holder objects, the release asset is deleted and the model retrained without those images.
- [ ] New plans uploaded by users for inference are **not** stored or used for training without consent (not applicable now; there is no deployed service).

## 3. Risk: false negatives vs false positives
| Error | Example | Consequence | Severity |
|---|---|---|---|
| **False negative** (missed object) | missed door / stair / window | under-counted quantities; a missed **egress door or stair** in an accessibility or fire review | **High** for Door and Stairs |
| **False positive** (invented object) | furniture symbol where nothing is labelled; a "Room" on dimension lines | over-counted quantities, extra review time | **Medium**: visible and quick for a reviewer to delete |

- [x] For this use case, false negatives cost more than false positives. Operate at a **lower confidence threshold (0.15-0.25)** to favour recall, and let a human remove false positives.
- [x] Known weak spots are documented: Stairs recall 0.25, Furniture precision 0.34, Walls not usable (see `error_analysis.md`).
- [x] **Not intended for:** building-permit, fire-safety, structural or legal compliance decisions; cost quotations without review; plans from other countries or drawing standards that were not validated.

## 4. Human in the loop (HITL)
- [x] **The model only suggests.** Every detection is a proposal that a qualified person (architect, technician) accepts, corrects or deletes. Nothing is counted or exported automatically.
- [x] **Review workflow:** (1) the model pre-labels the plan; (2) the reviewer checks every Door, Stairs and Window, and scans for missed ones (FN is the high-risk error); (3) corrections are saved as new labels; (4) corrected plans go into the next dataset version.
- [x] **Accountability:** the person who signs the drawing or quantity take-off stays responsible for it. The tool's output is never the record of truth.
- [x] **Stop rule:** if a reviewer corrects more than about 30% of detections on a plan type, do not use the model on that plan type until it has been retrained.
- [x] **Monitoring:** re-evaluate the per-class P / R on a fresh validation set at every dataset version, and record the numbers in `results/metrics.md`.

## 5. GDPR
- [x] **Lawful basis (Art. 6):** educational, non-commercial project using images already made public under an open licence (legitimate interest, Art. 6(1)(f)). No special-category data (Art. 9).
- [x] **Data minimisation and purpose limitation (Art. 5(1)(b, c)):** images are used only to train and evaluate an element detector; title-block blurring is planned (section 1).
- [x] **Data-subject rights:** if a person shows that a plan identifies them, the image is removed from the next release and the model is retrained (contact: repository owner via GitHub issues).
- [x] **No profiling and no automated decision about people (Art. 22):** the model detects drawing symbols, not people.
- [ ] **For a real deployment with client plans:** sign a data-processing agreement with the client, keep EU hosting or apply safeguards for transfers, and run a short DPIA if plans of private homes are processed at scale.

## 6. EU AI Act (Regulation (EU) 2024/1689)
- [x] **Risk class: minimal / limited risk.** A drafting aid that detects symbols on drawings is not a prohibited practice (Art. 5). It is not listed in Annex III (high-risk areas), and it is not a safety component of a product covered by Annex I.
- [x] **Watch-out:** if the tool were used as a **safety component** (for example automatic fire-egress or accessibility compliance checks that replace human review), it would need a fresh high-risk assessment. That is why HITL (section 4) is mandatory.
- [x] **Transparency:** README section 5 and this file state what the model can and cannot do. Outputs are labelled as machine-generated suggestions.
- [x] **Technical documentation kept, as good practice:** frozen data + SHA256, parameters and versions (`results/params.yaml`, `results/run_info.md`), metrics, error analysis.
- [x] **AI literacy (Art. 4):** reviewers are told the known failure modes before they use the tool (error analysis).

## 7. Licences
- [x] Code and annotations: MIT, © Cesare Della Corte.
- [x] Images: Roboflow Universe *cad-drawings* (MIT). The copyright notice is kept and the source is cited in the README.
- [x] Weights: trained with Ultralytics YOLOv8 (**AGPL-3.0**). Weights distributed through the GitHub Release; commercial use needs AGPL compliance or an Ultralytics licence.
