"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { createArtistAvailability, getArtistApplication, getArtistAvailability, getArtistProfile, getCurrentUser, logout, submitArtistApplication, updateArtistProfile, type ArtistApplication, type ArtistAvailability, type ArtistProfile, type ArtistProfileInput, type CurrentUser } from "@/lib/api";

import { ArtistAvailabilityPanel } from "./ArtistAvailabilityPanel";
import { ArtistProfileForm } from "./ArtistProfileForm";
import { ErrorScreen } from "./ErrorScreen";
import { LoadingScreen } from "./LoadingScreen";
import { PageHeading } from "./PageHeading";
import { Sidebar } from "./Sidebar";
import { StatusBadge } from "./StatusBadge";
import { WorkspaceHeader } from "./WorkspaceHeader";

export function ArtistAccountScreen() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [profile, setProfile] = useState<ArtistProfile | null>(null);
  const [application, setApplication] = useState<ArtistApplication | null>(null);
  const [availability, setAvailability] = useState<ArtistAvailability[]>([]);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    Promise.all([getCurrentUser(), getArtistProfile(), getArtistApplication(), getArtistAvailability()])
      .then(([currentUser, currentProfile, currentApplication, currentAvailability]) => {
        if (!currentUser.roles.includes("ARTIST")) {
          router.replace("/");
          return;
        }
        setUser(currentUser);
        setProfile(currentProfile);
        setApplication(currentApplication);
        setAvailability(currentAvailability);
      })
      .catch((requestError: Error) => setError(requestError.message));
  }, [router]);

  if (error) return <ErrorScreen message={error} title="Unable to load Artist profile." />;
  if (!user || !profile || !application) return <LoadingScreen message="Loading Artist profile…" />;

  const submitApplication = async () => {
    if (!window.confirm("Submit this Artist application for Advisory review?")) return;
    setSubmitting(true);
    try {
      setApplication(await submitArtistApplication());
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to submit application.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="shell">
      <Sidebar name={user.full_name} role="Artist" />
      <section className="workspace">
        <WorkspaceHeader
          eyebrow="Artist account"
          onSignOut={() => logout().then(() => router.replace("/login"))}
          title="Profile & availability"
        />
        <PageHeading
          aside={<StatusBadge status={application.status} />}
          description="These values define how the agency negotiates on your behalf. Keep them accurate."
          title="Professional profile"
        />
        <section className="form-panel"><ArtistProfileForm profile={profile} onSave={async (input: ArtistProfileInput) => setProfile(await updateArtistProfile(input))} /></section>
        <section className="application-callout"><div><h3>Artist application</h3><p>{application.review_reason || "Submit your completed profile so the Advisory team can review it."}</p></div><button disabled={application.status !== "DRAFT" || submitting} onClick={submitApplication} type="button">{submitting ? "Submitting…" : "Submit for review"}</button></section>
        <PageHeading
          description="Add the periods you are free to tattoo. The agency only books inside these windows."
          title="Availability"
        />
        <ArtistAvailabilityPanel
          items={availability}
          onCreate={async (input) => {
            const created = await createArtistAvailability(input);
            setAvailability((items) => [...items, created]);
          }}
        />
      </section>
    </main>
  );
}
