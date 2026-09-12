import { ApplicationStatusPresenter } from "@/lib/artist/ApplicationStatusPresenter";
import type { ApplicationStatus } from "@/lib/types/artist";

type StatusBadgeProps = { status: ApplicationStatus };

export function StatusBadge({ status }: StatusBadgeProps) {
  return (
    <span className={`status-badge tone-${ApplicationStatusPresenter.tone(status)}`}>
      {ApplicationStatusPresenter.label(status)}
    </span>
  );
}
