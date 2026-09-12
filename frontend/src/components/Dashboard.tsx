"use client";

import { useRouter } from "next/navigation";
import Link from "next/link";
import { useEffect, useState } from "react";

import { queueDefinitions } from "@/content/dashboard";
import {
  getCurrentUser,
  getOperationsDashboard,
  getRoleWorkspace,
  logout,
  type CurrentUser,
  type OperationsDashboard,
  type RoleWorkspace,
} from "@/lib/api";
import { formatCurrency } from "@/lib/format";

import { ActivityList } from "./ActivityList";
import { ErrorScreen } from "./ErrorScreen";
import { Icon } from "./Icon";
import { LoadingScreen } from "./LoadingScreen";
import { PageHeading } from "./PageHeading";
import { QueueCard } from "./QueueCard";
import { RoleWorkspaceDashboard } from "./RoleWorkspaceDashboard";
import { Sidebar } from "./Sidebar";
import { WorkspaceHeader } from "./WorkspaceHeader";

export function Dashboard() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [dashboard, setDashboard] = useState<OperationsDashboard | null>(null);
  const [roleWorkspace, setRoleWorkspace] = useState<RoleWorkspace | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getCurrentUser()
      .then(async (currentUser) => {
        setUser(currentUser);
        if (currentUser.roles.includes("ADVISORY")) {
          setDashboard(await getOperationsDashboard());
          return;
        }
        setRoleWorkspace(await getRoleWorkspace());
      })
      .catch((requestError: Error) => {
        if (requestError.message.includes("credentials") || requestError.message.includes("Authentication")) {
          router.replace("/login");
          return;
        }
        setError(requestError.message);
      });
  }, [router]);

  if (error) return <ErrorScreen message={error} title="Unable to load operations." />;
  if (!user || (!dashboard && !roleWorkspace)) return <LoadingScreen message="Loading operations…" />;

  const handleSignOut = () => logout().then(() => router.replace("/login"));
  if (roleWorkspace) {
    return <RoleWorkspaceDashboard user={user} workspace={roleWorkspace} onSignOut={handleSignOut} />;
  }
  if (!dashboard) return null;

  const role = user.roles[0] ?? "Advisory";
  const totalQueue = Object.values(dashboard.queues).reduce((total, value) => total + value, 0);

  return (
    <main className="shell">
      <Sidebar name={user.full_name} role={role} />
      <section className="workspace">
        <WorkspaceHeader
          eyebrow="Live operations"
          onSignOut={handleSignOut}
          title={`Good to see you, ${user.full_name.split(" ")[0]}.`}
        >
          <span className="notification-count">
            <Icon name="bell" />
            {dashboard.unread_notifications} unread
          </span>
        </WorkspaceHeader>
        <section className="dashboard-hero">
          <div className="hero-copy">
            <small>THE ART MOVES. WE MAKE IT FLOW.</small>
            <h2>Build remarkable Guest experiences.</h2>
            <p>One precise workspace for artists, Studios, bookings, travel and growth.</p>
            <div className="hero-actions">
              <Link className="primary-action" href="/operations/create">
                <Icon name="create" />
                Create operation
              </Link>
              <span><strong>{totalQueue}</strong> items need attention</span>
            </div>
          </div>
        </section>
        <PageHeading
          aside={<span className="live-indicator"><i />Live</span>}
          description="Everything that needs a decision from the Advisory team, in one place."
          eyebrow="Today"
          title="Operations overview"
        />
        <section className="summary-grid">
          <article className="summary-card accent-card">
            <span className="card-mark"><Icon name="alert" /></span>
            <small>Items requiring attention</small>
            <strong>{totalQueue}</strong>
            <p>Across all operational queues</p>
          </article>
          {dashboard.agency_revenue_by_currency.length > 0 ? (
            dashboard.agency_revenue_by_currency.slice(0, 2).map((entry) => (
              <article className="summary-card" key={entry.currency}>
                <span className="card-mark"><Icon name="revenue" /></span>
                <small>Confirmed agency revenue</small>
                <strong>{formatCurrency(entry.total, entry.currency)}</strong>
                <p>{entry.currency} · 20% received on closed sales</p>
              </article>
            ))
          ) : (
            <article className="summary-card">
              <span className="card-mark"><Icon name="revenue" /></span>
              <small>Confirmed agency revenue</small>
              <strong>—</strong>
              <p>No closings recorded yet</p>
            </article>
          )}
        </section>
        <PageHeading
          description="Each card opens the list of records waiting for you."
          eyebrow="Workflow"
          title="Action queues"
        />
        <section className="queue-grid">
          {queueDefinitions.map((queue) => (
            <QueueCard
              key={queue.key}
              label={queue.label}
              detail={queue.detail}
              hint={queue.hint}
              icon={queue.icon}
              value={dashboard.queues[queue.key] ?? 0}
              href={`/operations/${queue.slug}`}
            />
          ))}
        </section>
        <section className="activity-panel">
          <div className="section-heading"><div><h3>Recent activity</h3><p>Latest audited operational changes.</p></div></div>
          <ActivityList activities={dashboard.recent_activity} />
        </section>
      </section>
    </main>
  );
}
