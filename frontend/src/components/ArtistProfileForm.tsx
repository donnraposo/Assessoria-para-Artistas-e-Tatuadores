"use client";

import { FormEvent, useState } from "react";

import { ProfileDraftValidator } from "@/lib/artist/ProfileDraftValidator";
import { StyleListParser } from "@/lib/artist/StyleListParser";
import type { ArtistProfileDraft } from "@/lib/types/artist";

type ArtistProfileFormProps = {
  draft: ArtistProfileDraft;
  saving: boolean;
  onSave: (draft: ArtistProfileDraft) => void;
};

export function ArtistProfileForm({ draft, saving, onSave }: ArtistProfileFormProps) {
  const [values, setValues] = useState(draft);
  const [styleText, setStyleText] = useState(StyleListParser.format(draft.styles));
  const [messages, setMessages] = useState<string[]>([]);

  function update<TField extends keyof ArtistProfileDraft>(
    field: TField,
    value: ArtistProfileDraft[TField],
  ) {
    setValues((current) => ({ ...current, [field]: value }));
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const candidate = { ...values, styles: StyleListParser.parse(styleText) };
    const validation = ProfileDraftValidator.validate(candidate);
    setMessages(validation);
    if (validation.length > 0) return;
    onSave(candidate);
  }

  return (
    <form className="record-form" onSubmit={handleSubmit}>
      <div className="field-grid">
        <p className="field field-wide">
          <label htmlFor="professional_name">Professional name</label>
          <input
            id="professional_name"
            maxLength={160}
            onChange={(event) => update("professional_name", event.target.value)}
            required
            value={values.professional_name}
          />
        </p>
        <p className="field field-wide">
          <label htmlFor="biography">Biography</label>
          <textarea
            id="biography"
            onChange={(event) => update("biography", event.target.value)}
            rows={4}
            value={values.biography}
          />
        </p>
        <p className="field field-wide">
          <label htmlFor="styles">Tattoo styles</label>
          <input
            id="styles"
            onChange={(event) => setStyleText(event.target.value)}
            value={styleText}
          />
          <small>Separate each style with a comma. At least one is required to submit.</small>
        </p>
        <p className="field">
          <label htmlFor="years_experience">Years of experience</label>
          <input
            id="years_experience"
            min={0}
            onChange={(event) => update("years_experience", Number(event.target.value))}
            type="number"
            value={values.years_experience}
          />
        </p>
        <p className="field">
          <label htmlFor="currency">Currency</label>
          <input
            id="currency"
            maxLength={3}
            onChange={(event) => update("currency", event.target.value.toUpperCase())}
            value={values.currency}
          />
        </p>
        <p className="field">
          <label htmlFor="minimum_tattoo_value">Minimum tattoo value</label>
          <input
            id="minimum_tattoo_value"
            inputMode="decimal"
            onChange={(event) => update("minimum_tattoo_value", event.target.value)}
            value={values.minimum_tattoo_value}
          />
          <small>The Advisory team never closes a tattoo below this value.</small>
        </p>
        <p className="field">
          <label htmlFor="expected_ticket">Expected ticket</label>
          <input
            id="expected_ticket"
            inputMode="decimal"
            onChange={(event) => update("expected_ticket", event.target.value)}
            value={values.expected_ticket}
          />
        </p>
        <p className="field">
          <label htmlFor="daily_session_value">Daily session value (optional)</label>
          <input
            id="daily_session_value"
            inputMode="decimal"
            onChange={(event) =>
              update("daily_session_value", event.target.value === "" ? null : event.target.value)
            }
            value={values.daily_session_value ?? ""}
          />
        </p>
      </div>
      {messages.length > 0 && (
        <ul className="form-error" role="alert">
          {messages.map((message) => (
            <li key={message}>{message}</li>
          ))}
        </ul>
      )}
      <div className="form-actions">
        <button disabled={saving} type="submit">{saving ? "Saving…" : "Save profile"}</button>
      </div>
    </form>
  );
}
