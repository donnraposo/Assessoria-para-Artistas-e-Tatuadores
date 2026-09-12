const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export type CurrentUser = {
  id: string;
  email: string;
  full_name: string;
  roles: string[];
};

export type Activity = {
  id: string;
  action: string;
  resource_type: string;
  resource_id: string;
  created_at: string;
};

export type OperationsDashboard = {
  queues: Record<string, number>;
  agency_revenue_by_currency: Array<{ currency: string; total: string }>;
  unread_notifications: number;
  recent_activity: Activity[];
};

export type RoleWorkspace = {
  role: "ARTIST" | "STUDIO";
  cards: Array<{ key: string; label: string; value: number; detail: string }>;
  balances: Array<{ currency: string; total: string }>;
};

export type OperationsQueueItem = Record<string, string | number | null>;

export type OperationsQueue = {
  count: number;
  page: number;
  pages: number;
  results: OperationsQueueItem[];
};

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    credentials: "include",
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: "Request failed." })) as Record<string, unknown>;
    const detail = typeof body.detail === "string"
      ? body.detail
      : Object.values(body).flat().map(String).join(" ");
    throw new Error(detail || "Request failed.");
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

async function csrfToken(): Promise<string> {
  const result = await requestJson<{ csrf_token: string }>("/auth/csrf/");
  return result.csrf_token;
}

async function postWithCsrf<T>(path: string, body: Record<string, unknown>): Promise<T> {
  const token = await csrfToken();
  return requestJson<T>(path, {
    method: "POST",
    headers: { "X-CSRFToken": token },
    body: JSON.stringify(body),
  });
}

async function putWithCsrf<T>(path: string, body: Record<string, unknown>): Promise<T> {
  const token = await csrfToken();
  return requestJson<T>(path, {
    method: "PUT",
    headers: { "X-CSRFToken": token },
    body: JSON.stringify(body),
  });
}

async function patchWithCsrf<T>(path: string, body: Record<string, unknown>): Promise<T> {
  const token = await csrfToken();
  return requestJson<T>(path, {
    method: "PATCH",
    headers: { "X-CSRFToken": token },
    body: JSON.stringify(body),
  });
}

async function deleteWithCsrf(path: string): Promise<void> {
  const token = await csrfToken();
  await requestJson<void>(path, {
    method: "DELETE",
    headers: { "X-CSRFToken": token },
  });
}

export type SelfServiceRole = "ARTIST" | "STUDIO";

export function register(input: {
  fullName: string;
  email: string;
  password: string;
  role: SelfServiceRole;
}): Promise<CurrentUser> {
  return postWithCsrf<CurrentUser>("/auth/register/", {
    full_name: input.fullName,
    email: input.email,
    password: input.password,
    role: input.role,
  });
}

export async function login(email: string, password: string): Promise<CurrentUser> {
  const token = await csrfToken();
  return requestJson<CurrentUser>("/auth/login/", {
    method: "POST",
    headers: { "X-CSRFToken": token },
    body: JSON.stringify({ email, password }),
  });
}

export async function logout(): Promise<void> {
  const token = await csrfToken();
  await requestJson<void>("/auth/logout/", {
    method: "POST",
    headers: { "X-CSRFToken": token },
  });
}

export function getCurrentUser(): Promise<CurrentUser> {
  return requestJson<CurrentUser>("/auth/me/");
}

export function getOperationsDashboard(): Promise<OperationsDashboard> {
  return requestJson<OperationsDashboard>("/operations/dashboard/");
}

export function getRoleWorkspace(): Promise<RoleWorkspace> {
  return requestJson<RoleWorkspace>("/operations/workspace/");
}

export function getOperationsQueue(queue: string, page: number): Promise<OperationsQueue> {
  return requestJson<OperationsQueue>(`/operations/queues/${queue}/?page=${page}&page_size=20`);
}

export function reviewArtistApplication(id: string, approved: boolean, reason: string) {
  return postWithCsrf(`/artists/applications/${id}/review/`, { approved, reason });
}

export function reviewStudio(id: string, approved: boolean, reason: string) {
  return postWithCsrf(`/studios/${id}/review/`, { approved, reason });
}

export function markGuestProposalReady(id: string) {
  return postWithCsrf(`/guests/proposals/${id}/ready/`, {});
}

export function confirmGuestProposal(id: string) {
  return postWithCsrf(`/guests/proposals/${id}/confirm/`, {});
}

export function confirmStudioBooking(id: string) {
  return postWithCsrf(`/studios/booking-requests/${id}/confirm/`, {});
}

export function decideCancellation(id: string, approved: boolean, reason: string) {
  return postWithCsrf(`/schedule/cancellation-requests/${id}/decide/`, { approved, reason });
}

export type ProposalTransitionTarget = "DECLINED" | "CANCELLED";

export function transitionGuestProposal(id: string, target: ProposalTransitionTarget, reason: string) {
  return postWithCsrf(`/guests/proposals/${id}/transition/`, { status: target, reason });
}

export function registerExternalStudioResponse(id: string, accepted: boolean, reason: string) {
  return postWithCsrf(`/studios/booking-requests/${id}/external-response/`, { accepted, reason });
}

export type LeadClosingInput = {
  appointmentId: string;
  finalValue: string;
  currency: string;
  artistMinimumApproved: boolean;
  paymentReference: string;
};

export function closeLead(id: string, input: LeadClosingInput) {
  return postWithCsrf(`/sales/leads/${id}/close/`, {
    appointment_id: input.appointmentId,
    final_value: input.finalValue,
    currency: input.currency,
    artist_minimum_approved: input.artistMinimumApproved,
    payment_reference: input.paymentReference,
    idempotency_key: crypto.randomUUID(),
  });
}

export type ArtistProfile = {
  id: string;
  professional_name: string;
  biography: string;
  years_experience: number;
  styles: string[];
  currency: string;
  minimum_tattoo_value: string;
  expected_ticket: string;
  daily_session_value: string | null;
};

export type ArtistApplication = {
  id: string;
  status: string;
  review_reason: string;
  submitted_at: string | null;
  reviewed_at: string | null;
};

export type ArtistAvailability = {
  id: string;
  starts_at: string;
  ends_at: string;
  timezone: string;
  changed_by_advisory: boolean;
  change_reason: string;
};

export type ArtistProfileInput = Omit<ArtistProfile, "id">;

export function getArtistProfile() {
  return requestJson<ArtistProfile>("/artists/me/");
}

export function updateArtistProfile(input: ArtistProfileInput) {
  return putWithCsrf<ArtistProfile>("/artists/me/", input);
}

export function getArtistApplication() {
  return requestJson<ArtistApplication>("/artists/me/application/");
}

export function submitArtistApplication() {
  return postWithCsrf<ArtistApplication>("/artists/me/application/", {});
}

export function getArtistAvailability() {
  return requestJson<ArtistAvailability[]>("/artists/me/availability/");
}

export type ArtistAvailabilityInput = Pick<ArtistAvailability, "starts_at" | "ends_at" | "timezone">;

export function createArtistAvailability(input: ArtistAvailabilityInput) {
  return postWithCsrf<ArtistAvailability>("/artists/me/availability/", input);
}

export function updateArtistAvailability(id: string, input: ArtistAvailabilityInput) {
  return patchWithCsrf<ArtistAvailability>(`/artists/me/availability/${id}/`, input);
}

export function deleteArtistAvailability(id: string) {
  return deleteWithCsrf(`/artists/me/availability/${id}/`);
}

export type StudioProfile = {
  id: string;
  name: string;
  country_code: string;
  city: string;
  address: string;
  description: string;
  amenities: string[];
  offers_accommodation: boolean;
  accommodation_details: string;
  status: string;
  review_reason: string;
};

export type StudioProfileInput = Omit<StudioProfile, "id" | "status" | "review_reason">;

export type StudioBookingRequest = {
  id: string;
  guest: string;
  studio: string;
  artist: string;
  starts_at: string;
  ends_at: string;
  timezone: string;
  status: string;
  response_reason: string;
};

export function getStudioProfile() {
  return requestJson<StudioProfile>("/studios/me/");
}

export function updateStudioProfile(input: StudioProfileInput) {
  return putWithCsrf<StudioProfile>("/studios/me/", input);
}

export function submitStudioProfile() {
  return postWithCsrf<StudioProfile>("/studios/me/submit/", {});
}

export function getStudioBookingRequests() {
  return requestJson<StudioBookingRequest[]>("/studios/me/booking-requests/");
}

export function respondToStudioBooking(id: string, accepted: boolean, reason: string) {
  return postWithCsrf<StudioBookingRequest>(`/studios/booking-requests/${id}/respond/`, {
    accepted,
    reason,
  });
}

export type Workstation = {
  id: string;
  name: string;
  is_active: boolean;
};

export type WorkstationInput = Pick<Workstation, "name">;

export function getWorkstations() {
  return requestJson<Workstation[]>("/studios/me/workstations/");
}

export function createWorkstation(input: WorkstationInput) {
  return postWithCsrf<Workstation>("/studios/me/workstations/", input);
}

export type StudioPrice = {
  id: string;
  pricing_type: string;
  amount: string;
  currency: string;
  conditions: string;
  valid_from: string;
  valid_until: string | null;
};

export type StudioPriceInput = Omit<StudioPrice, "id">;

export function getStudioPrices() {
  return requestJson<StudioPrice[]>("/studios/me/prices/");
}

export function createStudioPrice(input: StudioPriceInput) {
  return postWithCsrf<StudioPrice>("/studios/me/prices/", input);
}

export type StudioAvailabilitySlot = {
  id: string;
  workstation: string | null;
  starts_at: string;
  ends_at: string;
  capacity: number;
  timezone: string;
};

export type StudioAvailabilitySlotInput = Omit<StudioAvailabilitySlot, "id">;

export function getStudioAvailabilitySlots() {
  return requestJson<StudioAvailabilitySlot[]>("/studios/me/availability/");
}

export function createStudioAvailabilitySlot(input: StudioAvailabilitySlotInput) {
  return postWithCsrf<StudioAvailabilitySlot>("/studios/me/availability/", input);
}

export type Guest = {
  id: string;
  city: string;
  country_code: string;
  starts_on: string;
  ends_on: string;
  timezone: string;
  currency: string;
  status: string;
};

export type Appointment = {
  id: string;
  guest: string;
  studio: string;
  client_name: string;
  starts_at: string;
  ends_at: string;
  timezone: string;
  final_value: string | null;
  currency: string;
  status: string;
};

export type MyTrip = {
  guest: Pick<Guest, "id" | "city" | "country_code" | "starts_on" | "ends_on" | "timezone">;
  status: string;
  travel_segments: Array<{ id: string; origin: string; destination: string; departs_at: string; arrives_at: string; status: string }>;
  accommodations: Array<{ id: string; name: string; address: string; check_in_at: string; check_out_at: string; status: string }>;
  studios: Array<{ id: string; studio_name: string; studio_address: string; starts_at: string; ends_at: string }>;
  appointments: Array<{ id: string; studio_name: string; starts_at: string; ends_at: string; status: string }>;
  costs: { currency: string; travel: string; accommodation: string; ads: string; total: string };
};

export type PortfolioItem = {
  id: string;
  original_name: string;
  caption: string;
  style: string;
  content_type: string;
  size_bytes: number;
  position: number;
  created_at: string;
  access_url?: string;
};

export function getGuests() {
  return requestJson<Guest[]>("/guests/");
}

export function getAppointments() {
  return requestJson<Appointment[]>("/schedule/appointments/");
}

export function requestAppointmentCancellation(id: string, reason: string) {
  return postWithCsrf(`/schedule/appointments/${id}/cancellation-requests/`, { reason });
}

export function getMyTrip(guestId: string) {
  return requestJson<MyTrip>(`/logistics/guests/${guestId}/my-trip/`);
}

export async function getArtistPortfolio() {
  const items = await requestJson<PortfolioItem[]>("/artists/me/portfolio/");
  return Promise.all(items.map(async (item) => {
    const access = await requestJson<{ access_url: string }>(`/artists/me/portfolio/${item.id}/access/`);
    return { ...item, access_url: access.access_url };
  }));
}

export type PortfolioUploadInput = {
  file: File;
  caption: string;
  style: string;
  position: number;
};

export async function uploadArtistPortfolioItem(input: PortfolioUploadInput) {
  const request = await postWithCsrf<{ upload_id: string; upload_url: string }>(
    "/artists/me/portfolio/uploads/",
    {
      original_name: input.file.name,
      content_type: input.file.type,
      size_bytes: input.file.size,
      caption: input.caption,
      style: input.style,
      position: input.position,
    },
  );
  const upload = await fetch(request.upload_url, {
    method: "PUT",
    headers: { "Content-Type": input.file.type },
    body: input.file,
  });
  if (!upload.ok) throw new Error("The image could not be sent to private storage.");
  return postWithCsrf<PortfolioItem>(`/artists/me/portfolio/uploads/${request.upload_id}/confirm/`, {});
}

export function deleteArtistPortfolioItem(id: string) {
  return deleteWithCsrf(`/artists/me/portfolio/${id}/`);
}

export type OperationsReferenceData = {
  artists: Array<{ id: string; professional_name: string; currency: string }>;
  studios: Array<{ id: string; name: string; city: string; country_code: string }>;
  guests: Array<{ id: string; artist_id: string; city: string; country_code: string; currency: string; starts_on: string; ends_on: string; status: string }>;
};

export type AdvisoryRecordKind = "proposal" | "reservation" | "lead" | "appointment" | "campaign" | "travel" | "accommodation" | "guest_studio";

export function getOperationsReferenceData() {
  return requestJson<OperationsReferenceData>("/operations/reference-data/");
}

export function createAdvisoryRecord(kind: AdvisoryRecordKind, input: Record<string, unknown>) {
  const guestId = typeof input.guest === "string" ? input.guest : "";
  const paths: Record<AdvisoryRecordKind, string> = {
    proposal: "/guests/proposals/",
    reservation: "/studios/booking-requests/",
    lead: "/sales/leads/",
    appointment: "/schedule/appointments/",
    campaign: "/marketing/campaigns/",
    travel: `/logistics/guests/${guestId}/travel-segments/`,
    accommodation: `/logistics/guests/${guestId}/accommodations/`,
    guest_studio: `/guests/${guestId}/studios/`,
  };
  const body = ["travel", "accommodation", "guest_studio"].includes(kind)
    ? Object.fromEntries(Object.entries(input).filter(([key]) => key !== "guest"))
    : input;
  return postWithCsrf(paths[kind], body);
}
