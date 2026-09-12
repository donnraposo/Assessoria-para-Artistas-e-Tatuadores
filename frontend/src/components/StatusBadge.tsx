import { formatOperationalValue, statusTone, type StatusTone } from "@/lib/format";

import { Icon } from "./Icon";
import type { IconName } from "./iconName";

const toneIcons: Record<StatusTone, IconName> = {
  positive: "approved",
  danger: "declined",
  warning: "pending",
  info: "pending",
  neutral: "pending",
};

type StatusBadgeProps = {
  status: string | number | null;
};

export function StatusBadge({ status }: StatusBadgeProps) {
  const tone = statusTone(status);
  return (
    <span className={`status-badge status-${tone}`}>
      <Icon name={toneIcons[tone]} />
      {formatOperationalValue("status", status)}
    </span>
  );
}
