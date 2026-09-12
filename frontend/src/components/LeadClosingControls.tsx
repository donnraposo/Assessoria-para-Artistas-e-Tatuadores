"use client";

import { useState } from "react";

import type { LeadClosingInput } from "@/lib/api";

import { Icon } from "./Icon";

type LeadClosingControlsProps = {
  appointmentId: string;
  clientName: string;
  onClose: (input: LeadClosingInput) => Promise<void>;
};

export function LeadClosingControls({ appointmentId, clientName, onClose }: LeadClosingControlsProps) {
  const [form, setForm] = useState<LeadClosingInput>({
    appointmentId,
    finalValue: "",
    currency: "BRL",
    artistMinimumApproved: false,
    paymentReference: "",
  });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const submit = async () => {
    if (!form.appointmentId || Number(form.finalValue) <= 0 || !/^[A-Z]{3}$/.test(form.currency) || !form.paymentReference.trim()) {
      setError("Complete the appointment, value, currency, and payment reference.");
      return;
    }
    if (!window.confirm(`Confirm payment and close the Lead for ${clientName}?`)) return;
    setBusy(true);
    setError("");
    try {
      await onClose(form);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Closing failed.");
      setBusy(false);
    }
  };

  return (
    <div className="closing-controls">
      <input aria-label="Appointment ID" disabled={busy} onChange={(event) => setForm({ ...form, appointmentId: event.target.value })} placeholder="Appointment ID" value={form.appointmentId} />
      <div>
        <input aria-label="Final value" disabled={busy} min="0.01" onChange={(event) => setForm({ ...form, finalValue: event.target.value })} placeholder="Final value" step="0.01" type="number" value={form.finalValue} />
        <input aria-label="Currency" disabled={busy} maxLength={3} onChange={(event) => setForm({ ...form, currency: event.target.value.toUpperCase() })} value={form.currency} />
      </div>
      <input aria-label="Payment reference" disabled={busy} onChange={(event) => setForm({ ...form, paymentReference: event.target.value })} placeholder="Payment reference" value={form.paymentReference} />
      <label><input checked={form.artistMinimumApproved} disabled={busy} onChange={(event) => setForm({ ...form, artistMinimumApproved: event.target.checked })} type="checkbox" />Artist approved minimum-price closing</label>
      <button disabled={busy} onClick={submit} type="button"><Icon name="revenue" />Confirm closing</button>
      {error && <small role="alert">{error}</small>}
    </div>
  );
}
