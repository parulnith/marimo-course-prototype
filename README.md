# marimo course prototype

This repository contains a course prototype for the marimo team.

## View the course

Open the [live course preview](https://parulnith.github.io/marimo-course-prototype/).

The preview shows the course layout, left sidebar, lesson content, interactive components, and embedded marimo notebooks.

## Files for the marimo team

The `course/` folder contains the portable course content:

- `course/modules/` contains the MDX lessons.
- `course/assets/` contains the images, GIFs, Jupyter notebooks, and marimo notebooks used by the lessons.
- `course/components/placeholders.mdx` describes the custom MDX components that the marimo team will need to map to its website components.
- `course/README.md` contains integration notes.

## Preview files

The `preview/` folder contains the React and Vite site used for the live course preview. These files show one possible presentation of the course. The marimo team does not need to copy this folder into its website.

The `preview/public/notebooks/` folder contains exported notebook files used by the live preview. It is generated content, but it must remain in this repository for the embedded notebooks to load on the preview site.

## Run the preview locally

```bash
cd preview
npm install
npm run dev
```

Open the local address shown in the terminal.
