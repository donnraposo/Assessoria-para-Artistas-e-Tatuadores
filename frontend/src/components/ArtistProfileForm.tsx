"use client";

import { useState } from "react";

import type { ArtistProfile, ArtistProfileInput } from "@/lib/api";

type ArtistProfileFormProps = {
  profile: ArtistProfile;
  onSave: (input: ArtistProfileInput) => Promise<void>;
};

export function ArtistProfileForm({ profile, onSave }: ArtistProfileFormProps) {
  const [form, setForm] = useState({ ...profile, stylesText: profile.styles.join(", ") });
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
        professional_name: form.professional_name,
        biography: form.biography,
        years_experience: Number(form.years_experience),
        styles: form.stylesText.split(",").map((style) => style.trim()).filter(Boolean),
        currency: form.currency.toUpperCase(),
        minimum_tattoo_value: form.minimum_tattoo_value,
        expected_ticket: form.expected_ticket,
        daily_session_value: form.daily_session_value || null,
      });
      setMessage("Profile saved.");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to save profile.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <form className="data-form" onSubmit={submit}>
      <div className="form-grid">
        <label>Professional name<input required value={form.professional_name} onChange={(event) => setForm({ ...form, professional_name: event.target.value })} /></label>
        <label>Years of experience<input min="0" required type="number" value={form.years_experience} onChange={(event) => setForm({ ...form, years_experience: Number(event.target.value) })} /></label>
        <label className="form-span">Biography<textarea value={form.biography} onChange={(event) => setForm({ ...form, biography: event.target.value })} /></label>
        <label className="form-span">Styles, separated by commas<input required value={form.stylesText} onChange={(event) => setForm({ ...form, stylesText: event.target.value })} /></label>
        <label>Currency<input maxLength={3} required value={form.currency} onChange={(event) => setForm({ ...form, currency: event.target.value })} /></label>
        <label>Minimum tattoo value<input min="0" required step="0.01" type="number" value={form.minimum_tattoo_value} onChange={(event) => setForm({ ...form, minimum_tattoo_value: event.target.value })} /></label>
        <label>Expected ticket<input min="0" required step="0.01" type="number" value={form.expected_ticket} onChange={(event) => setForm({ ...form, expected_ticket: event.target.value })} /></label>
        <label>Daily session value<input min="0" step="0.01" type="number" value={form.daily_session_value ?? ""} onChange={(event) => setForm({ ...form, daily_session_value: event.target.value })} /></label>
      </div>
      <div className="form-actions"><button disabled={busy} type="submit">{busy ? "Saving…" : "Save profile"}</button>{message && <span className="success-message">{message}</span>}</div>
      {error && <p className="form-error" role="alert">{error}</p>}
    </form>
  );
}
