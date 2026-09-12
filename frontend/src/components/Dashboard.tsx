"use client";

import { useRouter } from "next/navigation";
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
import { QueueCard } from "./QueueCard";
import { RoleWorkspaceDashboard } from "./RoleWorkspaceDashboard";
import { Sidebar } from "./Sidebar";

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

  if (error) {
    return <main className="centered-state"><h1>Unable to load operations.</h1><p>{error}</p></main>;
  }
  if (!user || (!dashboard && !roleWorkspace)) {
    return <main className="centered-state"><span className="loader" /><p>Loading operations…</p></main>;
  }

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
        <header className="topbar">
          <div><small>LIVE OPERATIONS</small><h1>Good to see you, {user.full_name.split(" ")[0]}.</h1></div>
          <div className="topbar-actions">
            <span className="notification-count">{dashboard.unread_notifications} unread</span>
            <button onClick={handleSignOut}>Sign out</button>
          </div>
        </header>
        <section className="page-heading">
          <div><h2>Operations overview</h2><p>Everything that needs attention, in one place.</p></div>
          <span className="live-indicator"><i />Live</span>
        </section>
        <section className="summary-grid">
          <article className="summary-card accent-card">
            <small>Items requiring attention</small><strong>{totalQueue}</strong><p>Across all operational queues</p>
          </article>
          {dashboard.agency_revenue_by_currency.length > 0 ? (
            dashboard.agency_revenue_by_currency.slice(0, 2).map((entry) => (
              <article className="summary-card" key={entry.currency}>
                <small>Confirmed agency revenue</small>
                <strong>{formatCurrency(entry.total, entry.currency)}</strong>
                <p>{entry.currency} · Recorded closings</p>
              </article>
            ))
          ) : (
            <article className="summary-card"><small>Confirmed agency revenue</small><strong>—</strong><p>No closings recorded yet</p></article>
          )}
        </section>
        <section className="section-heading"><div><h3>Action queues</h3><p>Prioritized work for the Advisory team.</p></div></section>
        <section className="queue-grid">
          {queueDefinitions.map((queue) => (
            <QueueCard
              key={queue.key}
              label={queue.label}
              detail={queue.detail}
              value={dashboard.queues[queue.key] ?? 0}
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
