"use client";

import { useState } from "react";

import type { ArtistAvailability, ArtistAvailabilityInput } from "@/lib/api";

import { EmptyState } from "./EmptyState";
import { Icon } from "./Icon";

type ArtistAvailabilityOverridePanelProps = {
  items: ArtistAvailability[];
  onOverride: (input: ArtistAvailabilityInput & { reason: string }) => Promise<void>;
};

export function ArtistAvailabilityOverridePanel({ items, onOverride }: ArtistAvailabilityOverridePanelProps) {
  const [startsAt, setStartsAt] = useState("");
  const [endsAt, setEndsAt] = useState("");
  const [reason, setReason] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (new Date(endsAt) <= new Date(startsAt)) {
      setError("End time must be after start time.");
      return;
    }
    if (!reason.trim()) {
      setError("Add a reason for this intervention.");
      return;
    }
    if (!window.confirm("Override this Artist's availability? This window cannot be edited by the Artist afterwards.")) return;
    setBusy(true);
    setError("");
    try {
      await onOverride({
        starts_at: new Date(startsAt).toISOString(),
        ends_at: new Date(endsAt).toISOString(),
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC",
        reason: reason.trim(),
      });
      setStartsAt("");
      setEndsAt("");
      setReason("");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to override availability.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="split-panel">
      <form className="data-form compact-form" onSubmit={submit}>
        <label>Available from<input required type="datetime-local" value={startsAt} onChange={(event) => setStartsAt(event.target.value)} /></label>
        <label>Available until<input required type="datetime-local" value={endsAt} onChange={(event) => setEndsAt(event.target.value)} /></label>
        <label>Reason<textarea required value={reason} onChange={(event) => setReason(event.target.value)} /></label>
        <button disabled={busy} type="submit"><Icon name="alert" />{busy ? "Overriding…" : "Override availability"}</button>
        {error && <p className="form-error" role="alert">{error}</p>}
      </form>
      <div className="record-list">
        {items.length === 0 ? (
          <EmptyState
            hint="This Artist has not registered any availability yet."
            icon="schedule"
            title="No availability registered"
          />
        ) : items.map((item) => (
          <article key={item.id}>
            <strong>{new Date(item.starts_at).toLocaleString("en-US")}</strong>
            <span>to {new Date(item.ends_at).toLocaleString("en-US")}</span>
            <small>{item.timezone}{item.changed_by_advisory ? " · Managed by Advisory" : ""}</small>
          </article>
        ))}
      </div>
    </div>
  );
}
