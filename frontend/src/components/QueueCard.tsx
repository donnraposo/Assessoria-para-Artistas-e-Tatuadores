import Link from "next/link";

type QueueCardProps = {
  label: string;
  detail: string;
  value: number;
  href?: string;
};

export function QueueCard({ label, detail, value, href }: QueueCardProps) {
  const content = (
    <>
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{value === 0 ? "Queue is clear" : detail}</small>
    </>
  );

  if (href) {
    return <Link className="queue-card queue-link" href={href}>{content}</Link>;
  }
  return <article className="queue-card">{content}</article>;
}
