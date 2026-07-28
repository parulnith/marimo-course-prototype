import mdx from "@mdx-js/rollup";
import react from "@vitejs/plugin-react";
import remarkFrontmatter from "remark-frontmatter";
import { defineConfig } from "vite";
import { fileURLToPath } from "node:url";

export default defineConfig({
  plugins: [
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
