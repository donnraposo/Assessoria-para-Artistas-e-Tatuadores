"use client";

import { useState } from "react";

import type { StudioPrice, StudioPriceInput } from "@/lib/api";

import { EmptyState } from "./EmptyState";
import { Icon } from "./Icon";

type StudioPricePanelProps = {
  items: StudioPrice[];
  onCreate: (input: StudioPriceInput) => Promise<void>;
};

const pricingTypes = [
  { value: "HOURLY", label: "Hourly" },
  { value: "DAILY", label: "Daily" },
  { value: "WEEKLY", label: "Weekly" },
  { value: "PERCENTAGE", label: "Percentage" },
  { value: "NEGOTIATED", label: "Negotiated" },
];

export function StudioPricePanel({ items, onCreate }: StudioPricePanelProps) {
  const [pricingType, setPricingType] = useState("DAILY");
  const [amount, setAmount] = useState("");
  const [currency, setCurrency] = useState("BRL");
  const [validFrom, setValidFrom] = useState("");
  const [validUntil, setValidUntil] = useState("");
  const [conditions, setConditions] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      await onCreate({
        pricing_type: pricingType,
        amount,
        currency: currency.toUpperCase(),
        valid_from: validFrom,
        valid_until: validUntil || null,
        conditions,
      });
      setAmount("");
      setValidUntil("");
      setConditions("");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to add pricing.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="split-panel">
      <form className="data-form compact-form" onSubmit={submit}>
        <label>Pricing type
          <select value={pricingType} onChange={(event) => setPricingType(event.target.value)}>
            {pricingTypes.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
          </select>
        </label>
        <label>Amount<input required min="0" step="0.01" type="number" value={amount} onChange={(event) => setAmount(event.target.value)} /></label>
        <label>Currency<input required maxLength={3} value={currency} onChange={(event) => setCurrency(event.target.value)} /></label>
        <label>Valid from<input required type="date" value={validFrom} onChange={(event) => setValidFrom(event.target.value)} /></label>
        <label>Valid until<input type="date" value={validUntil} onChange={(event) => setValidUntil(event.target.value)} /></label>
        <label>Conditions<textarea value={conditions} onChange={(event) => setConditions(event.target.value)} /></label>
        <button disabled={busy} type="submit"><Icon name="create" />{busy ? "Adding…" : "Add pricing"}</button>
        {error && <p className="form-error" role="alert">{error}</p>}
      </form>
      <div className="record-list">
        {items.length === 0 ? (
          <EmptyState
            hint="Register how the Studio charges the agency, such as a daily rate or a percentage."
            icon="revenue"
            title="No pricing registered yet"
          />
        ) : items.map((item) => (
          <article key={item.id}>
            <strong>{pricingTypes.find((option) => option.value === item.pricing_type)?.label ?? item.pricing_type}: {item.amount} {item.currency}</strong>
            <span>From {item.valid_from}{item.valid_until ? ` to ${item.valid_until}` : ""}</span>
            {item.conditions && <small>{item.conditions}</small>}
          </article>
        ))}
      </div>
    </div>
  );
}
