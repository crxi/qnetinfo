import { defineConfig } from "astro/config";
import yaml from "@rollup/plugin-yaml";

// Production site lives at https://crxi.github.io/qnetinfo/
// Astro uses `site` for absolute URLs (sitemap, og:url) and `base`
// to prefix all internal asset and route URLs so the build works
// when served from the /qnetinfo subpath.
export default defineConfig({
  site: "https://crxi.github.io",
  base: "/qnetinfo",
  vite: {
    plugins: [yaml()],
  },
  build: {
    inlineStylesheets: "always",
  },
});
