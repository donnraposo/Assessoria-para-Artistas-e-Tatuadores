"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";

import { getNavigationItems } from "@/content/dashboard";

import { Icon } from "./Icon";

type SidebarProps = {
  name: string;
  role: string;
};

function buildInitials(name: string): string {
  return name
    .split(" ")
    .map((part) => part[0])
    .slice(0, 2)
    .join("")
    .toUpperCase();
}

export function Sidebar({ name, role }: SidebarProps) {
  const pathname = usePathname();
  const navigationItems = getNavigationItems(role);

  return (
    <aside className="sidebar">
      <div className="brand"><b>A</b><span>Atria</span></div>
      <small className="sidebar-caption">{role.toUpperCase()} WORKSPACE</small>
      <nav aria-label="Main navigation">
        {navigationItems.map((item) => {
          const current = pathname === item.href;
          return (
            <Link
              aria-current={current ? "page" : undefined}
              className={current ? "nav-item active" : "nav-item"}
              data-tooltip={item.label}
              href={item.href}
              key={item.href}
            >
              <Icon name={item.icon} />
              <span className="nav-label">{item.label}</span>
              <span aria-hidden="true" className="nav-label-short">{item.short}</span>
            </Link>
          );
        })}
      </nav>
      <div className="profile">
        <b>{buildInitials(name)}</b>
        <span><strong>{name}</strong><small>{role}</small></span>
      </div>
    </aside>
  );
}
