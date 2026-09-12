import type { Activity } from "@/lib/types/operations";
import { formatShortDate, humanizeAction } from "@/lib/format";

type ActivityListProps = { activities: Activity[] };

export function ActivityList({ activities }: ActivityListProps) {
  if (activities.length === 0) {
    return <div className="empty-state">No operational activity yet.</div>;
  }
  return (
    <div className="activity-list">
      {activities.map((activity) => (
        <div className="activity-row" key={activity.id}>
          <i />
          <span>
            <strong>{humanizeAction(activity.action)}</strong>
            <small>{activity.resource_type}</small>
          </span>
          <time dateTime={activity.created_at}>{formatShortDate(activity.created_at)}</time>
        </div>
      ))}
    </div>
  );
}
