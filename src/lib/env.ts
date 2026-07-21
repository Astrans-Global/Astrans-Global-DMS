export function getSupabasePublicConfig() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? "";
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? "";
  return {
    url,
    anonKey,
    isConfigured: Boolean(url && anonKey),
  };
}

export function getRuntimeHints() {
  return {
    nodeEnv: process.env.NODE_ENV ?? "development",
    isVercel: process.env.VERCEL === "1",
    vercelEnv: process.env.VERCEL_ENV ?? null,
    hasServiceRole: Boolean(process.env.SUPABASE_SERVICE_ROLE_KEY),
  };
}
