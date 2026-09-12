"use client";

import { useState } from "react";

import type { StudioAvailabilitySlot, StudioAvailabilitySlotInput, Workstation } from "@/lib/api";

import { EmptyState } from "./EmptyState";
import { Icon } from "./Icon";

type StudioAvailabilityPanelProps = {
  items: StudioAvailabilitySlot[];
  workstations: Workstation[];
  onCreate: (input: StudioAvailabilitySlotInput) => Promise<void>;
};

export function StudioAvailabilityPanel({ items, workstations, onCreate }: StudioAvailabilityPanelProps) {
  const [workstationId, setWorkstationId] = useState("");
  const [startsAt, setStartsAt] = useState("");
  const [endsAt, setEndsAt] = useState("");
  const [capacity, setCapacity] = useState("1");
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
        workstation: workstationId || null,
        starts_at: new Date(startsAt).toISOString(),
        ends_at: new Date(endsAt).toISOString(),
        capacity: Number(capacity),
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC",
      });
      setStartsAt("");
      setEndsAt("");
      setCapacity("1");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to add availability.");
    } finally {
      setBusy(false);
    }
  };

  const workstationName = (id: string | null) => workstations.find((workstation) => workstation.id === id)?.name ?? "Any workstation";

  return (
    <div className="split-panel">
      <form className="data-form compact-form" onSubmit={submit}>
        <label>Workstation
          <select value={workstationId} onChange={(event) => setWorkstationId(event.target.value)}>
            <option value="">Any workstation</option>
            {workstations.map((workstation) => <option key={workstation.id} value={workstation.id}>{workstation.name}</option>)}
          </select>
        </label>
        <label>Available from<input required type="datetime-local" value={startsAt} onChange={(event) => setStartsAt(event.target.value)} /></label>
        <label>Available until<input required type="datetime-local" value={endsAt} onChange={(event) => setEndsAt(event.target.value)} /></label>
        <label>Capacity<input required min="1" type="number" value={capacity} onChange={(event) => setCapacity(event.target.value)} /></label>
        <button disabled={busy} type="submit"><Icon name="create" />{busy ? "Adding…" : "Add availability"}</button>
        {error && <p className="form-error" role="alert">{error}</p>}
      </form>
      <div className="record-list">
        {items.length === 0 ? (
          <EmptyState
            hint="Add the periods the Studio can host Guests. The agency only books inside these windows."
            icon="schedule"
            title="No availability added yet"
          />
        ) : items.map((item) => (
          <article key={item.id}>
            <strong>{new Date(item.starts_at).toLocaleString("en-US")}</strong>
            <span>to {new Date(item.ends_at).toLocaleString("en-US")}</span>
            <small>{workstationName(item.workstation)} · Capacity {item.capacity} · {item.timezone}</small>
          </article>
        ))}
      </div>
    </div>
  );
}
