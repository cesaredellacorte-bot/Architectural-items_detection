# Author workflow (delete this file before submitting)

Order matters: each step produces what the next one needs. Rubric weights in brackets.

## 0. Decide (15 min)
- [ ] Use the **Roboflow 80/20 split** and **YOLOv8n/s** exactly as the brief says (do not re-split or switch model family, or the README will contradict the assignment).
- [ ] One person owns the repo; everyone else is added as collaborator. Pick licence (MIT or "Internal/Private Use Only") and confirm dataset rights.

## 1. Repo skeleton (Step A) [Repo 2 pts]
1. GitHub -> New repository -> Add file -> Upload files: drag in this whole folder.
2. Search-and-replace the `<placeholders>` in README.md and docs/*.md (GitHub web editor is enough).
3. Make sure no API key is committed. Check every link opens (README -> docs, notebooks, release).

## 2. Reproducibility proof (Step B) [Reproducibility 3 pts]
1. Colab secret `ROBOFLOW_API_KEY`; edit the parameters cell of `notebooks/02_train_eval.ipynb` (repo name, Roboflow names, version, model, epochs >= 30).
2. Open it **from GitHub** in Colab -> T4 GPU -> Restart runtime -> Run all.
3. Cell 9 downloads `results_to_commit.zip`: unzip and upload `results/` into the repo (metrics.md, curves/, evidence/, run_info.md).
4. Create a GitHub Release `v1.0`, attach `best.pt` (copy from `/content/runs/train/weights/`), paste the URL in README and in `WEIGHTS_URL`.
5. Fill README "Reproducibility checklist" and "Reproducibility proof" from `results/run_info.md`.
6. No GPU/time: set `FAST_VERIFY = True`, run, and say so explicitly in the proof note.
7. Re-run once from a **fresh** Colab session to be sure it works for a third party.

## 3. Evidence pack + error analysis (Step C) [Evidence 2 pts + Error analysis 1.5 pts]
1. Evidence images are already generated in `results/evidence/` (5 annotations, 10 validation, 5 new).
2. Put 5+ new images in `/new_images/` before running (images the model never saw).
3. Open `results/evidence/errors/`: pick 3 FP (red) and 3 FN (blue); write hypotheses in `docs/error_analysis.md`.
   Test each hypothesis quickly: FP on something unlabelled? -> missing label. Rare class? -> count instances in `labels.jpg`. Tiny object? -> compare box size with the class average.
4. Write 3 improvements that are concrete (what, how many, from where) and tied to a failure above, with a measurable target.
5. Interpret the metrics in 2-3 sentences in README (which class is weak, precision vs recall gap, curve behaviour: still improving? overfitting?).

## 4. Governance + licence (Step D) [Governance 1.5 pts]
- [ ] Complete every checkbox in `docs/governance_checklist.md` with real answers (not "N/A").
- [ ] Licence line + dataset rights line in README match the checklist.

## 5. PDF pack
- [ ] `pdf_pack/slides.pdf` (6-8 slides) and `pdf_pack/mini_report.pdf` (2 pages) following `pdf_pack/OUTLINE.md`; link both from README.

## 6. Final QA (10 min)
- [ ] Open the repo in a private browser window: all links work, images render.
- [ ] Rubric pass: how-to steps copy/paste-able - versions/params documented - metrics + interpretation - 10+5+3-5 evidence images - 3 FP + 3 FN + 3 improvements - governance + licence.
- [ ] Submit the single GitHub link on Canvas.

## Status of this package (what is already filled in vs what only you can fill)
Already filled from your run: metrics table, curves, prediction grid, class counts, error-analysis patterns, governance risk note, reproduction steps.
Search the repo for `TODO(you)` - every remaining item needs information only you have.
