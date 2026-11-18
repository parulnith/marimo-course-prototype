# Occupancy course example

The course notebook `occupancy.py` is a shortened adaptation of [marimo-studio's occupancy example](https://github.com/marimo-team/marimo-studio/blob/72376de50eb89fe8372ad55f3b341cfb439be154/examples/occupancy.py), copyright 2026 Marimo, under Apache 2.0. The license is included in `LICENSE.txt`.

The adaptation retains the 70% light and 30% CO₂ scoring rule and threshold evaluation. It uses pandas, bundles the input data, and adds reusable functions, command-line arguments, and CSV output to `occupancy.py`. It omits the monitoring and observation-scope features. It does not include the official Studio views; learners build a new view from this notebook.

`occupancy.csv` is the 8,143-row training split of Luis Candanedo's [UCI Occupancy Detection dataset](https://doi.org/10.24432/C5X01N), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This file is copied without changes from the [pinned Panel mirror](https://raw.githubusercontent.com/holoviz/panel/62dda3f986251295ab4892a45e02c7f1533cf4c0/examples/assets/occupancy.csv) used by the official example.

These are in-sample metrics from a simple scoring rule, not held-out estimates from a fitted model. Normalization is recalculated for the input file. Evaluating on new data with fixed training normalization would require a separate training and evaluation workflow.

## Run locally

In the browser and notebook editor, `occupancy.py` reads the CSV from the pinned Panel URL above, so no separate data download is needed. Script mode still uses the bundled `occupancy.csv` by default and accepts a custom file with `--input`.

Keep the files and `public` folder together. From this folder:

```bash
uvx marimo edit --sandbox occupancy.py
uv run occupancy.py --threshold 0.5 --output occupancy_predictions.csv
```

For Studio, run `uvx --with marimo-studio marimo edit occupancy.py --sandbox --watch`, then follow the guided exercise in Module 5. It adds views to this same notebook. The official model review is a reference, not the output of these course files.

The notebook pins `marimo-studio[lens]==0.2.3` and `marimo-lens==0.2.3` for the Lens feedback exercise. Studio 0.2.3 requires marimo 0.25.0; Lens 0.2.3 supports that version. Keep these versions together rather than applying requirements from the latest hosted Lens documentation. The learner download includes these dependencies and installs them through `--sandbox`.
