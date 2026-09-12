import type { ArtistProfile, ArtistProfileDraft } from "../types/artist";

export class ProfileDraftMapper {
  static empty(): ArtistProfileDraft {
    return {
      professional_name: "",
      biography: "",
      years_experience: 0,
      styles: [],
      currency: "BRL",
      minimum_tattoo_value: "",
      expected_ticket: "",
      daily_session_value: null,
    };
  }

  static fromProfile(profile: ArtistProfile): ArtistProfileDraft {
    return {
      professional_name: profile.professional_name,
      biography: profile.biography,
      years_experience: profile.years_experience,
      styles: profile.styles,
      currency: profile.currency,
      minimum_tattoo_value: profile.minimum_tattoo_value,
      expected_ticket: profile.expected_ticket,
      daily_session_value: profile.daily_session_value,
    };
  }
}
