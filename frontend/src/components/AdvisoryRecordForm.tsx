"use client";

import { useState, type FormEvent } from "react";

import type { AdvisoryFormDefinition, FormFieldDefinition } from "@/content/operationsForms";

type AdvisoryRecordFormProps = {
  definition: AdvisoryFormDefinition;
  onSubmit: (payload: Record<string, unknown>) => Promise<void>;
};

function initialValues(fields: FormFieldDefinition[]) {
  return Object.fromEntries(
    fields.map((field) => [field.name, field.defaultValue ?? (field.required ? field.options?.[0]?.value : "") ?? ""]),
  );
}

function buildPayload(fields: FormFieldDefinition[], values: Record<string, string>) {
  return Object.fromEntries(
    fields.flatMap((field) => {
      const rawValue = values[field.name]?.trim() ?? "";
      if (!rawValue && !field.required) return [];
      const value = field.type === "datetime" ? new Date(rawValue).toISOString() : rawValue;
      const normalized = ["country_code", "currency"].includes(field.name)
        ? String(value).toUpperCase()
        : value;
      return [[field.name, normalized]];
    }),
  );
}

export function AdvisoryRecordForm({ definition, onSubmit }: AdvisoryRecordFormProps) {
  const [values, setValues] = useState<Record<string, string>>(() => initialValues(definition.fields));
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const updateValue = (name: string, value: string) => {
    setValues((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!window.confirm(`Create this ${definition.title.toLowerCase()}?`)) return;
    setLoading(true);
    setError("");
    setSuccess("");
    try {
      await onSubmit(buildPayload(definition.fields, values));
      setValues(initialValues(definition.fields));
      setSuccess(`${definition.title} created successfully.`);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to create record.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <details className="creation-card">
      <summary>
        <span><strong>{definition.title}</strong><small>{definition.description}</small></span>
        <b>+</b>
      </summary>
      <form className="data-form creation-form" onSubmit={handleSubmit}>
        <div className="form-grid">
          {definition.fields.map((field) => (
            <label className={field.type === "textarea" ? "form-span" : undefined} key={field.name}>
              {field.label}
              {field.type === "select" ? (
                <select required={field.required} value={values[field.name]} onChange={(event) => updateValue(field.name, event.target.value)}>
                  {!field.required && <option value="">Not selected</option>}
                  {field.options?.length ? field.options.map((option) => <option key={option.value} value={option.value}>{option.label}</option>) : field.required && <option value="">No eligible records</option>}
                </select>
              ) : field.type === "textarea" ? (
                <textarea required={field.required} value={values[field.name]} onChange={(event) => updateValue(field.name, event.target.value)} />
              ) : (
                <input
                  required={field.required}
                  step={field.type === "number" ? "0.01" : undefined}
                  type={field.type === "datetime" ? "datetime-local" : field.type}
                  value={values[field.name]}
                  onChange={(event) => updateValue(field.name, event.target.value)}
                />
              )}
            </label>
          ))}
        </div>
        {error && <p className="form-error" role="alert">{error}</p>}
        {success && <p className="success-message" role="status">{success}</p>}
        <button disabled={loading || definition.fields.some((field) => field.required && !values[field.name])} type="submit">
          {loading ? "Creating…" : definition.submitLabel}
        </button>
      </form>
    </details>
  );
}
