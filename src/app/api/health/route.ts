import { NextResponse } from "next/server";
import { getRuntimeHints, getSupabasePublicConfig } from "@/lib/env";

export const dynamic = "force-dynamic";

export async function GET() {
  const supabase = getSupabasePublicConfig();
  const runtime = getRuntimeHints();

  return NextResponse.json({
    ok: true,
    app: "astrans-global-dms",
    supabaseConfigured: supabase.isConfigured,
    serviceRoleConfigured: runtime.hasServiceRole,
    runtime,
    nextSteps: supabase.isConfigured
      ? ["Open / — skeleton is ready for feature work."]
      : [
          "Create a free Supabase project",
          "Copy keys into .env.local (see .env.example)",
          "Add the same keys in Vercel Project Settings → Environment Variables",
          "See docs/SETUP.md",
        ],
  });
}
