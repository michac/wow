import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

// Static SPA: `vite build` emits a self-contained dist/ to host anywhere.
// `base: "./"` makes asset + data paths relative so it works under a subpath
// (e.g. GitHub Pages project sites).
export default defineConfig({
  base: "./",
  // Stage B writes the runtime JSON here; Vite serves it at / in dev and
  // copies it into dist/ on build.
  publicDir: "static",
  plugins: [svelte()],
});
