import type { ReactNode } from "react";

import { navigationFor } from "@/content/dashboard";
import type { CurrentUser } from "@/lib/types/identity";

import { Sidebar } from "./Sidebar";

type WorkspaceFrameProps = {
  user: CurrentUser;
  roleName: string;
  activeHref: string;
  eyebrow: string;
  onSignOut: () => void;
  actions?: ReactNode;
  children: ReactNode;
};

export function WorkspaceFrame({
  user,
  roleName,
  activeHref,
  eyebrow,
  onSignOut,
  actions,
  children,
}: WorkspaceFrameProps) {
  return (
    <main className="shell">
      <Sidebar
        activeHref={activeHref}
        items={navigationFor(user.roles)}
        name={user.full_name}
        role={roleName}
      />
      <section className="workspace">
        <header className="topbar">
          <div>
            <small>{eyebrow}</small>
            <h1>Good to see you, {user.full_name.split(" ")[0]}.</h1>
          </div>
          <div className="topbar-actions">
            {actions}
            <button onClick={onSignOut} type="button">Sign out</button>
          </div>
        </header>
        {children}
      </section>
    </main>
  );
}
