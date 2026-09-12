"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { getArtistAvailabilityFor, getCurrentUser, getOperationsReferenceData, logout, overrideArtistAvailability, type ArtistAvailability, type CurrentUser, type OperationsReferenceData } from "@/lib/api";

import { ArtistAvailabilityOverridePanel } from "./ArtistAvailabilityOverridePanel";
import { EmptyState } from "./EmptyState";
import { ErrorScreen } from "./ErrorScreen";
import { Icon } from "./Icon";
import { LoadingScreen } from "./LoadingScreen";
import { PageHeading } from "./PageHeading";
import { Sidebar } from "./Sidebar";
import { WorkspaceHeader } from "./WorkspaceHeader";

export function AdvisoryArtistsScreen() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [referenceData, setReferenceData] = useState<OperationsReferenceData | null>(null);
  const [selectedArtistId, setSelectedArtistId] = useState<string | null>(null);
  const [availability, setAvailability] = useState<ArtistAvailability[]>([]);
  const [detailLoading, setDetailLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    Promise.all([getCurrentUser(), getOperationsReferenceData()])
      .then(([currentUser, currentReferenceData]) => {
        if (cancelled) return;
        if (!currentUser.roles.includes("ADVISORY")) {
          router.replace("/");
          return;
        }
        setUser(currentUser);
        setReferenceData(currentReferenceData);
      })
      .catch((requestError: Error) => {
        if (cancelled) return;
        if (requestError.message.includes("credentials") || requestError.message.includes("Authentication")) {
          router.replace("/login");
          return;
        }
        setError(requestError.message);
      });
    return () => { cancelled = true; };
  }, [router]);

  if (error) return <ErrorScreen action={<Link className="quiet-action" href="/">Return to overview</Link>} message={error} title="Unable to load Artists." />;
  if (!user || !referenceData) return <LoadingScreen message="Loading Artists…" />;

  const selectArtist = async (artistId: string) => {
    setSelectedArtistId(artistId);
    setDetailLoading(true);
    setError("");
    try {
      setAvailability(await getArtistAvailabilityFor(artistId));
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to load Artist availability.");
    } finally {
      setDetailLoading(false);
    }
  };

  const selectedArtist = referenceData.artists.find((artist) => artist.id === selectedArtistId);

  return (
    <main className="shell">
      <Sidebar name={user.full_name} role="Advisory" />
      <section className="workspace">
        <WorkspaceHeader eyebrow="Advisory workbench" onSignOut={() => logout().then(() => router.replace("/login"))} title="Artists">
          <Link className="quiet-action" href="/"><Icon name="overview" /><span>Overview</span></Link>
        </WorkspaceHeader>
        <PageHeading
          description="Pick an Artist to review their availability and, exceptionally, override it with a reason."
          title={`${referenceData.artists.length} ${referenceData.artists.length === 1 ? "Artist" : "Artists"}`}
        />
        <div className="guest-grid">
          {referenceData.artists.length === 0 ? (
            <EmptyState hint="Approved Artists will appear here." icon="artist" title="No Artists yet" />
          ) : referenceData.artists.map((artist) => (
            <article className="guest-card" key={artist.id}>
              <h3>{artist.professional_name}</h3>
              <p>{artist.currency}</p>
              <button onClick={() => selectArtist(artist.id)} type="button"><Icon name="schedule" />View availability</button>
            </article>
          ))}
        </div>
        {detailLoading && <p role="status">Loading Artist availability…</p>}
        {!detailLoading && selectedArtist && (
          <>
            <PageHeading description={`Windows currently registered for ${selectedArtist.professional_name}.`} title="Availability" />
            <ArtistAvailabilityOverridePanel
              items={availability}
              onOverride={async (input) => {
                await overrideArtistAvailability(selectedArtist.id, input);
                await selectArtist(selectedArtist.id);
              }}
            />
          </>
        )}
      </section>
    </main>
  );
}
