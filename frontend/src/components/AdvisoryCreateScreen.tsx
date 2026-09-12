"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";

import { buildAdvisoryForms } from "@/content/operationsForms";
import { createAdvisoryRecord, getCurrentUser, getOperationsReferenceData, logout, type CurrentUser, type OperationsReferenceData } from "@/lib/api";

import { AdvisoryRecordForm } from "./AdvisoryRecordForm";
import { ErrorScreen } from "./ErrorScreen";
import { Icon } from "./Icon";
import { LoadingScreen } from "./LoadingScreen";
import { PageHeading } from "./PageHeading";
import { Sidebar } from "./Sidebar";
import { WorkspaceHeader } from "./WorkspaceHeader";

export function AdvisoryCreateScreen() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [referenceData, setReferenceData] = useState<OperationsReferenceData | null>(null);
  const [error, setError] = useState("");
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC";
  const definitions = useMemo(
    () => referenceData ? buildAdvisoryForms(referenceData, timezone) : [],
    [referenceData, timezone],
  );

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

  if (error) return <ErrorScreen action={<Link className="quiet-action" href="/">Return to overview</Link>} message={error} title="Unable to load creation tools." />;
  if (!user || !referenceData) return <LoadingScreen message="Loading creation tools…" />;

  return (
    <main className="shell">
      <Sidebar name={user.full_name} role="Advisory" />
      <section className="workspace">
        <WorkspaceHeader
          eyebrow="Advisory workbench"
          onSignOut={() => logout().then(() => router.replace("/login"))}
          title="Create operational records"
        >
          <Link className="quiet-action" href="/"><Icon name="overview" /><span>Overview</span></Link>
        </WorkspaceHeader>
        <PageHeading
          aside={<span className="live-indicator"><i />Secure</span>}
          description="Open a card to create the record. Follow the order of the Guest journey: proposal, reservation, lead, appointment."
          eyebrow="Workbench"
          title="Build the next operation"
        />
        <section className="creation-grid">
          {definitions.map((definition) => (
            <AdvisoryRecordForm
              definition={definition}
              key={definition.id}
              onSubmit={(payload) => createAdvisoryRecord(definition.id, payload).then(() => undefined)}
            />
          ))}
        </section>
      </section>
    </main>
  );
}
