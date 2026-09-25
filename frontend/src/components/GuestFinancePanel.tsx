"use client";

import { useState } from "react";

import type { GuestFinanceSummary } from "@/lib/api";
import { formatCurrency, humanizeField } from "@/lib/format";

import { Icon } from "./Icon";
import { StatusBadge } from "./StatusBadge";

type GuestFinancePanelProps = {
  summary: GuestFinanceSummary;
  onConfirmEntry?: (entryId: string, reference: string) => Promise<void>;
};

export function GuestFinancePanel({ summary, onConfirmEntry }: GuestFinancePanelProps) {
  const [reference, setReference] = useState<Record<string, string>>({});
  const [busyId, setBusyId] = useState<string | null>(null);
  const [error, setError] = useState("");

  const confirm = async (entryId: string) => {
    if (!onConfirmEntry) return;
    setBusyId(entryId);
    setError("");
    try {
      await onConfirmEntry(entryId, reference[entryId] ?? "");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to confirm entry.");
    } finally {
      setBusyId(null);
    }
  };

  return (
    <section className="trip-panel">
      <div className="section-heading">
        <div>
          <h3>Finance</h3>
          <p>Agency revenue, Artist balance and refunds for this Guest.</p>
        </div>
        <div className="trip-summary">
          <strong>{formatCurrency(summary.agency_revenue_confirmed, summary.currency)}</strong>
          <small>Agency revenue confirmed</small>
        </div>
      </div>
      <div className="trip-grid">
        <div>
          <h4><Icon name="revenue" />Artist receivable</h4>
          <article><strong>Expected</strong><span>{formatCurrency(summary.artist_receivable_expected, summary.currency)}</span></article>
          <article><strong>Confirmed</strong><span>{formatCurrency(summary.artist_receivable_confirmed, summary.currency)}</span></article>
        </div>
        <div>
          <h4><Icon name="revenue" />Artist refund</h4>
          <article><strong>Due</strong><span>{formatCurrency(summary.artist_refund_due, summary.currency)}</span></article>
          <article><strong>Confirmed</strong><span>{formatCurrency(summary.artist_refund_confirmed, summary.currency)}</span></article>
        </div>
        <div>
          <h4><Icon name="revenue" />Entries</h4>
          {summary.entries.length === 0
            ? <p>No entries recorded yet.</p>
            : summary.entries.map((entry) => (
              <article key={entry.id}>
                <strong>{humanizeField(entry.entry_type.toLowerCase())}</strong>
                <span>{formatCurrency(entry.amount, entry.currency)}</span>
                <StatusBadge status={entry.status} />
                {onConfirmEntry && entry.status !== "CONFIRMED" && (
                  <div className="review-controls">
                    <input
                      aria-label={`Reference for ${humanizeField(entry.entry_type.toLowerCase())}`}
                      disabled={busyId === entry.id}
                      onChange={(event) => setReference((current) => ({ ...current, [entry.id]: event.target.value }))}
                      placeholder="Reference (optional)"
                      value={reference[entry.id] ?? ""}
                    />
                    <div>
                      <button className="approve-action" disabled={busyId === entry.id} onClick={() => confirm(entry.id)} type="button">
                        <Icon name="approved" />{busyId === entry.id ? "Confirming…" : "Confirm"}
                      </button>
                    </div>
                  </div>
                )}
              </article>
            ))}
        </div>
      </div>
      {error && <p className="form-error" role="alert">{error}</p>}
    </section>
  );
}
