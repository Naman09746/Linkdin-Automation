"use client";

import { useEffect, useMemo, useState } from "react";

type Stats = {
  pending: number;
  approved: number;
  posted: number;
  rejected: number;
};

type Signal = {
  title?: string;
  url?: string;
};

type Draft = {
  id: string;
  post_type?: string;
  content?: string;
  visual_url?: string | null;
  signals?: Signal | null;
  created_at?: string;
  status?: string;
};

type HistoryItem = Draft;

type TabKey = "home" | "review" | "history";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api";

const tabs: { key: TabKey; label: string }[] = [
  { key: "home", label: "Overview" },
  { key: "review", label: "Review Queue" },
  { key: "history", label: "History" },
];

const emptyStats: Stats = {
  pending: 0,
  approved: 0,
  posted: 0,
  rejected: 0,
};

export default function DashboardPage() {
  const [tab, setTab] = useState<TabKey>("home");
  const [stats, setStats] = useState<Stats>(emptyStats);
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const statsCards = useMemo(
    () => [
      { label: "Pending", value: stats.pending, tone: "accent" },
      { label: "Approved", value: stats.approved, tone: "positive" },
      { label: "Posted", value: stats.posted, tone: "neutral" },
      { label: "Rejected", value: stats.rejected, tone: "warning" },
    ],
    [stats]
  );

  useEffect(() => {
    void loadStats();
  }, []);

  useEffect(() => {
    if (tab === "review") {
      void loadDrafts();
    }

    if (tab === "history") {
      void loadHistory();
    }
  }, [tab]);

  async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options?.headers || {}),
      },
    });

    if (!response.ok) {
      throw new Error(`Request failed: ${response.status}`);
    }

    return (await response.json()) as T;
  }

  async function loadStats() {
    try {
      const data = await apiFetch<Stats>("/stats");
      setStats(data);
    } catch {
      setStats(emptyStats);
    }
  }

  async function loadDrafts() {
    setLoading(true);
    setMessage(null);
    try {
      const data = await apiFetch<Draft[]>("/drafts/pending");
      setDrafts(data);
    } catch {
      setDrafts([]);
      setMessage("Unable to load pending drafts.");
    } finally {
      setLoading(false);
    }
  }

  async function loadHistory() {
    setLoading(true);
    setMessage(null);
    try {
      const data = await apiFetch<HistoryItem[]>("/drafts/history");
      setHistory(data);
    } catch {
      setHistory([]);
      setMessage("Unable to load history.");
    } finally {
      setLoading(false);
    }
  }

  async function approveDraft(draftId: string) {
    setMessage(null);
    await apiFetch(`/drafts/${draftId}/approve`, { method: "POST" });
    await Promise.all([loadDrafts(), loadStats()]);
    setMessage("Draft approved.");
  }

  async function rejectDraft(draftId: string) {
    const reason = window.prompt("Optional rejection note:") || "";
    setMessage(null);
    await apiFetch(`/drafts/${draftId}/reject`, {
      method: "POST",
      body: JSON.stringify({ status: "rejected", rejection_reason: reason }),
    });
    await Promise.all([loadDrafts(), loadStats()]);
    setMessage("Draft rejected.");
  }

  return (
    <div className="shell">
      <div className="shell__glow" aria-hidden="true" />
      <header className="topbar motion-rise" style={{ "--delay": "80ms" } as React.CSSProperties}>
        <div>
          <p className="topbar__kicker">LinkedIn AI Agent</p>
          <h1>Draft Command Deck</h1>
          <p className="topbar__sub">Track, review, and ship content without leaving the dashboard.</p>
        </div>
        <div className="status-chip">
          <span className="status-dot" />
          <span>Pipeline active</span>
        </div>
      </header>

      <nav className="tabbar motion-rise" style={{ "--delay": "140ms" } as React.CSSProperties}>
        {tabs.map((item) => (
          <button
            key={item.key}
            type="button"
            className={`tab ${tab === item.key ? "tab--active" : ""}`}
            onClick={() => setTab(item.key)}
          >
            {item.label}
          </button>
        ))}
      </nav>

      <main className="content">
        {tab === "home" && (
          <section className="grid">
            {statsCards.map((card, index) => (
              <div
                key={card.label}
                className={`panel panel--${card.tone} motion-rise`}
                style={{ "--delay": `${180 + index * 80}ms` } as React.CSSProperties}
              >
                <p className="panel__label">{card.label}</p>
                <h2>{card.value}</h2>
                <p className="panel__foot">Live sync with Supabase</p>
              </div>
            ))}
            <div className="panel panel--wide motion-rise" style={{ "--delay": "520ms" } as React.CSSProperties}>
              <div>
                <p className="panel__label">System pulse</p>
                <h3>Next run window</h3>
                <p className="panel__body">
                  Keep your agent loop running locally while review actions stay centralized in this console.
                </p>
              </div>
              <div className="panel__meta">
                <div>
                  <p className="panel__label">API</p>
                  <p className="panel__body">{API_BASE}</p>
                </div>
                <div>
                  <p className="panel__label">Status</p>
                  <p className="panel__body">Ready for review</p>
                </div>
              </div>
            </div>
          </section>
        )}

        {tab === "review" && (
          <section className="stack">
            <div className="section-head">
              <div>
                <h2>Review queue</h2>
                <p>Approve or reject drafts the moment they land.</p>
              </div>
              <button className="ghost" onClick={loadDrafts} type="button">
                Refresh
              </button>
            </div>
            {message && <p className="notice">{message}</p>}
            {loading && <p className="notice">Loading drafts...</p>}
            {!loading && drafts.length === 0 && (
              <p className="notice">No pending drafts. Trigger a pipeline run to generate new content.</p>
            )}
            <div className="cards">
              {drafts.map((draft, index) => (
                <article
                  key={draft.id}
                  className="card motion-rise"
                  style={{ "--delay": `${160 + index * 90}ms` } as React.CSSProperties}
                >
                  <div className="card__header">
                    <div>
                      <p className="card__tag">{draft.post_type || "Draft"}</p>
                      <h3>{draft.signals?.title || "Untitled signal"}</h3>
                    </div>
                    <div className="card__actions">
                      <button className="approve" onClick={() => approveDraft(draft.id)} type="button">
                        Approve
                      </button>
                      <button className="reject" onClick={() => rejectDraft(draft.id)} type="button">
                        Reject
                      </button>
                    </div>
                  </div>

                  <div className="card__body">
                    <div className="card__content">
                      <p>{draft.content || "No draft content."}</p>
                      {draft.signals?.url && (
                        <a className="source" href={draft.signals.url} target="_blank" rel="noreferrer">
                          View source
                        </a>
                      )}
                    </div>
                    <div className="card__visual">
                      {draft.visual_url ? (
                        <img src={draft.visual_url} alt="Draft visual" />
                      ) : (
                        <div className="visual__placeholder">No visual</div>
                      )}
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </section>
        )}

        {tab === "history" && (
          <section className="stack">
            <div className="section-head">
              <div>
                <h2>Publishing history</h2>
                <p>See every approved and rejected decision.</p>
              </div>
              <button className="ghost" onClick={loadHistory} type="button">
                Refresh
              </button>
            </div>
            {message && <p className="notice">{message}</p>}
            {loading && <p className="notice">Loading history...</p>}
            {!loading && history.length === 0 && (
              <p className="notice">No history yet. Approve or reject a draft to populate this view.</p>
            )}
            {history.length > 0 && (
              <div className="table">
                <div className="table__row table__head">
                  <span>Date</span>
                  <span>Signal</span>
                  <span>Type</span>
                  <span>Status</span>
                </div>
                {history.map((item) => (
                  <div key={item.id} className="table__row">
                    <span>{item.created_at ? new Date(item.created_at).toLocaleString() : "-"}</span>
                    <span>{item.signals?.title || "Untitled"}</span>
                    <span>{item.post_type || "-"}</span>
                    <span className={`pill pill--${item.status || "pending"}`}>{item.status || "pending"}</span>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  );
}
