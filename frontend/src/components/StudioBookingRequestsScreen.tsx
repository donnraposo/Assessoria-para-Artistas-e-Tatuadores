"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { getCurrentUser, getStudioBookingRequests, logout, respondToStudioBooking, type CurrentUser, type StudioBookingRequest } from "@/lib/api";

import { EmptyState } from "./EmptyState";
import { ErrorScreen } from "./ErrorScreen";
import { LoadingScreen } from "./LoadingScreen";
import { PageHeading } from "./PageHeading";
import { QueueActionControls } from "./QueueActionControls";
import { Sidebar } from "./Sidebar";
import { StatusBadge } from "./StatusBadge";
import { WorkspaceHeader } from "./WorkspaceHeader";

const responseActions = [
  { id: "approve", label: "Accept", tone: "approve", statuses: ["REQUESTED"] },
  { id: "reject", label: "Decline", tone: "reject", statuses: ["REQUESTED"], requiresReason: true },
] as const;

export function StudioBookingRequestsScreen() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [requests, setRequests] = useState<StudioBookingRequest[] | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([getCurrentUser(), getStudioBookingRequests()])
      .then(([currentUser, currentRequests]) => {
        if (!currentUser.roles.includes("STUDIO")) {
          router.replace("/");
          return;
        }
        setUser(currentUser);
        setRequests(currentRequests);
      })
      .catch((requestError: Error) => setError(requestError.message));
  }, [router]);

  if (error) return <ErrorScreen message={error} title="Unable to load reservation requests." />;
  if (!user || !requests) return <LoadingScreen message="Loading reservations…" />;

  return (
    <main className="shell">
      <Sidebar name={user.full_name} role="Studio" />
      <section className="workspace">
        <WorkspaceHeader
          eyebrow="Studio operations"
          onSignOut={() => logout().then(() => router.replace("/login"))}
          title="Reservation requests"
        />
        <PageHeading
          description="Accept or decline the dates the agency wants to book at your Studio."
          title={`${requests.length} ${requests.length === 1 ? "request" : "requests"}`}
        />
        <div className="record-list standalone-list">
          {requests.length === 0 ? (
            <EmptyState
              hint="Requests appear here when the Advisory team plans a trip that needs your space."
              icon="reservation"
              title="No reservation requests yet"
            />
          ) : requests.map((request) => {
            const actions = responseActions.filter((action) => action.statuses.includes(request.status as "REQUESTED"));
            return <article className="reservation-row" key={request.id}>
              <div>
                <strong>{new Date(request.starts_at).toLocaleString("en-US")}</strong>
                <span>Until {new Date(request.ends_at).toLocaleString("en-US")}</span>
                <span className="row-meta"><StatusBadge status={request.status} /></span>
              </div>
              {actions.length > 0 && <QueueActionControls actions={actions} itemLabel={`reservation ${request.id}`} onAction={async (action, reason) => {
                const updated = await respondToStudioBooking(request.id, action === "approve", reason);
                setRequests((items) => items?.map((item) => item.id === updated.id ? updated : item) ?? []);
              }} />}
            </article>;
          })}
        </div>
      </section>
    </main>
  );
}
