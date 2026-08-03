# Course content

This folder contains the portable course files for website integration.

## Folder structure

```text
course/
├── components/
│   └── placeholders.mdx
├── images/
│   └── module-1/
├── modules/
│   ├── 01-interactive-environments.mdx
│   ├── 02-reproducibility.mdx
│   ├── 03-interactivity.mdx
│   ├── 04-ai-coding-agents.mdx
│   └── 05-reusable-systems.mdx
└── notebooks/
    ├── module-1/
    └── module-2/
```

## What each folder contains

`modules/` contains the MDX lesson files.

`images/` contains the images and GIFs used in the lessons.

`notebooks/module-1/` contains the Jupyter and marimo notebook source files used to create the Module 1 examples.

`notebooks/module-2/` contains the Jupyter and marimo notebook source files used for the environment and version control exercises.

`components/placeholders.mdx` describes the custom MDX components used in the lessons. These names can be mapped to the components provided by the website.

## Module 1 notebooks

The Module 1 notebook source files are:

- `notebooks/module-1/1_1_jupyter_baseline.ipynb`
- `notebooks/module-1/1_2_marimo_reactive_workflow.py`
- `notebooks/module-1/environment-tour.py`
- `notebooks/module-1/marimo_baseline.py`

## Module 2 notebooks

The Module 2 notebook source files are:

- `notebooks/module-2/2_1_environment_drift.ipynb`
- `notebooks/module-2/2_2_sandboxed_environment.py`
- `notebooks/module-2/2_3_jupyter_diff_demo.ipynb`
- `notebooks/module-2/2_3_marimo_diff_demo.py`

## Run a marimo notebook

Install marimo if needed.

```bash
pip install marimo
```

Open a notebook in edit mode.

```bash
marimo edit course/notebooks/module-1/1_2_marimo_reactive_workflow.py
```

Open the Module 2 environment example in an isolated sandbox.

```bash
marimo edit --sandbox course/notebooks/module-2/2_2_sandboxed_environment.py
```

The `preview/` folder at the repository root is not part of this course package. It is only used to publish the standalone course preview.
