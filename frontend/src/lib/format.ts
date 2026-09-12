export function formatCurrency(value: string, currency: string): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    maximumFractionDigits: 2,
  }).format(Number(value));
}

export function humanizeAction(action: string): string {
  return action
    .replaceAll(".", " ")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export function humanizeField(field: string): string {
  return field.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export type StatusTone = "positive" | "danger" | "warning" | "info" | "neutral";

const statusTones: Record<StatusTone, readonly string[]> = {
  positive: ["APPROVED", "CONFIRMED", "ACCEPTED", "PAID", "FINISHED", "CLOSED", "READY", "COMPLETED", "ACTIVE"],
  danger: ["REJECTED", "REFUSED", "DECLINED", "CANCELLED", "CANCELED", "FAILED", "EXPIRED"],
  warning: ["UNDER_REVIEW", "PENDING", "REQUESTED", "CANCELLATION_REQUESTED", "AWAITING_DECISION"],
  info: ["PLANNING", "IN_CAPTURE", "IN_PROGRESS", "SCHEDULE_FULL", "OPEN", "SUBMITTED"],
  neutral: ["DRAFT", "INACTIVE"],
};

export function statusTone(status: string | number | null): StatusTone {
  const normalized = String(status ?? "").toUpperCase();
  const match = (Object.keys(statusTones) as StatusTone[]).find((tone) => statusTones[tone].includes(normalized));
  return match ?? "neutral";
}

export function formatOperationalValue(field: string, value: string | number | null): string {
  if (value === null || value === "") return "—";
  if (field.endsWith("_at")) {
    return new Intl.DateTimeFormat("en-US", {
      dateStyle: "medium",
      timeStyle: "short",
    }).format(new Date(String(value)));
  }
  if (field === "status") return humanizeField(String(value).toLowerCase());
  return String(value);
}
