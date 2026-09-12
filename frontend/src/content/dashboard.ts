import type { IconName } from "@/components/iconName";

export type QueueActionId =
  | "approve"
  | "reject"
  | "mark-ready"
  | "confirm-guest"
  | "confirm-booking"
  | "approve-cancellation"
  | "reject-cancellation";

export type QueueActionDefinition = {
  id: QueueActionId;
  label: string;
  tone: "approve" | "reject" | "neutral";
  statuses: readonly string[];
  requiresReason?: boolean;
};

export type NavigationItem = {
  label: string;
  short: string;
  href: string;
  icon: IconName;
};

const reviewActions: readonly QueueActionDefinition[] = [
  { id: "approve", label: "Approve", tone: "approve", statuses: ["UNDER_REVIEW"] },
  { id: "reject", label: "Reject", tone: "reject", statuses: ["UNDER_REVIEW"], requiresReason: true },
];

export const queueDefinitions = [
  { key: "artist_applications", slug: "artist-applications", label: "Artist applications", detail: "Awaiting review", hint: "Approve or reject artists who applied to the agency.", icon: "artist", columns: ["artist_id", "status", "submitted_at"], actions: reviewActions },
  { key: "studios", slug: "studios", label: "Studio applications", detail: "Awaiting review", hint: "Approve partner Studios so they can host Guests.", icon: "studio", columns: ["name", "city", "country_code", "status"], actions: reviewActions },
  { key: "guest_proposals", slug: "guest-proposals", label: "Guest proposals", detail: "Planning or ready", hint: "Move a planned trip forward until the Guest is confirmed.", icon: "proposal", columns: ["artist_id", "city", "country_code", "status"], actions: [
    { id: "mark-ready", label: "Mark ready", tone: "neutral", statuses: ["PLANNING"] },
    { id: "confirm-guest", label: "Confirm Guest", tone: "approve", statuses: ["READY"] },
  ] },
  { key: "studio_reservations", slug: "studio-reservations", label: "Studio reservations", detail: "Require action", hint: "Confirm the Studio bookings already accepted by the partner.", icon: "reservation", columns: ["guest_id", "studio_id", "status", "starts_at"], actions: [
    { id: "confirm-booking", label: "Confirm booking", tone: "approve", statuses: ["ACCEPTED"] },
  ] },
  { key: "open_leads", slug: "open-leads", label: "Open leads", detail: "In negotiation", hint: "Register the 20% payment to close a sale and confirm its appointment.", icon: "lead", columns: ["client_name", "source", "appointment_id", "status"], actions: [] },
  { key: "cancellations", slug: "cancellations", label: "Cancellations", detail: "Awaiting decision", hint: "Decide on cancellation requests sent by artists.", icon: "cancellation", columns: ["appointment_id", "reason", "status", "created_at"], actions: [
    { id: "approve-cancellation", label: "Approve", tone: "approve", statuses: ["PENDING"], requiresReason: true },
    { id: "reject-cancellation", label: "Keep appointment", tone: "reject", statuses: ["PENDING"], requiresReason: true },
  ] },
  { key: "logistics", slug: "logistics", label: "Logistics", detail: "Pending updates", hint: "Keep travel and accommodation details up to date for each Guest.", icon: "logistics", columns: ["item_type", "guest_id", "status", "updated_at"], actions: [] },
] as const;

const overviewItem: NavigationItem = { label: "Overview", short: "Overview", href: "/", icon: "overview" };

export function getNavigationItems(role: string): NavigationItem[] {
  if (role.toUpperCase() === "ARTIST") {
    return [
      overviewItem,
      { label: "Profile & availability", short: "Profile", href: "/artist/profile", icon: "artist" },
      { label: "Guests & My Trip", short: "Guests", href: "/artist/guests", icon: "guest" },
      { label: "Schedule", short: "Schedule", href: "/artist/schedule", icon: "schedule" },
      { label: "Portfolio", short: "Portfolio", href: "/artist/portfolio", icon: "portfolio" },
    ];
  }
  if (role.toUpperCase() === "STUDIO") {
    return [
      overviewItem,
      { label: "Studio profile", short: "Profile", href: "/studio/profile", icon: "studio" },
      { label: "Reservation requests", short: "Requests", href: "/studio/reservations", icon: "reservation" },
    ];
  }
  if (role.toUpperCase() !== "ADVISORY") return [overviewItem];
  return [
    overviewItem,
    { label: "Create records", short: "Create", href: "/operations/create", icon: "create" },
    ...queueDefinitions.map((queue) => ({
      label: queue.label,
      short: queue.label.split(" ")[0],
      href: `/operations/${queue.slug}`,
      icon: queue.icon as IconName,
    })),
  ];
}
