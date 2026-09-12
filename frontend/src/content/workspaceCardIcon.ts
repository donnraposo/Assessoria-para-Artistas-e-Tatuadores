import type { IconName } from "@/components/iconName";

const cardIcons: Record<string, IconName> = {
  active_guests: "guest",
  upcoming_appointments: "schedule",
  pending_logistics: "logistics",
  notifications: "bell",
  pending_requests: "pending",
  accepted_requests: "approved",
  confirmed_bookings: "reservation",
};

export function workspaceCardIcon(key: string): IconName {
  return cardIcons[key] ?? "overview";
}
