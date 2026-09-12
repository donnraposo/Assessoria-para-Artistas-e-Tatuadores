"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { getCurrentUser, getGuests, getMyTrip, logout, type CurrentUser, type Guest, type MyTrip } from "@/lib/api";

import { EmptyState } from "./EmptyState";
import { ErrorScreen } from "./ErrorScreen";
import { Icon } from "./Icon";
import { LoadingScreen } from "./LoadingScreen";
import { MyTripPanel } from "./MyTripPanel";
import { PageHeading } from "./PageHeading";
import { Sidebar } from "./Sidebar";
import { StatusBadge } from "./StatusBadge";
import { WorkspaceHeader } from "./WorkspaceHeader";

export function ArtistGuestsScreen() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [guests, setGuests] = useState<Guest[] | null>(null);
  const [trip, setTrip] = useState<MyTrip | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([getCurrentUser(), getGuests()])
      .then(([currentUser, currentGuests]) => {
        if (!currentUser.roles.includes("ARTIST")) {
          router.replace("/");
          return;
        }
        setUser(currentUser);
        setGuests(currentGuests);
      })
      .catch((requestError: Error) => setError(requestError.message));
  }, [router]);

  if (error) return <ErrorScreen message={error} title="Unable to load Guests." />;
  if (!user || !guests) return <LoadingScreen message="Loading Guests…" />;

  const loadTrip = async (guestId: string) => {
    setError("");
    try {
      setTrip(await getMyTrip(guestId));
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to load My Trip.");
    }
  };

  return (
    <main className="shell">
      <Sidebar name={user.full_name} role="Artist" />
      <section className="workspace">
        <WorkspaceHeader
          eyebrow="Artist operations"
          onSignOut={() => logout().then(() => router.replace("/login"))}
          title="Guests & My Trip"
        />
        <PageHeading
          description="Each Guest is one trip. Open My Trip to see flights, stay, Studios and schedule together."
          title={`${guests.length} ${guests.length === 1 ? "Guest" : "Guests"}`}
        />
        <div className="guest-grid">
          {guests.length === 0 ? (
            <EmptyState
              hint="The Advisory team creates a Guest when a trip is confirmed for you."
              icon="guest"
              title="No Guests assigned yet"
            />
          ) : guests.map((guest) => (
            <article className="guest-card" key={guest.id}>
              <StatusBadge status={guest.status} />
              <h3>{guest.city}, {guest.country_code}</h3>
              <p>{guest.starts_on} — {guest.ends_on}</p>
              <button onClick={() => loadTrip(guest.id)} type="button"><Icon name="trip" />View My Trip</button>
            </article>
          ))}
        </div>
        {trip && <MyTripPanel trip={trip} />}
      </section>
    </main>
  );
}
