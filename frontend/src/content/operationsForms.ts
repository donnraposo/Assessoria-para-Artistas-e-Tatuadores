import type { AdvisoryRecordKind, OperationsReferenceData } from "@/lib/api";

export type FormOption = { label: string; value: string };

export type FormFieldDefinition = {
  name: string;
  label: string;
  type: "text" | "number" | "date" | "datetime" | "email" | "tel" | "select" | "textarea";
  required?: boolean;
  defaultValue?: string;
  options?: readonly FormOption[];
};

export type AdvisoryFormDefinition = {
  id: AdvisoryRecordKind;
  title: string;
  description: string;
  submitLabel: string;
  fields: FormFieldDefinition[];
};

export function buildAdvisoryForms(data: OperationsReferenceData, timezone: string): AdvisoryFormDefinition[] {
  const artists = data.artists.map((artist) => ({ label: artist.professional_name, value: artist.id }));
  const studios = data.studios.map((studio) => ({ label: `${studio.name} · ${studio.city}`, value: studio.id }));
  const guests = data.guests.map((guest) => ({ label: `${guest.city} · ${guest.starts_on} · ${guest.status}`, value: guest.id }));
  const commonGuest = { name: "guest", label: "Guest", type: "select", options: guests, required: true } as const;
  const commonStudio = { name: "studio", label: "Studio", type: "select", options: studios, required: true } as const;
  const commonArtist = { name: "artist", label: "Artist", type: "select", options: artists, required: true } as const;
  const timezoneField = { name: "timezone", label: "Timezone", type: "text", defaultValue: timezone, required: true } as const;
  const currencies = [...new Set([...data.artists.map((artist) => artist.currency), ...data.guests.map((guest) => guest.currency)])].sort().map((currency) => ({ label: currency, value: currency }));
  const currencyField = { name: "currency", label: "Currency", type: "select", options: currencies.length ? currencies : [{ label: "BRL", value: "BRL" }], required: true } as const;
  return [
    {
      id: "proposal",
      title: "Guest proposal",
      description: "Create the commercial and operational plan for an approved Artist and Studio.",
      submitLabel: "Create proposal",
      fields: [commonArtist, { ...commonStudio, name: "primary_studio", label: "Primary Studio" }, { name: "city", label: "City", type: "text", required: true }, { name: "country_code", label: "Country code", type: "text", defaultValue: "BR", required: true }, { name: "starts_on", label: "Starts on", type: "date", required: true }, { name: "ends_on", label: "Ends on", type: "date", required: true }, timezoneField, currencyField, { name: "ads_budget", label: "Ads budget", type: "number", required: true }, { name: "minimum_tattoo_value", label: "Minimum tattoo value", type: "number", required: true }, { name: "expected_ticket", label: "Expected ticket", type: "number", required: true }, { name: "daily_session_value", label: "Daily session value", type: "number" }],
    },
    {
      id: "reservation",
      title: "Studio reservation request",
      description: "Send a reservation request to a partner Studio.",
      submitLabel: "Send request",
      fields: [commonGuest, commonStudio, commonArtist, { name: "starts_at", label: "Starts at", type: "datetime", required: true }, { name: "ends_at", label: "Ends at", type: "datetime", required: true }, timezoneField],
    },
    {
      id: "lead",
      title: "Lead",
      description: "Register a prospective tattoo client for a Guest.",
      submitLabel: "Create Lead",
      fields: [commonGuest, { name: "source", label: "Source", type: "text", required: true }, { name: "client_name", label: "Client name", type: "text", required: true }, { name: "client_email", label: "Client email", type: "email" }, { name: "client_phone", label: "Client phone", type: "tel" }, { name: "external_reference", label: "External reference", type: "text" }, { name: "notes", label: "Notes", type: "textarea" }],
    },
    {
      id: "appointment",
      title: "Appointment",
      description: "Create a pending-payment appointment within Artist and Studio availability.",
      submitLabel: "Create appointment",
      fields: [commonGuest, commonStudio, { name: "client_name", label: "Client name", type: "text", required: true }, { name: "client_email", label: "Client email", type: "email" }, { name: "client_phone", label: "Client phone", type: "tel" }, { name: "starts_at", label: "Starts at", type: "datetime", required: true }, { name: "ends_at", label: "Ends at", type: "datetime", required: true }, timezoneField, currencyField],
    },
    {
      id: "campaign",
      title: "Marketing campaign",
      description: "Register an approved campaign budget for a Guest.",
      submitLabel: "Create campaign",
      fields: [commonGuest, { name: "name", label: "Campaign name", type: "text", required: true }, { name: "channel", label: "Channel", type: "text", required: true }, { name: "authorized_budget", label: "Authorized budget", type: "number", required: true }, currencyField, { name: "starts_on", label: "Starts on", type: "date", required: true }, { name: "ends_on", label: "Ends on", type: "date", required: true }],
    },
    {
      id: "travel",
      title: "Travel segment",
      description: "Add a flight, train or other movement to a Guest itinerary.",
      submitLabel: "Add travel segment",
      fields: [commonGuest, { name: "segment_type", label: "Segment type", type: "select", options: [{ label: "Outbound", value: "OUTBOUND" }, { label: "Return", value: "RETURN" }, { label: "Other", value: "OTHER" }], required: true }, { name: "origin", label: "Origin", type: "text", required: true }, { name: "destination", label: "Destination", type: "text", required: true }, { name: "departs_at", label: "Departs at", type: "datetime", required: true }, { name: "arrives_at", label: "Arrives at", type: "datetime", required: true }, { ...timezoneField, name: "origin_timezone", label: "Origin timezone" }, { ...timezoneField, name: "destination_timezone", label: "Destination timezone" }, { name: "provider", label: "Provider", type: "text" }, { name: "booking_reference", label: "Booking reference", type: "text" }, { name: "cost", label: "Cost", type: "number", defaultValue: "0", required: true }, currencyField, { name: "notes", label: "Notes", type: "textarea" }],
    },
    {
      id: "accommodation",
      title: "Accommodation",
      description: "Add private lodging or an eligible Studio stay to a Guest itinerary.",
      submitLabel: "Add accommodation",
      fields: [commonGuest, { ...commonStudio, required: false }, { name: "name", label: "Accommodation name", type: "text", required: true }, { name: "address", label: "Address", type: "text", required: true }, { name: "check_in_at", label: "Check-in", type: "datetime", required: true }, { name: "check_out_at", label: "Check-out", type: "datetime", required: true }, timezoneField, { name: "booking_reference", label: "Booking reference", type: "text" }, { name: "cost", label: "Cost", type: "number", defaultValue: "0", required: true }, currencyField, { name: "notes", label: "Notes", type: "textarea" }],
    },
  ];
}
