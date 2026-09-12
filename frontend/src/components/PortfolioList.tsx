import type { PortfolioItem } from "@/lib/types/artist";

type PortfolioListProps = { items: PortfolioItem[] };

const BYTES_IN_KILOBYTE = 1024;

export function PortfolioList({ items }: PortfolioListProps) {
  if (items.length === 0) {
    return <div className="empty-state">No portfolio images were declared.</div>;
  }
  return (
    <ul className="portfolio-list">
      {items.map((item) => (
        <li key={item.id}>
          <strong>{item.original_name}</strong>
          <small>
            {item.style || "No style"} · {Math.round(item.size_bytes / BYTES_IN_KILOBYTE)} KB
          </small>
        </li>
      ))}
    </ul>
  );
}
