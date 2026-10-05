import mdx from "@mdx-js/rollup";
import react from "@vitejs/plugin-react";
import remarkFrontmatter from "remark-frontmatter";
import { defineConfig } from "vite";
import { execFileSync } from "node:child_process";
import { copyFileSync, cpSync, existsSync, mkdirSync, mkdtempSync, rmSync, statSync } from "node:fs";
import { basename, dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { tmpdir } from "node:os";

const repoRoot = fileURLToPath(new URL("../", import.meta.url));
const notebookOutputDir = join(repoRoot, "preview/public/notebooks");
const notebookSources = [
  "course/notebooks/module-1/marimo_baseline.py",
  "course/notebooks/module-1/1_2_marimo_reactive_workflow.py",
  "course/notebooks/module-2/2_2_active_environment_starter.py",
  "course/notebooks/module-2/2_2_sandboxed_environment.py",
  "course/notebooks/module-3/3_1_inspect_and_edit_data.py",
  "course/notebooks/module-3/3_2_explore_data_visually.py",
  "course/notebooks/module-3/3_3_choose_model_inputs.py",
  "course/notebooks/module-3/3_4_fit_and_compare_models.py",
  "course/notebooks/module-3/3_5_debug_errors_interactively.py",
  "course/notebooks/module-4/4_1_ai_features_demo.py",
  "course/notebooks/module-5/sentiment_classifier.py",
  "course/notebooks/module-5/sentiment_classifier_script.py",
  "course/notebooks/module-5/eval_pipeline.py",
  "course/notebooks/module-5/occupancy.py",
  "course/notebooks/module-5/occupancy_reuse.py",
].map((path) => join(repoRoot, path));

function notebookExportDir(source) {
  return basename(dirname(source)) === "module-5"
    ? join(notebookOutputDir, "module-5")
    : notebookOutputDir;
}

function exportedNotebookPath(source) {
  return join(notebookExportDir(source), `${basename(source, ".py")}.html`);
}

function exportNotebook(source, force = false) {
  const exportDir = notebookExportDir(source);
  const destination = exportedNotebookPath(source);
  const sourceDestination = join(exportDir, basename(source));
  mkdirSync(exportDir, { recursive: true });
  if (force || !existsSync(sourceDestination) || statSync(sourceDestination).mtimeMs < statSync(source).mtimeMs) {
    copyFileSync(source, sourceDestination);
  }
  if (!force && existsSync(destination) && statSync(destination).mtimeMs >= statSync(source).mtimeMs) {
    return false;
  }

  const stagingDir = mkdtempSync(join(tmpdir(), "marimo-course-export-"));
  const exportArgs = [
    "--from", "marimo==0.23.16", "marimo", "export", "html-wasm", source,
    "-o", stagingDir, "--mode", "edit", "--no-sandbox", "-f",
  ];
  if (["sentiment_classifier.py", "sentiment_classifier_script.py"].includes(basename(source))) {
    exportArgs.push("--execute");
  }
  try {
    execFileSync("uvx", exportArgs, { cwd: repoRoot, stdio: "inherit" });
    copyFileSync(join(stagingDir, "index.html"), destination);
    rmSync(join(stagingDir, "index.html"));
    // Keep sibling notebooks' public files and wheels when merging an export.
    cpSync(stagingDir, exportDir, { recursive: true });
  } finally {
    rmSync(stagingDir, { recursive: true, force: true });
  }
  if (basename(source) === "eval_pipeline.py") {
    const publicDir = join(exportDir, "public");
    mkdirSync(publicDir, { recursive: true });
    copyFileSync(
      join(dirname(source), "sentiment_classifier.py"),
      join(publicDir, "sentiment_classifier.py"),
    );
  }
  if (["occupancy.py", "occupancy_reuse.py"].includes(basename(source))) {
    const publicDir = join(exportDir, "public");
    mkdirSync(publicDir, { recursive: true });
    copyFileSync(join(dirname(source), "public/occupancy.csv"), join(publicDir, "occupancy.csv"));
    copyFileSync(join(dirname(source), "occupancy.py"), join(publicDir, "occupancy.py"));
  }
  return true;
}

function marimoNotebookSync() {
  return {
    name: "marimo-notebook-sync",
    buildStart() {
      if (process.env.GITHUB_ACTIONS) return;
      for (const source of notebookSources) exportNotebook(source);
      execFileSync("python3", [join(repoRoot, "preview/scripts/package_occupancy.py")], { cwd: repoRoot });
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
          if (basename(source).startsWith("occupancy")) {
            execFileSync("python3", [join(repoRoot, "preview/scripts/package_occupancy.py")], { cwd: repoRoot });
          }
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
