const cardHints: Record<string, string> = {
  active_guests: "Trips already confirmed for you.",
  upcoming_appointments: "Tattoos scheduled and paid for.",
  pending_logistics: "Travel and stay the agency is still arranging.",
  notifications: "Updates you have not opened yet.",
  pending_requests: "Bookings waiting for your answer.",
  accepted_requests: "Bookings you accepted, awaiting agency confirmation.",
  confirmed_bookings: "Dates locked in your Studio.",
};

export function workspaceCardHint(key: string): string | undefined {
  return cardHints[key];
}
