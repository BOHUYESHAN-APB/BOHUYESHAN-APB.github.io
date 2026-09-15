import type { APIRoute } from "astro";

// Dynamic OG generation is disabled for this site: post titles are Chinese and
// satori has no CJK font bundled, so generated cards would be broken. Pages fall
// back to public/default-og.jpg; this endpoint 404s so stale refs fail cleanly.
export const GET: APIRoute = () => new Response(null, { status: 404 });
