import type { Activity } from "@/lib/api";
import { humanizeAction } from "@/lib/format";

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
          <time dateTime={activity.created_at}>
            {new Date(activity.created_at).toLocaleDateString("en-US", {
              month: "short",
              day: "numeric",
            })}
          </time>
        </div>
      ))}
    </div>
  );
}
