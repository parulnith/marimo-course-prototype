import mdx from "@mdx-js/rollup";
import react from "@vitejs/plugin-react";
import remarkFrontmatter from "remark-frontmatter";
import { defineConfig } from "vite";
import { execFileSync } from "node:child_process";
import { copyFileSync, existsSync, mkdirSync, rmSync, statSync } from "node:fs";
import { basename, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = fileURLToPath(new URL("../", import.meta.url));
const notebookOutputDir = join(repoRoot, "preview/public/notebooks");
const notebookSources = [
  "course/notebooks/module-1/marimo_baseline.py",
  "course/notebooks/module-1/1_2_marimo_reactive_workflow.py",
  "course/notebooks/module-2/2_2_active_environment_starter.py",
  "course/notebooks/module-2/2_2_sandboxed_environment.py",
  "course/notebooks/module-3/3_1_interactive_ml_workflow_starter.py",
].map((path) => join(repoRoot, path));

function exportedNotebookPath(source) {
  return join(notebookOutputDir, `${basename(source, ".py")}.html`);
}

function exportNotebook(source, force = false) {
  const destination = exportedNotebookPath(source);
  if (!force && existsSync(destination) && statSync(destination).mtimeMs >= statSync(source).mtimeMs) {
    return false;
  }

  mkdirSync(notebookOutputDir, { recursive: true });
  execFileSync(
    "uvx",
    ["--from", "marimo==0.23.16", "marimo", "export", "html-wasm", source, "-o", notebookOutputDir, "--mode", "edit", "--no-sandbox", "-f"],
    { cwd: repoRoot, stdio: "inherit" },
  );
  const generated = join(notebookOutputDir, "index.html");
  copyFileSync(generated, destination);
  rmSync(generated);
  return true;
}

function marimoNotebookSync() {
  return {
    name: "marimo-notebook-sync",
    buildStart() {
      if (process.env.GITHUB_ACTIONS) return;
      for (const source of notebookSources) exportNotebook(source);
    },
    configureServer(server) {
      server.watcher.add(notebookSources);
      server.middlewares.use((request, response, next) => {
        if (request.url?.startsWith("/notebooks/")) {
          response.setHeader("Cache-Control", "no-store");
        }
        next();
      });
      server.watcher.on("all", (event, changedPath) => {
        if (event !== "change" && event !== "add") return;
        const source = notebookSources.find((path) => path === changedPath);
        if (!source) return;
        try {
          exportNotebook(source, true);
          server.ws.send({ type: "full-reload" });
        } catch (error) {
          server.config.logger.error(`Could not export ${basename(source)}: ${error.message}`);
        }
      });
    },
  };
}

export default defineConfig({
  base: process.env.GITHUB_ACTIONS ? "/marimo-course-prototype/" : "/",
  plugins: [
    marimoNotebookSync(),
    {
      enforce: "pre",
      ...mdx({
        jsxImportSource: "react",
        providerImportSource: "@mdx-js/react",
        remarkPlugins: [remarkFrontmatter],
      }),
    },
    react(),
  ],
  resolve: {
    alias: {
      "@mdx-js/react": fileURLToPath(new URL("./node_modules/@mdx-js/react/index.js", import.meta.url)),
    },
  },
  server: {
    fs: { allow: [".."] },
  },
});
