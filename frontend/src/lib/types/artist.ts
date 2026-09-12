export type ApplicationStatus = "DRAFT" | "UNDER_REVIEW" | "APPROVED" | "REJECTED";

export type ArtistProfileDraft = {
  professional_name: string;
  biography: string;
  years_experience: number;
  styles: string[];
  currency: string;
  minimum_tattoo_value: string;
  expected_ticket: string;
  daily_session_value: string | null;
};

export type ArtistProfile = ArtistProfileDraft & {
  id: string;
  created_at: string;
  updated_at: string;
};

export type ArtistApplication = {
  id: string;
  status: ApplicationStatus;
  review_reason: string;
  submitted_at: string | null;
  reviewed_at: string | null;
};

export type PortfolioItem = {
  id: string;
  object_key: string;
  original_name: string;
  content_type: string;
  size_bytes: number;
  caption: string;
  style: string;
  position: number;
  created_at: string;
};

export type ArtistApplicationDetail = ArtistApplication & {
  artist: ArtistProfile;
  contact_name: string;
  contact_email: string;
  portfolio: PortfolioItem[];
};

export type ArtistApplicationQueueItem = {
  id: string;
  artist_id: string;
  status: ApplicationStatus;
  submitted_at: string | null;
  updated_at: string;
  professional_name: string;
  years_experience: number;
  styles: string[];
};
