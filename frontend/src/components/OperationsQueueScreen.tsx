"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { queueDefinitions, type QueueActionId } from "@/content/dashboard";
import { closeLead, confirmGuestProposal, confirmStudioBooking, decideCancellation, getCurrentUser, getOperationsQueue, logout, markGuestProposalReady, reviewArtistApplication, reviewStudio, type CurrentUser, type LeadClosingInput, type OperationsQueue } from "@/lib/api";

import { ErrorScreen } from "./ErrorScreen";
import { Icon } from "./Icon";
import { LoadingScreen } from "./LoadingScreen";
import { OperationsQueueTable } from "./OperationsQueueTable";
import { PageHeading } from "./PageHeading";
import { Sidebar } from "./Sidebar";
import { WorkspaceHeader } from "./WorkspaceHeader";

type OperationsQueueScreenProps = { queueSlug: string };

export function OperationsQueueScreen({ queueSlug }: OperationsQueueScreenProps) {
  const router = useRouter();
  const definition = queueDefinitions.find((queue) => queue.slug === queueSlug);
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [queue, setQueue] = useState<OperationsQueue | null>(null);
  const [page, setPage] = useState(1);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [revision, setRevision] = useState(0);

  useEffect(() => {
    if (!definition) return;
    let cancelled = false;
    Promise.all([getCurrentUser(), getOperationsQueue(queueSlug, page)])
      .then(([currentUser, currentQueue]) => {
        if (cancelled) return;
        if (!currentUser.roles.includes("ADVISORY")) {
          router.replace("/");
          return;
        }
        setUser(currentUser);
        setQueue(currentQueue);
        setLoading(false);
      })
      .catch((requestError: Error) => {
        if (cancelled) return;
        if (requestError.message.includes("credentials") || requestError.message.includes("Authentication")) {
          router.replace("/login");
          return;
        }
        setError(requestError.message);
        setLoading(false);
      });
    return () => { cancelled = true; };
  }, [definition, page, queueSlug, revision, router]);

  const handleAction = async (id: string, action: QueueActionId, reason: string) => {
    if (action === "approve" || action === "reject") {
      const review = definition?.slug === "artist-applications" ? reviewArtistApplication : reviewStudio;
      await review(id, action === "approve", reason);
    } else if (action === "mark-ready") {
      await markGuestProposalReady(id);
    } else if (action === "confirm-guest") {
      await confirmGuestProposal(id);
    } else if (action === "confirm-booking") {
      await confirmStudioBooking(id);
    } else {
      await decideCancellation(id, action === "approve-cancellation", reason);
    }
    setLoading(true);
    setRevision((value) => value + 1);
  };

  const handleCloseLead = async (id: string, input: LeadClosingInput) => {
    await closeLead(id, input);
    setLoading(true);
    setRevision((value) => value + 1);
  };

  const backToOverview = <Link className="quiet-action" href="/">Return to overview</Link>;
  if (!definition) return <ErrorScreen action={backToOverview} message="This address does not match any operational queue." title="Queue not found." />;
  if (error) return <ErrorScreen action={backToOverview} message={error} title="Unable to load queue." />;
  if (loading || !user || !queue) return <LoadingScreen message="Loading queue…" />;

  return (
    <main className="shell">
      <Sidebar name={user.full_name} role="Advisory" />
      <section className="workspace">
        <WorkspaceHeader
          eyebrow="Advisory queue"
          onSignOut={() => logout().then(() => router.replace("/login"))}
          title={definition.label}
        >
          <Link className="quiet-action" href="/"><Icon name="overview" /><span>Overview</span></Link>
        </WorkspaceHeader>
        <PageHeading
          aside={<span className="live-indicator"><i />Live</span>}
          description={definition.hint}
          title={`${queue.count} ${queue.count === 1 ? "item" : "items"}`}
        />
        <section className="table-panel">
          <OperationsQueueTable actions={definition.actions} columns={definition.columns} items={queue.results} onAction={handleAction} onCloseLead={definition.slug === "open-leads" ? handleCloseLead : undefined} />
          {queue.pages > 1 && (
            <nav className="pagination" aria-label="Queue pages">
              <button disabled={page === 1} onClick={() => { setLoading(true); setPage((value) => value - 1); }} type="button">Previous</button>
              <span>Page {queue.page} of {queue.pages}</span>
              <button disabled={page === queue.pages} onClick={() => { setLoading(true); setPage((value) => value + 1); }} type="button">Next</button>
            </nav>
          )}
        </section>
      </section>
    </main>
  );
}
