"use client";

import { useState } from "react";

import type { StudioBooking } from "@/lib/api";
import { formatOperationalValue } from "@/lib/format";

import { EmptyState } from "./EmptyState";
import { Icon } from "./Icon";
import { StatusBadge } from "./StatusBadge";

type StudioBookingPaymentPanelProps = {
  items: StudioBooking[];
  onMarkAsPaid: (bookingId: string) => Promise<void>;
};

export function StudioBookingPaymentPanel({ items, onMarkAsPaid }: StudioBookingPaymentPanelProps) {
  const [busyId, setBusyId] = useState<string | null>(null);
  const [error, setError] = useState("");

  const markAsPaid = async (booking: StudioBooking) => {
    if (!window.confirm("Mark this Studio booking as paid?")) return;
    setBusyId(booking.id);
    setError("");
    try {
      await onMarkAsPaid(booking.id);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to update payment status.");
    } finally {
      setBusyId(null);
    }
  };

  return (
    <div className="record-list">
      {items.length === 0 ? (
        <EmptyState
          hint="Confirmed Studio bookings for this Guest will appear here."
          icon="reservation"
          title="No Studio bookings yet"
        />
      ) : items.map((item) => (
        <article key={item.id}>
          <strong>{formatOperationalValue("starts_at", item.starts_at)}</strong>
          <span>to {formatOperationalValue("ends_at", item.ends_at)}</span>
          <div className="row-meta">
            <StatusBadge status={item.payment_status} />
            {item.payment_status !== "PAID" && (
              <button className="quiet-action" disabled={busyId === item.id} onClick={() => markAsPaid(item)} type="button">
                <Icon name="revenue" />{busyId === item.id ? "Saving…" : "Mark as paid"}
              </button>
            )}
          </div>
        </article>
      ))}
      {error && <p className="form-error" role="alert">{error}</p>}
    </div>
  );
}
