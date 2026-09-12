"use client";

import { useState } from "react";

import { Icon } from "./Icon";

type CancellationRequestControlsProps = {
  clientName: string;
  onSubmit: (reason: string) => Promise<void>;
};

export function CancellationRequestControls({ clientName, onSubmit }: CancellationRequestControlsProps) {
  const [reason, setReason] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const submit = async () => {
    if (!reason.trim()) {
      setError("Add a cancellation reason.");
      return;
    }
    if (!window.confirm(`Request cancellation for ${clientName}?`)) return;
    setBusy(true);
    setError("");
    try {
      await onSubmit(reason.trim());
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to request cancellation.");
      setBusy(false);
    }
  };

  return (
    <div className="review-controls">
      <input disabled={busy} onChange={(event) => setReason(event.target.value)} placeholder="Cancellation reason" value={reason} />
      <button className="reject-action" disabled={busy} onClick={submit} type="button"><Icon name="cancellation" />Request cancellation</button>
      {error && <small role="alert">{error}</small>}
    </div>
  );
}
