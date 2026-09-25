"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { createStudioAvailabilitySlot, createStudioPrice, createWorkstation, getCurrentUser, getStudioAvailabilitySlots, getStudioPrices, getStudioProfile, getWorkstations, logout, submitStudioProfile, updateStudioProfile, type CurrentUser, type StudioAvailabilitySlot, type StudioPrice, type StudioProfile, type StudioProfileInput, type Workstation } from "@/lib/api";

import { ErrorScreen } from "./ErrorScreen";
import { LoadingScreen } from "./LoadingScreen";
import { PageHeading } from "./PageHeading";
import { Sidebar } from "./Sidebar";
import { StatusBadge } from "./StatusBadge";
import { StudioAvailabilityPanel } from "./StudioAvailabilityPanel";
import { StudioPricePanel } from "./StudioPricePanel";
import { StudioProfileForm } from "./StudioProfileForm";
import { WorkspaceHeader } from "./WorkspaceHeader";
import { WorkstationPanel } from "./WorkstationPanel";

export function StudioAccountScreen() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [profile, setProfile] = useState<StudioProfile | null>(null);
  const [workstations, setWorkstations] = useState<Workstation[]>([]);
  const [prices, setPrices] = useState<StudioPrice[]>([]);
  const [availability, setAvailability] = useState<StudioAvailabilitySlot[]>([]);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    Promise.all([getCurrentUser(), getStudioProfile(), getWorkstations(), getStudioPrices(), getStudioAvailabilitySlots()])
      .then(([currentUser, currentProfile, currentWorkstations, currentPrices, currentAvailability]) => {
        if (!currentUser.roles.includes("STUDIO")) {
          router.replace("/");
          return;
        }
        setUser(currentUser);
        setProfile(currentProfile);
        setWorkstations(currentWorkstations);
        setPrices(currentPrices);
        setAvailability(currentAvailability);
      })
      .catch((requestError: Error) => setError(requestError.message));
  }, [router]);

  if (error) return <ErrorScreen message={error} title="Unable to load Studio profile." />;
  if (!user || !profile) return <LoadingScreen message="Loading Studio profile…" />;

  const submitForReview = async () => {
    if (!window.confirm("Submit this Studio for Advisory review?")) return;
    setSubmitting(true);
    try {
      setProfile(await submitStudioProfile());
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to submit Studio.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="shell">
      <Sidebar name={user.full_name} role="Studio" />
      <section className="workspace">
        <WorkspaceHeader
          eyebrow="Studio account"
          onSignOut={() => logout().then(() => router.replace("/login"))}
          title="Studio profile"
        />
        <PageHeading
          aside={<StatusBadge status={profile.status} />}
          description="Only approved Studios appear to the Advisory team when they plan a trip."
          title="Operational profile"
        />
        <section className="form-panel"><StudioProfileForm profile={profile} onSave={async (input: StudioProfileInput) => setProfile(await updateStudioProfile(input))} /></section>
        <section className="application-callout"><div><h3>Studio application</h3><p>{profile.review_reason || "Submit the completed Studio profile so the Advisory team can review it."}</p></div><button disabled={profile.status !== "DRAFT" || submitting} onClick={submitForReview} type="button">{submitting ? "Submitting…" : "Submit for review"}</button></section>
        <PageHeading
          description="Register the benches or chairs the agency can reserve for Guests."
          title="Workstations"
        />
        <WorkstationPanel
          items={workstations}
          onCreate={async (input) => {
            const created = await createWorkstation(input);
            setWorkstations((items) => [...items, created]);
          }}
        />
        <PageHeading
          description="Register how the Studio charges the agency for hosting a Guest."
          title="Pricing"
        />
        <StudioPricePanel
          items={prices}
          onCreate={async (input) => {
            const created = await createStudioPrice(input);
            setPrices((items) => [...items, created]);
          }}
        />
        <PageHeading
          description="Add the periods the Studio can host Guests. The agency only books inside these windows."
          title="Availability"
        />
        <StudioAvailabilityPanel
          items={availability}
          workstations={workstations}
          onCreate={async (input) => {
            const created = await createStudioAvailabilitySlot(input);
            setAvailability((items) => [...items, created]);
          }}
        />
      </section>
    </main>
  );
}
