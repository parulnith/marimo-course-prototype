# The Modern AI and ML Development Stack, Powered by marimo

This folder contains portable course content. It is not the marimo website.

The files in `modules/` are meant to be copied into the marimo Learn repository. They use standard Markdown and MDX where possible. The custom components in Module 1 are placeholders. The marimo Learn team must map them to the components already used by the site.

The notebook paths in the MDX are relative paths. The team may need to replace them with hosted URLs or repository paths during integration.

Before final integration, the marimo team should provide its required frontmatter fields and exact MDX component names.

## Package contents

```text
course/
├── README.md
├── assets/module-1/
├── components/placeholders.mdx
├── modules/
│   ├── 01-interactive-environments.mdx
│   ├── 02-reproducibility.mdx
│   ├── 03-interactivity.mdx
│   ├── 04-ai-coding-agents.mdx
│   └── 05-reusable-systems.mdx
└── notebooks/module-1/
    ├── reactive-workflow.py
    └── environment-tour.py
```

The `assets/module-1/` folder is reserved for images and other files that Module 1 may need later.

## Run the notebooks

Install marimo if needed:

```bash
pip install marimo
```

Open the reactive workflow:

```bash
marimo edit course/notebooks/module-1/reactive-workflow.py
```

Open the guided environment tour:

```bash
marimo edit course/notebooks/module-1/environment-tour.py
```

Use `marimo run` instead of `marimo edit` when you want to use a notebook without changing it.

Each notebook includes inline dependency metadata. A tool such as `uv` can create a temporary environment from that metadata:

```bash
uv run course/notebooks/module-1/reactive-workflow.py
uv run course/notebooks/module-1/environment-tour.py
```

## Integration notes

The file `components/placeholders.mdx` documents the placeholder component contract. Module 1 also has an HTML comment above each placeholder use. These comments state what the marimo Learn team must map.

No site framework, layout, navigation, fonts, or design tokens are included. The existing marimo Learn codebase should provide all final layout and styling.

## Local visual preview

The separate `preview/` folder shows one possible course presentation on marimo.io. It is for review only. It does not define how the marimo team must integrate or style the course.

Install the preview dependencies once:

```bash
cd preview
npm install
npm run dev
```

Then open the URL shown in the terminal. The preview imports Module 1 directly from `course/modules/01-interactive-environments.mdx`. Changes appear as soon as you save the MDX file.

The lesson uses `MarimoEmbed` placeholders for interactive notebooks. The marimo Learn team must map this component to its existing notebook embed and replace the local notebook paths with hosted URLs if required.

The hidden-state example uses a GIF placeholder for maximum portability. Keep `course/assets/module-1/jupyter_hidden_state.ipynb` as the source used to record the final animation. When the GIF is ready, place it at `course/assets/module-1/jupyter-hidden-state.gif` and replace the placeholder text in Module 1 with standard Markdown image syntax.
