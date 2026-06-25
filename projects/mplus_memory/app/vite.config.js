import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import tailwindcss from "@tailwindcss/vite";

// GitHub Pages serves from /<repo>/; this project lives in the `wow` repo.
// Override with VITE_BASE if the publish path differs.
export default defineConfig({
  base: process.env.VITE_BASE ?? "/wow/",
  plugins: [svelte(), tailwindcss()],
});
