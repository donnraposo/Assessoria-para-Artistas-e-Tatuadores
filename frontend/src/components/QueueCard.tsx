type QueueCardProps = {
  label: string;
  detail: string;
  value: number;
};

export function QueueCard({ label, detail, value }: QueueCardProps) {
  return (
    <article className="queue-card">
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{value === 0 ? "Queue is clear" : detail}</small>
    </article>
  );
}

