"use client";

import { useState } from "react";

import type { StudioProfile, StudioProfileInput } from "@/lib/api";

type StudioProfileFormProps = {
  profile: StudioProfile;
  onSave: (input: StudioProfileInput) => Promise<void>;
};

export function StudioProfileForm({ profile, onSave }: StudioProfileFormProps) {
  const [form, setForm] = useState({ ...profile, amenitiesText: profile.amenities.join(", ") });
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    setBusy(true);
    setMessage("");
    setError("");
    try {
      await onSave({
        name: form.name,
        country_code: form.country_code.toUpperCase(),
        city: form.city,
        address: form.address,
        description: form.description,
        amenities: form.amenitiesText.split(",").map((item) => item.trim()).filter(Boolean),
        offers_accommodation: form.offers_accommodation,
        accommodation_details: form.accommodation_details,
      });
      setMessage("Studio profile saved.");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to save Studio profile.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <form className="data-form" onSubmit={submit}>
      <div className="form-grid">
        <label>Studio name<input required value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} /></label>
        <label>Country code<input maxLength={2} required value={form.country_code} onChange={(event) => setForm({ ...form, country_code: event.target.value })} /></label>
        <label>City<input required value={form.city} onChange={(event) => setForm({ ...form, city: event.target.value })} /></label>
        <label>Address<input required value={form.address} onChange={(event) => setForm({ ...form, address: event.target.value })} /></label>
        <label className="form-span">Description<textarea value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} /></label>
        <label className="form-span">Amenities, separated by commas<input value={form.amenitiesText} onChange={(event) => setForm({ ...form, amenitiesText: event.target.value })} /></label>
        <label className="checkbox-label"><input checked={form.offers_accommodation} onChange={(event) => setForm({ ...form, offers_accommodation: event.target.checked })} type="checkbox" />Offers accommodation</label>
        <label>Accommodation details<input disabled={!form.offers_accommodation} value={form.accommodation_details} onChange={(event) => setForm({ ...form, accommodation_details: event.target.value })} /></label>
      </div>
      <div className="form-actions"><button disabled={busy} type="submit">{busy ? "Saving…" : "Save Studio"}</button>{message && <span className="success-message">{message}</span>}</div>
      {error && <p className="form-error" role="alert">{error}</p>}
    </form>
  );
}
