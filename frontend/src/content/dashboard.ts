export const navigationItems = [{ label: "Overview", href: "/" }] as const;

export const queueDefinitions = [
  { key: "artist_applications", label: "Artist applications", detail: "Awaiting review" },
  { key: "studios", label: "Studio applications", detail: "Awaiting review" },
  { key: "guest_proposals", label: "Guest proposals", detail: "Planning or ready" },
  { key: "studio_reservations", label: "Studio reservations", detail: "Require action" },
  { key: "open_leads", label: "Open leads", detail: "In negotiation" },
  { key: "cancellations", label: "Cancellations", detail: "Awaiting decision" },
  { key: "logistics", label: "Logistics", detail: "Pending updates" },
] as const;
