"use client";

import { useState } from "react";

import type { ArtistAvailability, ArtistAvailabilityInput } from "@/lib/api";

import { EmptyState } from "./EmptyState";
import { Icon } from "./Icon";

type ArtistAvailabilityPanelProps = {
  items: ArtistAvailability[];
  onCreate: (input: ArtistAvailabilityInput) => Promise<void>;
  onUpdate: (id: string, input: ArtistAvailabilityInput) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
};

function toLocalInputValue(isoValue: string): string {
  const date = new Date(isoValue);
  const offsetMs = date.getTimezoneOffset() * 60000;
  return new Date(date.getTime() - offsetMs).toISOString().slice(0, 16);
}

export function ArtistAvailabilityPanel({ items, onCreate, onUpdate, onDelete }: ArtistAvailabilityPanelProps) {
  const [startsAt, setStartsAt] = useState("");
  const [endsAt, setEndsAt] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editStartsAt, setEditStartsAt] = useState("");
  const [editEndsAt, setEditEndsAt] = useState("");
  const [rowBusy, setRowBusy] = useState<string | null>(null);
  const [rowError, setRowError] = useState("");

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

  const startEditing = (item: ArtistAvailability) => {
    setEditingId(item.id);
    setEditStartsAt(toLocalInputValue(item.starts_at));
    setEditEndsAt(toLocalInputValue(item.ends_at));
    setRowError("");
  };

  const submitEdit = async (item: ArtistAvailability, event: React.FormEvent) => {
    event.preventDefault();
    if (new Date(editEndsAt) <= new Date(editStartsAt)) {
      setRowError("End time must be after start time.");
      return;
    }
    setRowBusy(item.id);
    setRowError("");
    try {
      await onUpdate(item.id, {
        starts_at: new Date(editStartsAt).toISOString(),
        ends_at: new Date(editEndsAt).toISOString(),
        timezone: item.timezone,
      });
      setEditingId(null);
    } catch (requestError) {
      setRowError(requestError instanceof Error ? requestError.message : "Unable to update availability.");
    } finally {
      setRowBusy(null);
    }
  };

  const remove = async (item: ArtistAvailability) => {
    if (!window.confirm("Remove this availability window?")) return;
    setRowBusy(item.id);
    setRowError("");
    try {
      await onDelete(item.id);
    } catch (requestError) {
      setRowError(requestError instanceof Error ? requestError.message : "Unable to remove availability.");
      setRowBusy(null);
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
          <article key={item.id}>
            {editingId === item.id ? (
              <form className="data-form compact-form" onSubmit={(event) => submitEdit(item, event)}>
                <label>Available from<input required type="datetime-local" value={editStartsAt} onChange={(event) => setEditStartsAt(event.target.value)} /></label>
                <label>Available until<input required type="datetime-local" value={editEndsAt} onChange={(event) => setEditEndsAt(event.target.value)} /></label>
                <div className="form-actions">
                  <button disabled={rowBusy === item.id} type="submit">{rowBusy === item.id ? "Saving…" : "Save"}</button>
                  <button className="quiet-action" disabled={rowBusy === item.id} onClick={() => setEditingId(null)} type="button">Cancel</button>
                </div>
              </form>
            ) : (
              <>
                <strong>{new Date(item.starts_at).toLocaleString("en-US")}</strong>
                <span>to {new Date(item.ends_at).toLocaleString("en-US")}</span>
                <small>{item.timezone}</small>
                {item.changed_by_advisory ? (
                  <small className="muted-label">Managed by Advisory{item.change_reason ? `: ${item.change_reason}` : ""}</small>
                ) : (
                  <div className="row-meta">
                    <button className="quiet-action" onClick={() => startEditing(item)} type="button">Edit</button>
                    <button className="quiet-action" disabled={rowBusy === item.id} onClick={() => remove(item)} type="button">
                      <Icon name="trash" />Remove
                    </button>
                  </div>
                )}
              </>
            )}
          </article>
        ))}
        {rowError && <p className="form-error" role="alert">{rowError}</p>}
      </div>
    </div>
  );
}
