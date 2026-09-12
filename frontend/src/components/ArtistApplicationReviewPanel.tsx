"use client";

import { useState } from "react";

import { formatCurrency, formatLongDate } from "@/lib/format";
import type { ArtistApplicationDetail } from "@/lib/types/artist";

import { PortfolioList } from "./PortfolioList";
import { StatusBadge } from "./StatusBadge";

type ArtistApplicationReviewPanelProps = {
  application: ArtistApplicationDetail;
  deciding: boolean;
  onDecide: (approved: boolean, reason: string) => void;
};

export function ArtistApplicationReviewPanel({
  application,
  deciding,
  onDecide,
}: ArtistApplicationReviewPanelProps) {
  const [reason, setReason] = useState("");
  const [reasonError, setReasonError] = useState("");
  const artist = application.artist;

  function handleDecision(approved: boolean) {
    if (!approved && reason.trim().length === 0) {
      setReasonError("A rejection requires a reason recorded for the audit trail.");
      return;
    }
    setReasonError("");
    onDecide(approved, reason.trim());
  }

  return (
    <div className="review-panel">
      <div className="section-heading">
        <div>
          <h3>{artist.professional_name}</h3>
          <p>{application.contact_name} · {application.contact_email}</p>
        </div>
        <StatusBadge status={application.status} />
      </div>
      <dl className="detail-grid">
        <div>
          <dt>Experience</dt>
          <dd>{artist.years_experience} years</dd>
        </div>
        <div>
          <dt>Styles</dt>
          <dd>{artist.styles.length > 0 ? artist.styles.join(", ") : "Not declared"}</dd>
        </div>
        <div>
          <dt>Minimum tattoo value</dt>
          <dd>{formatCurrency(artist.minimum_tattoo_value, artist.currency)}</dd>
        </div>
        <div>
          <dt>Expected ticket</dt>
          <dd>{formatCurrency(artist.expected_ticket, artist.currency)}</dd>
        </div>
        <div>
          <dt>Daily session value</dt>
          <dd>
            {artist.daily_session_value
              ? formatCurrency(artist.daily_session_value, artist.currency)
              : "Not declared"}
          </dd>
        </div>
        <div>
          <dt>Submitted</dt>
          <dd>{application.submitted_at ? formatLongDate(application.submitted_at) : "—"}</dd>
        </div>
      </dl>
      {artist.biography && <p className="detail-biography">{artist.biography}</p>}
      <div className="section-heading">
        <div>
          <h3>Portfolio</h3>
          <p>Images declared by the Artist for this application.</p>
        </div>
      </div>
      <PortfolioList items={application.portfolio} />
      {application.status === "UNDER_REVIEW" ? (
        <div className="decision-block">
          <p className="field field-wide">
            <label htmlFor="review_reason">Decision reason</label>
            <textarea
              id="review_reason"
              onChange={(event) => setReason(event.target.value)}
              rows={3}
              value={reason}
            />
            <small>Required to reject. Recorded in the audit trail either way.</small>
          </p>
          {reasonError && <p className="form-error" role="alert">{reasonError}</p>}
          <div className="form-actions">
            <button disabled={deciding} onClick={() => handleDecision(true)} type="button">
              {deciding ? "Recording…" : "Approve"}
            </button>
            <button
              className="danger-button"
              disabled={deciding}
              onClick={() => handleDecision(false)}
              type="button"
            >
              Reject
            </button>
          </div>
        </div>
      ) : (
        <p className="review-reason">
          <strong>Decision:</strong> {application.review_reason || "No reason recorded."}
        </p>
      )}
    </div>
  );
}
