import { serve } from "./server.mjs";
if (!process.argv[2])
  throw new Error("Usage: node scripts/serve.mjs PROJECT_DIRECTORY");
const server = await serve(process.argv[2], Number(process.argv[3] || 0));
console.log(server.url);
for (const signal of ["SIGINT", "SIGTERM"])
  process.on(signal, async () => {
    await server.close();
    process.exit(0);
  });
