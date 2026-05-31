const sampleCitations = [
  "BNSS Section 35",
  "Constitution of India Article 22",
  "Supreme Court arrest safeguards",
];

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <section className="mx-auto flex max-w-7xl gap-6 px-6 py-8">
        <aside className="hidden w-72 rounded-2xl border border-slate-800 bg-slate-900/70 p-4 lg:block">
          <h2 className="text-lg font-semibold">NyayaGPT</h2>
          <p className="mt-1 text-sm text-slate-400">Indian legal research workspace</p>
          <nav className="mt-6 space-y-2 text-sm">
            {['Legal Research', 'Case Comparison', 'Statute Explorer', 'Timeline Builder', 'Document Summarizer'].map((item) => (
              <div key={item} className="rounded-xl px-3 py-2 hover:bg-slate-800">{item}</div>
            ))}
          </nav>
        </aside>
        <div className="flex-1 rounded-2xl border border-slate-800 bg-slate-900/60">
          <header className="border-b border-slate-800 p-6">
            <p className="text-sm uppercase tracking-[0.35em] text-cyan-300">AI-Powered Indian Legal Research and Assistance Platform</p>
            <h1 className="mt-3 text-4xl font-bold">Ask Indian law questions with traceable evidence.</h1>
          </header>
          <section className="space-y-4 p-6">
            <div className="rounded-2xl bg-slate-800 p-4">
              <p className="font-medium">Can police arrest without warrant?</p>
            </div>
            <article className="rounded-2xl border border-cyan-900/60 bg-cyan-950/20 p-5">
              <div className="mb-3 flex items-center justify-between">
                <h2 className="font-semibold text-cyan-200">Grounded answer</h2>
                <span className="rounded-full bg-emerald-500/15 px-3 py-1 text-sm text-emerald-300">Confidence 0.88</span>
              </div>
              <p className="leading-7 text-slate-200">
                Arrest without warrant depends on statutory grounds under criminal procedure and must comply with constitutional safeguards. NyayaGPT will refuse to answer if retrieved evidence or citation validation fails.
              </p>
              <div className="mt-5 grid gap-3 md:grid-cols-3">
                {sampleCitations.map((citation) => (
                  <div key={citation} className="rounded-xl border border-slate-700 bg-slate-950/70 p-3 text-sm">
                    <p className="font-medium text-cyan-200">{citation}</p>
                    <p className="mt-1 text-slate-400">Open source card and document viewer</p>
                  </div>
                ))}
              </div>
            </article>
            <div className="rounded-2xl border border-slate-800 bg-slate-950 p-4">
              <input className="w-full bg-transparent outline-none" placeholder="Ask a legal question; every answer requires evidence..." />
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}
