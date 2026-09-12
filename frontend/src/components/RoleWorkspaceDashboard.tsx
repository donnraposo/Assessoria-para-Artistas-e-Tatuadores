import type { CurrentUser, RoleWorkspace } from "@/lib/api";
import { workspaceCardHint } from "@/content/workspaceCardHint";
import { workspaceCardIcon } from "@/content/workspaceCardIcon";
import { formatCurrency } from "@/lib/format";
import Link from "next/link";

import { Icon } from "./Icon";
import { PageHeading } from "./PageHeading";
import { QueueCard } from "./QueueCard";
import { Sidebar } from "./Sidebar";
import { WorkspaceHeader } from "./WorkspaceHeader";

type RoleWorkspaceDashboardProps = {
  user: CurrentUser;
  workspace: RoleWorkspace;
  onSignOut: () => void;
};

export function RoleWorkspaceDashboard({ user, workspace, onSignOut }: RoleWorkspaceDashboardProps) {
  const isArtist = workspace.role === "ARTIST";
  const roleName = isArtist ? "Artist" : "Studio";
  const profileHref = isArtist ? "/artist/profile" : "/studio/profile";
  const headline = isArtist ? "Your craft, ready for the world." : "The right space for remarkable work.";
  const summary = isArtist
    ? "Track your trips, schedule and payouts while the agency handles the rest."
    : "Answer booking requests and keep your Studio details current.";

  return (
    <main className="shell">
      <Sidebar name={user.full_name} role={roleName} />
      <section className="workspace">
        <WorkspaceHeader
          eyebrow={`${roleName} workspace`}
          onSignOut={onSignOut}
          title={`Good to see you, ${user.full_name.split(" ")[0]}.`}
        />
        <section className="dashboard-hero">
          <div className="hero-copy">
            <small>{roleName.toUpperCase()} EDITION</small>
            <h2>{headline}</h2>
            <p>{summary}</p>
            <div className="hero-actions">
              <Link className="primary-action" href={profileHref}>
                <Icon name={isArtist ? "artist" : "studio"} />
                Manage profile
              </Link>
            </div>
          </div>
        </section>
        <PageHeading
          aside={<span className="live-indicator"><i />Live</span>}
          description="A snapshot of what is happening in your operation right now."
          eyebrow="Workspace"
          title="Your operation"
        />
        <section className="queue-grid">
          {workspace.cards.map((card) => (
            <QueueCard
              key={card.key}
              label={card.label}
              value={card.value}
              detail={card.detail}
              hint={workspaceCardHint(card.key)}
              icon={workspaceCardIcon(card.key)}
            />
          ))}
        </section>
        {workspace.balances.length > 0 && (
          <section>
            <PageHeading
              description="Your 80% share of every closed sale, paid to you outside the platform."
              eyebrow="Finance"
              title="Expected Artist balance"
            />
            <div className="summary-grid">
              {workspace.balances.map((balance) => (
                <article className="summary-card" key={balance.currency}>
                  <span className="card-mark"><Icon name="revenue" /></span>
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
