import { NextResponse } from "next/server";

/**
 * Placeholder cron-style endpoint.
 * v1 jobs must stay short (Vercel Hobby timeouts). No Redis / long workers.
 */
export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  const authHeader = request.headers.get("authorization");
  const cronSecret = process.env.CRON_SECRET;

  if (cronSecret && authHeader !== `Bearer ${cronSecret}`) {
    return NextResponse.json({ ok: false, error: "Unauthorized" }, { status: 401 });
  }

  return NextResponse.json({
    ok: true,
    job: "health",
    note: "Cron-friendly stub only. Real DMS jobs will be batched and short-lived.",
    at: new Date().toISOString(),
  });
}
