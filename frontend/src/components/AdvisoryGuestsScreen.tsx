"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { confirmFinancialEntry, getCurrentUser, getGuestFinanceSummary, getGuestStudioBookings, getOperationsReferenceData, logout, updateStudioBookingPaymentStatus, type CurrentUser, type GuestFinanceSummary, type OperationsReferenceData, type StudioBooking } from "@/lib/api";

import { EmptyState } from "./EmptyState";
import { ErrorScreen } from "./ErrorScreen";
import { GuestFinancePanel } from "./GuestFinancePanel";
import { Icon } from "./Icon";
import { LoadingScreen } from "./LoadingScreen";
import { PageHeading } from "./PageHeading";
import { Sidebar } from "./Sidebar";
import { StatusBadge } from "./StatusBadge";
import { StudioBookingPaymentPanel } from "./StudioBookingPaymentPanel";
import { WorkspaceHeader } from "./WorkspaceHeader";

export function AdvisoryGuestsScreen() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [referenceData, setReferenceData] = useState<OperationsReferenceData | null>(null);
  const [selectedGuestId, setSelectedGuestId] = useState<string | null>(null);
  const [finance, setFinance] = useState<GuestFinanceSummary | null>(null);
  const [bookings, setBookings] = useState<StudioBooking[]>([]);
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

  if (error) return <ErrorScreen action={<Link className="quiet-action" href="/">Return to overview</Link>} message={error} title="Unable to load Guests." />;
  if (!user || !referenceData) return <LoadingScreen message="Loading Guests…" />;

  const selectGuest = async (guestId: string) => {
    setSelectedGuestId(guestId);
    setDetailLoading(true);
    setError("");
    try {
      const [currentFinance, currentBookings] = await Promise.all([
        getGuestFinanceSummary(guestId),
        getGuestStudioBookings(guestId),
      ]);
      setFinance(currentFinance);
      setBookings(currentBookings);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to load Guest detail.");
    } finally {
      setDetailLoading(false);
    }
  };

  const refreshDetail = () => {
    if (selectedGuestId) selectGuest(selectedGuestId);
  };

  return (
    <main className="shell">
      <Sidebar name={user.full_name} role="Advisory" />
      <section className="workspace">
        <WorkspaceHeader eyebrow="Advisory workbench" onSignOut={() => logout().then(() => router.replace("/login"))} title="Guests">
          <Link className="quiet-action" href="/"><Icon name="overview" /><span>Overview</span></Link>
        </WorkspaceHeader>
        <PageHeading
          description="Pick a Guest to review its financial balance and Studio booking payments."
          title={`${referenceData.guests.length} ${referenceData.guests.length === 1 ? "Guest" : "Guests"}`}
        />
        <div className="guest-grid">
          {referenceData.guests.length === 0 ? (
            <EmptyState hint="Guests appear here once a Proposal is confirmed." icon="guest" title="No Guests yet" />
          ) : referenceData.guests.map((guest) => (
            <article className="guest-card" key={guest.id}>
              <StatusBadge status={guest.status} />
              <h3>{guest.city}, {guest.country_code}</h3>
              <p>{guest.starts_on} — {guest.ends_on}</p>
              <button onClick={() => selectGuest(guest.id)} type="button"><Icon name="revenue" />View finance</button>
            </article>
          ))}
        </div>
        {detailLoading && <p role="status">Loading Guest detail…</p>}
        {!detailLoading && finance && (
          <>
            <GuestFinancePanel
              onConfirmEntry={async (entryId, reference) => {
                await confirmFinancialEntry(entryId, reference);
                refreshDetail();
              }}
              summary={finance}
            />
            <PageHeading description="Confirm a Studio booking as paid once the transfer is settled." title="Studio bookings" />
            <StudioBookingPaymentPanel
              items={bookings}
              onMarkAsPaid={async (bookingId) => {
                await updateStudioBookingPaymentStatus(bookingId, "PAID");
                refreshDetail();
              }}
            />
          </>
        )}
      </section>
    </main>
  );
}
