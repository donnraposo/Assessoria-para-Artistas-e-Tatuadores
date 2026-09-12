import Link from "next/link";

import type { NavigationItem } from "@/content/dashboard";

type SidebarProps = {
  name: string;
  role: string;
  items: NavigationItem[];
  activeHref: string;
};

export function Sidebar({ name, role, items, activeHref }: SidebarProps) {
  const initials = name
    .split(" ")
    .map((part) => part[0])
    .slice(0, 2)
    .join("");

  return (
    <aside className="sidebar">
      <div className="brand"><b>A</b><span>Atria</span></div>
      <small>OPERATIONS</small>
      <nav>
        {items.map((item, index) => (
          <Link
            aria-current={item.href === activeHref ? "page" : undefined}
            className={item.href === activeHref ? "active" : ""}
            href={item.href}
            key={item.href}
          >
            <i>{String(index + 1).padStart(2, "0")}</i>{item.label}
          </Link>
        ))}
      </nav>
      <div className="profile">
        <b>{initials}</b>
        <span><strong>{name}</strong><small>{role}</small></span>
      </div>
    </aside>
  );
}
