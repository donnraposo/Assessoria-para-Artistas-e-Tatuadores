import type { CurrentUser, RoleWorkspace } from "@/lib/api";
import { formatCurrency } from "@/lib/format";

import { QueueCard } from "./QueueCard";
import { Sidebar } from "./Sidebar";

type RoleWorkspaceDashboardProps = {
  user: CurrentUser;
  workspace: RoleWorkspace;
  onSignOut: () => void;
};

export function RoleWorkspaceDashboard({ user, workspace, onSignOut }: RoleWorkspaceDashboardProps) {
  const roleName = workspace.role === "ARTIST" ? "Artist" : "Studio";
  return (
    <main className="shell">
      <Sidebar name={user.full_name} role={roleName} />
      <section className="workspace">
        <header className="topbar">
          <div><small>{roleName.toUpperCase()} WORKSPACE</small><h1>Good to see you, {user.full_name.split(" ")[0]}.</h1></div>
          <button onClick={onSignOut}>Sign out</button>
        </header>
        <section className="page-heading">
          <div><h2>Your operation</h2><p>Current information for your authorized workspace.</p></div>
          <span className="live-indicator"><i />Live</span>
        </section>
        <section className="queue-grid">
          {workspace.cards.map((card) => (
            <QueueCard
              key={card.key}
              label={card.label}
              value={card.value}
              detail={card.detail}
            />
          ))}
        </section>
        {workspace.balances.length > 0 && (
          <section>
            <div className="section-heading"><div><h3>Expected Artist balance</h3><p>Amounts expected from confirmed closings.</p></div></div>
            <div className="summary-grid">
              {workspace.balances.map((balance) => (
                <article className="summary-card" key={balance.currency}>
                  <small>{balance.currency}</small>
                  <strong>{formatCurrency(balance.total, balance.currency)}</strong>
                  <p>Expected external payment</p>
                </article>
              ))}
            </div>
          </section>
        )}
      </section>
    </main>
  );
}
