import { getRuntimeHints, getSupabasePublicConfig } from "@/lib/env";

export const dynamic = "force-dynamic";

export default function HomePage() {
  const supabase = getSupabasePublicConfig();
  const runtime = getRuntimeHints();

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-3xl flex-col justify-center gap-8 px-6 py-16">
      <header className="space-y-3">
        <p className="text-sm font-medium tracking-[0.18em] text-accent uppercase">
          Astrans
        </p>
        <h1 className="font-serif text-4xl leading-tight text-foreground sm:text-5xl">
          Global DMS
        </h1>
        <p className="max-w-xl text-base text-muted">
          Skeleton is live on the Vercel + Supabase path (same hosting model as
          Astrans Tasks). Feature modules come next; host decision stays open
          until after v1 usage numbers.
        </p>
      </header>

      <section className="rounded-2xl border border-line bg-panel p-6 shadow-sm">
        <h2 className="mb-4 text-lg font-semibold">Setup status</h2>
        <ul className="space-y-2 text-sm text-muted">
          <li>
            Supabase public keys:{" "}
            <strong className="text-foreground">
              {supabase.isConfigured ? "configured" : "missing"}
            </strong>
          </li>
          <li>
            Service role key:{" "}
            <strong className="text-foreground">
              {runtime.hasServiceRole ? "configured" : "optional for now"}
            </strong>
          </li>
          <li>
            Runtime:{" "}
            <strong className="text-foreground">
              {runtime.isVercel
                ? `Vercel (${runtime.vercelEnv ?? "unknown"})`
                : "local"}
            </strong>
          </li>
        </ul>

        {!supabase.isConfigured && (
          <p className="mt-4 rounded-xl bg-background px-4 py-3 text-sm text-muted">
            Copy <code className="text-foreground">.env.example</code> to{" "}
            <code className="text-foreground">.env.local</code>, add your
            Supabase keys, then restart{" "}
            <code className="text-foreground">npm run dev</code>. Full steps:{" "}
            <code className="text-foreground">docs/SETUP.md</code>.
          </p>
        )}
      </section>

      <section className="grid gap-3 sm:grid-cols-2">
        <a
          className="rounded-xl border border-line bg-panel px-4 py-3 text-sm font-medium text-foreground transition hover:border-accent"
          href="/api/health"
        >
          Open /api/health
        </a>
        <a
          className="rounded-xl border border-line bg-panel px-4 py-3 text-sm font-medium text-foreground transition hover:border-accent"
          href="/api/cron/health"
        >
          Open cron health stub
        </a>
      </section>
    </main>
  );
}
