// Minimal Bun static server for the CDM design prototypes.
//   bun serve.mjs   →   http://localhost:8791  (root serves cdm-designs.html)
const dir = import.meta.dir;
const PORT = 8791;

Bun.serve({
  port: PORT,
  async fetch(req) {
    let path = decodeURIComponent(new URL(req.url).pathname);
    if (path === "/" || path === "") path = "/cdm-designs.html";
    // keep it inside this folder
    if (path.includes("..")) return new Response("nope", { status: 400 });
    const f = Bun.file(dir + path);
    if (await f.exists()) return new Response(f);
    return new Response("not found", { status: 404 });
  },
});

console.log(`CDM prototypes → http://localhost:${PORT}`);
