export type NavigationItem = { label: string; href: string };

export type QueueDefinition = {
  key: string;
  label: string;
  detail: string;
  href?: string;
};

export const advisoryNavigation: NavigationItem[] = [
  { label: "Overview", href: "/" },
  { label: "Artist applications", href: "/queues/artist-applications" },
];

export const artistNavigation: NavigationItem[] = [
  { label: "Overview", href: "/" },
  { label: "My application", href: "/artist/application" },
];

export const studioNavigation: NavigationItem[] = [{ label: "Overview", href: "/" }];

export function navigationFor(roles: string[]): NavigationItem[] {
  if (roles.includes("ADVISORY")) return advisoryNavigation;
  if (roles.includes("ARTIST")) return artistNavigation;
  return studioNavigation;
}

export const queueDefinitions: QueueDefinition[] = [
  {
    key: "artist_applications",
    label: "Artist applications",
    detail: "Awaiting review",
    href: "/queues/artist-applications",
  },
  { key: "studios", label: "Studio applications", detail: "Awaiting review" },
  { key: "guest_proposals", label: "Guest proposals", detail: "Planning or ready" },
  { key: "studio_reservations", label: "Studio reservations", detail: "Require action" },
  { key: "open_leads", label: "Open leads", detail: "In negotiation" },
  { key: "cancellations", label: "Cancellations", detail: "Awaiting decision" },
  { key: "logistics", label: "Logistics", detail: "Pending updates" },
];
