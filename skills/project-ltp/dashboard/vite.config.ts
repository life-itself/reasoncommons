import { defineConfig } from "vite";
import type { OutputAsset, OutputChunk } from "rollup";
import type { Plugin } from "vite";
import react from "@vitejs/plugin-react";
import { readdirSync, readFileSync } from "node:fs";
import { relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const dashboardRoot = fileURLToPath(new URL(".", import.meta.url));
const projectsRoot = resolve(dashboardRoot, "public/projects");
const embeddedProjectsModule = "virtual:embedded-project-files";
const resolvedEmbeddedProjectsModule = `\0${embeddedProjectsModule}`;

function projectFiles(directory: string): Record<string, string> {
  const files: Record<string, string> = {};
  for (const entry of readdirSync(directory, { withFileTypes: true })) {
    const path = resolve(directory, entry.name);
    if (entry.isDirectory()) {
      Object.assign(files, projectFiles(path));
    } else if (entry.isFile()) {
      const key = `projects/${relative(projectsRoot, path).replaceAll("\\", "/")}`;
      files[key] = readFileSync(path, "utf8");
    }
  }
  return files;
}

/**
 * Put the static project catalog in the JavaScript bundle. FlowerShow serves
 * HTML itself but redirects other repository files to a cross-origin R2
 * bucket, so runtime fetches for YAML/JSON are blocked by browser CORS.
 */
function embedProjectFiles(): Plugin {
  return {
    name: "embed-project-files",
    resolveId(id) {
      return id === embeddedProjectsModule ? resolvedEmbeddedProjectsModule : null;
    },
    load(id) {
      if (id !== resolvedEmbeddedProjectsModule) return null;
      return `export default ${JSON.stringify(projectFiles(projectsRoot))};`;
    },
  };
}

function assetText(asset: OutputAsset): string {
  return typeof asset.source === "string"
    ? asset.source
    : new TextDecoder().decode(asset.source);
}

function escapeForInlineScript(code: string): string {
  // An HTML parser closes a script element even when </script occurs inside a
  // JavaScript string. Escaping the slash keeps the runtime string identical.
  return code.replaceAll(/<\/script/gi, "<\\/script");
}

/**
 * Collapse the production build into index.html. The host can then serve the
 * whole dashboard without cross-origin redirects for Vite's JS/CSS assets.
 */
function inlineBuildAssets(): Plugin {
  return {
    name: "inline-build-assets",
    enforce: "post",
    generateBundle(_options, bundle) {
      const htmlAsset = bundle["index.html"];
      if (!htmlAsset || htmlAsset.type !== "asset") {
        throw new Error("Vite did not emit index.html");
      }

      let html = assetText(htmlAsset);
      for (const [fileName, output] of Object.entries(bundle)) {
        if (output.type === "chunk" && output.isEntry) {
          const chunk = output as OutputChunk;
          const tags = [
            `<script type="module" crossorigin src="./${fileName}"></script>`,
            `<script type="module" src="./${fileName}"></script>`,
          ];
          const tag = tags.find((candidate) => html.includes(candidate));
          if (!tag) throw new Error(`Could not find the entry script tag for ${fileName}`);
          html = html.replace(
            tag,
            () => `<script type="module">${escapeForInlineScript(chunk.code)}</script>`,
          );
          delete bundle[fileName];
        } else if (output.type === "asset" && fileName.endsWith(".css")) {
          const tags = [
            `<link rel="stylesheet" crossorigin href="./${fileName}">`,
            `<link rel="stylesheet" href="./${fileName}">`,
          ];
          const tag = tags.find((candidate) => html.includes(candidate));
          if (!tag) throw new Error(`Could not find the stylesheet tag for ${fileName}`);
          html = html.replace(tag, () => `<style>${assetText(output)}</style>`);
          delete bundle[fileName];
        }
      }
      htmlAsset.source = html;
    },
  };
}

export default defineConfig({
  plugins: [react(), embedProjectFiles(), inlineBuildAssets()],
  // Relative base so the build can be hosted under any path (e.g. /dashboard/
  // on the published site) as well as at the root via serve_dashboard.py.
  base: "./",
  build: {
    outDir: "dist",
    emptyOutDir: true,
    sourcemap: false,
    // Emit one JS chunk so inlineBuildAssets can make index.html self-contained.
    rollupOptions: {
      output: { inlineDynamicImports: true },
    },
  },
});
