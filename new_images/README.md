# new_images/: plans NOT in the training or validation data

These images have no labels. Notebook 02 (cell 6) only runs the model on them to show how it generalises; they are **not** used for metrics.
Predictions: [`../results/evidence/new_predictions/`](../results/evidence/new_predictions/)

| File | Source | Licence (check on the source page) |
|---|---|---|
| `amsterdam-city-archives-IIyMRyOGyag-unsplash.jpg` | Amsterdam City Archives on Unsplash (https://unsplash.com/@amsterdamcityarchives) | Unsplash Licence |
| `amsterdam-city-archives-wD9uk9fNcQU-unsplash.jpg` | Amsterdam City Archives on Unsplash | Unsplash Licence |
| `EB1911_-_Hospital_-_Basement_Plan.png` | Wikimedia Commons, Encyclopaedia Britannica 1911 | Public domain |
| `Economy_Tailor_Shop_and_Wine_Cellar,_..._(sheet_4_of_9).tif.jpg` | Wikimedia Commons, Historic American Buildings Survey (HABS PA-4-AMB-1C) | Public domain (US government work) |
| `LWBR_RADIOACTIVE_WASTE_DISPOSAL_SYSTEM_PLOT_PLAN_-_Shippingport_...jpg` | Wikimedia Commons, Historic American Engineering Record (Shippingport Atomic Power Station) | Public domain (US government work) |

These plans are deliberately different from the training data: US and Dutch drawings, a hospital, an industrial plot plan, and very old scans. Poor results on them are expected (see `docs/error_analysis.md`).
