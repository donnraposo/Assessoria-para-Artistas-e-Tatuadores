import { navigationItems } from "@/content/dashboard";

type SidebarProps = {
  name: string;
  role: string;
};

export function Sidebar({ name, role }: SidebarProps) {
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
        {navigationItems.map((item, index) => (
          <a className={index === 0 ? "active" : ""} href={item.href} key={item.href}>
            <i>{String(index + 1).padStart(2, "0")}</i>{item.label}
          </a>
        ))}
      </nav>
      <div className="profile">
        <b>{initials}</b>
        <span><strong>{name}</strong><small>{role}</small></span>
      </div>
    </aside>
  );
}
