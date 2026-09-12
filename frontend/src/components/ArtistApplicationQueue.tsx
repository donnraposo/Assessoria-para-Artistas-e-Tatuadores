"use client";

import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

import { RequestFailure } from "@/lib/http/RequestFailure";
import { ArtistService } from "@/lib/services/ArtistService";
import { IdentityService } from "@/lib/services/IdentityService";
import { OperationsService } from "@/lib/services/OperationsService";
import type { ArtistApplicationDetail, ArtistApplicationQueueItem } from "@/lib/types/artist";
import type { CurrentUser } from "@/lib/types/identity";

import { ArtistApplicationReviewPanel } from "./ArtistApplicationReviewPanel";
import { QueuePagination } from "./QueuePagination";
import { WorkspaceFrame } from "./WorkspaceFrame";

export function ArtistApplicationQueue() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [items, setItems] = useState<ArtistApplicationQueueItem[] | null>(null);
  const [pages, setPages] = useState(1);
  const [page, setPage] = useState(1);
  const [selected, setSelected] = useState<ArtistApplicationDetail | null>(null);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [deciding, setDeciding] = useState(false);

  const loadQueue = useCallback(async (pageNumber: number) => {
    const queue = await OperationsService.artistApplicationQueue(pageNumber);
    setItems(queue.results);
    setPages(queue.pages);
    setPage(queue.page);
  }, []);

  useEffect(() => {
    IdentityService.currentUser()
      .then(async (currentUser) => {
        setUser(currentUser);
        if (!currentUser.roles.includes("ADVISORY")) {
          router.replace("/");
          return;
        }
        await loadQueue(1);
      })
      .catch((requestError: unknown) => {
        if (RequestFailure.isUnauthenticated(requestError)) {
          router.replace("/login");
          return;
        }
        setError(RequestFailure.message(requestError));
      });
  }, [loadQueue, router]);

  async function openApplication(applicationId: string) {
    setError("");
    setNotice("");
    try {
      setSelected(await ArtistService.applicationDetail(applicationId));
    } catch (requestError) {
      setError(RequestFailure.message(requestError));
    }
  }

  async function decide(approved: boolean, reason: string) {
    if (!selected) return;
    setDeciding(true);
    setError("");
    try {
      const reviewed = await ArtistService.reviewApplication(selected.id, approved, reason);
      setSelected(reviewed);
      setNotice(`${reviewed.artist.professional_name} was ${approved ? "approved" : "rejected"}.`);
      await loadQueue(page);
    } catch (requestError) {
      setError(RequestFailure.message(requestError));
    } finally {
      setDeciding(false);
    }
  }

  async function changePage(nextPage: number) {
    setError("");
    try {
      await loadQueue(nextPage);
      setSelected(null);
    } catch (requestError) {
      setError(RequestFailure.message(requestError));
    }
  }

  if (error && !user) {
    return (
      <main className="centered-state">
        <h1>Unable to load the queue.</h1>
        <p>{error}</p>
      </main>
    );
  }
  if (!user || !items) {
    return (
      <main className="centered-state">
        <span className="loader" />
        <p>Loading artist applications…</p>
      </main>
    );
  }

  return (
    <WorkspaceFrame
      activeHref="/queues/artist-applications"
      eyebrow="ADVISORY QUEUE"
      onSignOut={() => IdentityService.logout().then(() => router.replace("/login"))}
      roleName="Advisory"
      user={user}
    >
      <section className="page-heading">
        <div>
          <h2>Artist applications</h2>
          <p>Applications submitted by Artists and waiting for a decision.</p>
        </div>
        <span className="notification-count">{items.length} on this page</span>
      </section>
      {notice && <p className="form-notice" role="status">{notice}</p>}
      {error && <p className="form-error" role="alert">{error}</p>}
      <section className="queue-layout">
        <div className="panel">
          {items.length === 0 ? (
            <div className="empty-state">No application is waiting for review.</div>
          ) : (
            <ul className="record-list">
              {items.map((item) => (
                <li key={item.id}>
                  <button
                    className={selected?.id === item.id ? "record-row selected" : "record-row"}
                    onClick={() => openApplication(item.id)}
                    type="button"
                  >
                    <span>
                      <strong>{item.professional_name}</strong>
                      <small>
                        {item.styles.length > 0 ? item.styles.join(", ") : "No style declared"}
                      </small>
                    </span>
                    <small>{item.years_experience} yrs</small>
                  </button>
                </li>
              ))}
            </ul>
          )}
          <QueuePagination onChange={changePage} page={page} pages={pages} />
        </div>
        <div className="panel">
          {selected ? (
            <ArtistApplicationReviewPanel
              application={selected}
              deciding={deciding}
              key={selected.id}
              onDecide={decide}
            />
          ) : (
            <div className="empty-state">Select an application to review it.</div>
          )}
        </div>
      </section>
    </WorkspaceFrame>
  );
}
