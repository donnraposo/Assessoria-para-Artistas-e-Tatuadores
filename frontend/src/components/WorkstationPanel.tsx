"use client";

import { useState } from "react";

import type { Workstation, WorkstationInput } from "@/lib/api";

import { EmptyState } from "./EmptyState";
import { Icon } from "./Icon";

type WorkstationPanelProps = {
  items: Workstation[];
  onCreate: (input: WorkstationInput) => Promise<void>;
};

export function WorkstationPanel({ items, onCreate }: WorkstationPanelProps) {
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      await onCreate({ name });
      setName("");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to add workstation.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="split-panel">
      <form className="data-form compact-form" onSubmit={submit}>
        <label>Workstation name<input required value={name} onChange={(event) => setName(event.target.value)} /></label>
        <button disabled={busy} type="submit"><Icon name="create" />{busy ? "Adding…" : "Add workstation"}</button>
        {error && <p className="form-error" role="alert">{error}</p>}
      </form>
      <div className="record-list">
        {items.length === 0 ? (
          <EmptyState
            hint="Add each bench or chair available for bookings. Pricing and availability can target a specific one."
            icon="studio"
            title="No workstations added yet"
          />
        ) : items.map((item) => (
          <article key={item.id}><strong>{item.name}</strong></article>
        ))}
      </div>
    </div>
  );
}
