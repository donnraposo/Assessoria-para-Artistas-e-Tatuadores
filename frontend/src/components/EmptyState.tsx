import type { ReactNode } from "react";

import { Icon } from "./Icon";
import type { IconName } from "./iconName";

type EmptyStateProps = {
  title: string;
  hint?: string;
  icon?: IconName;
  action?: ReactNode;
};

export function EmptyState({ title, hint, icon = "empty", action }: EmptyStateProps) {
  return (
    <div className="empty-state">
      <span className="empty-state-mark"><Icon name={icon} /></span>
      <strong>{title}</strong>
      {hint && <p>{hint}</p>}
      {action}
    </div>
  );
}
