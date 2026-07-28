# Course content

This folder contains the files that the marimo team can integrate into its website.

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
    └── examples/
```

## What each folder contains

`modules/` contains the MDX lesson files.

`images/` contains the images and GIFs used in the lessons.

`notebooks/module-1/` contains the Jupyter and marimo notebook source files used to create the Module 1 examples.

`notebooks/examples/` contains optional marimo notebooks that are not used directly in the current lesson.

`components/placeholders.mdx` describes the custom MDX components used in the lessons. The marimo team can map these names to components on its website.

## Module 1 notebooks

The Module 1 notebook source files are:

- `notebooks/module-1/1_1_jupyter_baseline.ipynb`
- `notebooks/module-1/1_2_marimo_reactive_workflow.py`
- `notebooks/module-1/marimo_baseline.py`

## Run a marimo notebook

Install marimo if needed.

```bash
pip install marimo
```

Open a notebook in edit mode.

```bash
marimo edit course/notebooks/module-1/1_2_marimo_reactive_workflow.py
```

The `preview/` folder at the repository root is not part of this course package. It is only used to publish the standalone course preview.
