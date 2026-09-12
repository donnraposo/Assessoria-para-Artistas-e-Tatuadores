"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { ApplicationStatusPresenter } from "@/lib/artist/ApplicationStatusPresenter";
import { ApplicationSubmissionPolicy } from "@/lib/artist/ApplicationSubmissionPolicy";
import { ProfileDraftMapper } from "@/lib/artist/ProfileDraftMapper";
import { RequestFailure } from "@/lib/http/RequestFailure";
import { ArtistService } from "@/lib/services/ArtistService";
import { IdentityService } from "@/lib/services/IdentityService";
import type { ArtistApplication, ArtistProfileDraft } from "@/lib/types/artist";
import type { CurrentUser } from "@/lib/types/identity";

import { ArtistProfileForm } from "./ArtistProfileForm";
import { StatusBadge } from "./StatusBadge";
import { WorkspaceFrame } from "./WorkspaceFrame";

export function ArtistApplicationWorkspace() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [draft, setDraft] = useState<ArtistProfileDraft | null>(null);
  const [application, setApplication] = useState<ArtistApplication | null>(null);
  const [savedRevision, setSavedRevision] = useState(0);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    IdentityService.currentUser()
      .then(async (currentUser) => {
        setUser(currentUser);
        if (!currentUser.roles.includes("ARTIST")) {
          router.replace("/");
          return;
        }
        const profile = await ArtistService.findProfile();
        setDraft(profile ? ProfileDraftMapper.fromProfile(profile) : ProfileDraftMapper.empty());
        setApplication(await ArtistService.findApplication());
      })
      .catch((requestError: unknown) => {
        if (RequestFailure.isUnauthenticated(requestError)) {
          router.replace("/login");
          return;
        }
        setError(RequestFailure.message(requestError));
      });
  }, [router]);

  async function handleSave(values: ArtistProfileDraft) {
    setSaving(true);
    setError("");
    setNotice("");
    try {
      const saved = await ArtistService.saveProfile(values);
      setDraft(ProfileDraftMapper.fromProfile(saved));
      setApplication(await ArtistService.findApplication());
      setSavedRevision((revision) => revision + 1);
      setNotice("Profile saved.");
    } catch (requestError) {
      setError(RequestFailure.message(requestError));
    } finally {
      setSaving(false);
    }
  }

  async function handleSubmitApplication() {
    setSubmitting(true);
    setError("");
    setNotice("");
    try {
      setApplication(await ArtistService.submitApplication());
      setNotice("Application sent to the Advisory team.");
    } catch (requestError) {
      setError(RequestFailure.message(requestError));
    } finally {
      setSubmitting(false);
    }
  }

  if (error && !user) {
    return (
      <main className="centered-state">
        <h1>Unable to load your application.</h1>
        <p>{error}</p>
      </main>
    );
  }
  if (!user || !draft) {
    return (
      <main className="centered-state">
        <span className="loader" />
        <p>Loading your application…</p>
      </main>
    );
  }

  const status = application?.status ?? "DRAFT";
  const blocker = ApplicationSubmissionPolicy.blocker(status, draft.styles);

  return (
    <WorkspaceFrame
      activeHref="/artist/application"
      eyebrow="ARTIST WORKSPACE"
      onSignOut={() => IdentityService.logout().then(() => router.replace("/login"))}
      roleName="Artist"
      user={user}
    >
      <section className="page-heading">
        <div>
          <h2>My application</h2>
          <p>Your professional profile and the decision of the Advisory team.</p>
        </div>
        <StatusBadge status={status} />
      </section>
      <section className="panel">
        <div className="section-heading">
          <div>
            <h3>Application state</h3>
            <p>{ApplicationStatusPresenter.guidanceText(status)}</p>
          </div>
        </div>
        {application?.review_reason && (
          <p className="review-reason">
            <strong>Advisory note:</strong> {application.review_reason}
          </p>
        )}
        {notice && <p className="form-notice" role="status">{notice}</p>}
        {error && <p className="form-error" role="alert">{error}</p>}
        <div className="form-actions">
          <button
            disabled={!ApplicationSubmissionPolicy.allows(status, draft.styles) || submitting}
            onClick={handleSubmitApplication}
            type="button"
          >
            {submitting ? "Submitting…" : "Submit application"}
          </button>
          {blocker && <small className="action-hint">{blocker}</small>}
        </div>
      </section>
      <section className="panel">
        <div className="section-heading">
          <div>
            <h3>Professional profile</h3>
            <p>Commercial parameters the Advisory team uses to plan your Guests.</p>
          </div>
        </div>
        <ArtistProfileForm draft={draft} key={savedRevision} onSave={handleSave} saving={saving} />
      </section>
    </WorkspaceFrame>
  );
}
