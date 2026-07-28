# marimo course prototype

This repository contains course content and a standalone course preview.

## View the course

Open the [live course preview](https://parulnith.github.io/marimo-course-prototype/).

## Course files

The files for website integration are in `course/`.

- `course/modules/` contains the MDX lessons.
- `course/images/` contains the images and GIFs used by the lessons.
- `course/notebooks/` contains the Jupyter and marimo notebook source files.
- `course/components/` describes the custom MDX components.

See [`course/README.md`](course/README.md) for the full folder structure and integration notes.

## Preview files

The `preview/` folder contains the React and Vite site used for the live course preview. It is separate from the portable course content.

`preview/public/notebooks/` contains generated web files for the notebook embeds in the live preview. These files are required by the preview. The notebook source files are stored separately in `course/notebooks/`.

## Run the preview locally

```bash
cd preview
npm install
npm run dev
```

Open the local address shown in the terminal.
