"use client";

import { useState } from "react";

import type { QueueActionDefinition, QueueActionId } from "@/content/dashboard";

import { Icon } from "./Icon";
import type { IconName } from "./iconName";

const toneIcons: Record<QueueActionDefinition["tone"], IconName> = {
  approve: "approved",
  reject: "declined",
  neutral: "arrow",
};

type QueueActionControlsProps = {
  actions: readonly QueueActionDefinition[];
  itemLabel: string;
  onAction: (action: QueueActionId, reason: string) => Promise<void>;
};

export function QueueActionControls({ actions, itemLabel, onAction }: QueueActionControlsProps) {
  const [reason, setReason] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const execute = async (action: QueueActionDefinition) => {
    const normalizedReason = reason.trim();
    if (action.requiresReason && !normalizedReason) {
      setError("Add a reason before continuing.");
      return;
    }
    if (!window.confirm(`Confirm “${action.label}” for ${itemLabel}?`)) return;
    setBusy(true);
    setError("");
    try {
      await onAction(action.id, normalizedReason);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Action failed.");
      setBusy(false);
    }
  };

  return (
    <div className="review-controls">
      {actions.some((action) => action.requiresReason) && (
        <input
          aria-label={`Decision reason for ${itemLabel}`}
          disabled={busy}
          onChange={(event) => setReason(event.target.value)}
          placeholder="Decision reason"
          value={reason}
        />
      )}
      <div>
        {actions.map((action) => (
          <button
            className={`${action.tone}-action`}
            disabled={busy}
            key={action.id}
            onClick={() => execute(action)}
            type="button"
          >
            <Icon name={toneIcons[action.tone]} />
            {action.label}
          </button>
        ))}
      </div>
      {error && <small role="alert">{error}</small>}
    </div>
  );
}
