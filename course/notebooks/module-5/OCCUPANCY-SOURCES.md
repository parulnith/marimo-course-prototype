# Occupancy course example

The course notebook `occupancy.py` is a shortened adaptation of [marimo-studio's occupancy example](https://github.com/marimo-team/marimo-studio/blob/72376de50eb89fe8372ad55f3b341cfb439be154/examples/occupancy.py), copyright 2026 Marimo, under Apache 2.0. The license is included in `licenses/marimo-studio-LICENSE.txt`.

The adaptation retains the 70% light and 30% CO₂ scoring rule and threshold evaluation. It uses pandas, bundles the input data, and adds reusable functions, command-line arguments, and CSV output to `occupancy.py`. It omits the monitoring and observation-scope features. It does not include the official Studio views; learners build a new view from this notebook.

`public/occupancy.csv` is the 8,143-row training split of Luis Candanedo's [UCI Occupancy Detection dataset](https://doi.org/10.24432/C5X01N), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This file is copied without changes from the [pinned Panel mirror](https://raw.githubusercontent.com/holoviz/panel/62dda3f986251295ab4892a45e02c7f1533cf4c0/examples/assets/occupancy.csv) used by the official example.

These are in-sample metrics from a simple scoring rule, not held-out estimates from a fitted model. Normalization is recalculated for the input file. Evaluating on new data with fixed training normalization would require a separate training and evaluation workflow.

## Run locally

Keep the files and `public` folder together. From this folder:

```bash
uvx marimo edit --sandbox occupancy.py
uv run occupancy.py --threshold 0.5 --output occupancy_predictions.csv
uvx marimo edit --sandbox occupancy_reuse.py
```

For Studio, follow the guided exercise in the Module 5 draft. It adds a view to this same notebook. The official model review is a reference, not the output of these course files.
