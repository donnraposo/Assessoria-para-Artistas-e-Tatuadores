import { formatCurrency } from "@/lib/format";
import type { CurrentUser } from "@/lib/types/identity";
import type { RoleWorkspace } from "@/lib/types/operations";

import { QueueCard } from "./QueueCard";
import { WorkspaceFrame } from "./WorkspaceFrame";

type RoleWorkspaceDashboardProps = {
  user: CurrentUser;
  workspace: RoleWorkspace;
  onSignOut: () => void;
};

export function RoleWorkspaceDashboard({ user, workspace, onSignOut }: RoleWorkspaceDashboardProps) {
  const roleName = workspace.role === "ARTIST" ? "Artist" : "Studio";

  return (
    <WorkspaceFrame
      activeHref="/"
      eyebrow={`${roleName.toUpperCase()} WORKSPACE`}
      onSignOut={onSignOut}
      roleName={roleName}
      user={user}
    >
      <section className="page-heading">
        <div><h2>Your operation</h2><p>Current information for your authorized workspace.</p></div>
        <span className="live-indicator"><i />Live</span>
      </section>
      <section className="queue-grid">
        {workspace.cards.map((card) => (
          <QueueCard detail={card.detail} key={card.key} label={card.label} value={card.value} />
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
    </WorkspaceFrame>
  );
}
