"use client";

import { useState } from "react";

import type { ArtistAvailability } from "@/lib/api";

import { EmptyState } from "./EmptyState";
import { Icon } from "./Icon";

type ArtistAvailabilityPanelProps = {
  items: ArtistAvailability[];
  onCreate: (input: Omit<ArtistAvailability, "id">) => Promise<void>;
};

export function ArtistAvailabilityPanel({ items, onCreate }: ArtistAvailabilityPanelProps) {
  const [startsAt, setStartsAt] = useState("");
  const [endsAt, setEndsAt] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (new Date(endsAt) <= new Date(startsAt)) {
      setError("End time must be after start time.");
      return;
    }
    setBusy(true);
    setError("");
    try {
      await onCreate({
        starts_at: new Date(startsAt).toISOString(),
        ends_at: new Date(endsAt).toISOString(),
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC",
      });
      setStartsAt("");
      setEndsAt("");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to add availability.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="split-panel">
      <form className="data-form compact-form" onSubmit={submit}>
        <label>Available from<input required type="datetime-local" value={startsAt} onChange={(event) => setStartsAt(event.target.value)} /></label>
        <label>Available until<input required type="datetime-local" value={endsAt} onChange={(event) => setEndsAt(event.target.value)} /></label>
        <button disabled={busy} type="submit"><Icon name="create" />{busy ? "Adding…" : "Add availability"}</button>
        {error && <p className="form-error" role="alert">{error}</p>}
      </form>
      <div className="record-list">
        {items.length === 0 ? (
          <EmptyState
            hint="Add a start and end time on the left. The agency books only inside these windows."
            icon="schedule"
            title="No availability added yet"
          />
        ) : items.map((item) => (
          <article key={item.id}><strong>{new Date(item.starts_at).toLocaleString("en-US")}</strong><span>to {new Date(item.ends_at).toLocaleString("en-US")}</span><small>{item.timezone}</small></article>
        ))}
      </div>
    </div>
  );
}
