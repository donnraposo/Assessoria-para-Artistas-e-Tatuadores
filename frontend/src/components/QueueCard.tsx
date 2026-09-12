import Link from "next/link";

import { Icon } from "./Icon";
import type { IconName } from "./iconName";

type QueueCardProps = {
  label: string;
  detail: string;
  value: number;
  href?: string;
  hint?: string;
  icon?: IconName;
};

export function QueueCard({ label, detail, value, href, hint, icon = "overview" }: QueueCardProps) {
  const cleared = value === 0;
  const content = (
    <>
      <span className="card-mark"><Icon name={icon} /></span>
      <span className="card-title">{label}</span>
      <strong>{value}</strong>
      <small className={cleared ? "tone-clear" : "tone-active"}>{cleared ? "Nothing pending" : detail}</small>
      {hint && <p className="card-hint">{hint}</p>}
      {href && <span aria-hidden="true" className="card-go"><Icon name="arrow" /></span>}
    </>
  );
  if (href) return <Link className="queue-card queue-card-link" href={href}>{content}</Link>;
  return <article className="queue-card">{content}</article>;
}
