"use client";

import type { ReactNode } from "react";

import { Icon } from "./Icon";

type WorkspaceHeaderProps = {
  eyebrow: string;
  title: string;
  onSignOut: () => void;
  children?: ReactNode;
};

export function WorkspaceHeader({ eyebrow, title, onSignOut, children }: WorkspaceHeaderProps) {
  return (
    <header className="topbar">
      <div className="topbar-identity">
        <small>{eyebrow}</small>
        <h1>{title}</h1>
      </div>
      <div className="topbar-actions">
        {children}
        <button className="ghost-button" onClick={onSignOut} type="button">
          <Icon name="signout" />
          <span>Sign out</span>
        </button>
      </div>
    </header>
  );
}
