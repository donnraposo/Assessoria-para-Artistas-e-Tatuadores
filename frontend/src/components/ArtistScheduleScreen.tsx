"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { getAppointments, getCurrentUser, logout, requestAppointmentCancellation, type Appointment, type CurrentUser } from "@/lib/api";

import { CancellationRequestControls } from "./CancellationRequestControls";
import { EmptyState } from "./EmptyState";
import { ErrorScreen } from "./ErrorScreen";
import { LoadingScreen } from "./LoadingScreen";
import { PageHeading } from "./PageHeading";
import { Sidebar } from "./Sidebar";
import { StatusBadge } from "./StatusBadge";
import { WorkspaceHeader } from "./WorkspaceHeader";

export function ArtistScheduleScreen() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [appointments, setAppointments] = useState<Appointment[] | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([getCurrentUser(), getAppointments()])
      .then(([currentUser, currentAppointments]) => {
        if (!currentUser.roles.includes("ARTIST")) {
          router.replace("/");
          return;
        }
        setUser(currentUser);
        setAppointments(currentAppointments);
      })
      .catch((requestError: Error) => setError(requestError.message));
  }, [router]);

  if (error) return <ErrorScreen message={error} title="Unable to load schedule." />;
  if (!user || !appointments) return <LoadingScreen message="Loading schedule…" />;

  return (
    <main className="shell">
      <Sidebar name={user.full_name} role="Artist" />
      <section className="workspace">
        <WorkspaceHeader
          eyebrow="Artist operations"
          onSignOut={() => logout().then(() => router.replace("/login"))}
          title="Schedule"
        />
        <PageHeading
          description="Confirmed tattoos only. To cancel one, send a request to the agency — it decides."
          title={`${appointments.length} ${appointments.length === 1 ? "appointment" : "appointments"}`}
        />
        <div className="record-list standalone-list">
          {appointments.length === 0 ? (
            <EmptyState
              hint="An appointment appears here once a client pays the 20% to the agency."
              icon="schedule"
              title="No appointments scheduled yet"
            />
          ) : appointments.map((appointment) => (
            <article className="reservation-row" key={appointment.id}>
              <div>
                <strong>{appointment.client_name}</strong>
                <span>{new Date(appointment.starts_at).toLocaleString("en-US")} — {new Date(appointment.ends_at).toLocaleString("en-US")}</span>
                <span className="row-meta"><StatusBadge status={appointment.status} /><small>{appointment.timezone}</small></span>
              </div>
              {appointment.status === "CONFIRMED" && <CancellationRequestControls clientName={appointment.client_name} onSubmit={async (reason) => {
                await requestAppointmentCancellation(appointment.id, reason);
                setAppointments((items) => items?.map((item) => item.id === appointment.id ? { ...item, status: "CANCELLATION_REQUESTED" } : item) ?? []);
              }} />}
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
