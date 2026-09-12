import type { LeadClosingInput, OperationsQueueItem } from "@/lib/api";
import { formatOperationalValue, humanizeField } from "@/lib/format";
import type { QueueActionDefinition, QueueActionId } from "@/content/dashboard";

import { EmptyState } from "./EmptyState";
import { QueueActionControls } from "./QueueActionControls";
import { LeadClosingControls } from "./LeadClosingControls";
import { StatusBadge } from "./StatusBadge";

type OperationsQueueTableProps = {
  columns: readonly string[];
  items: OperationsQueueItem[];
  actions: readonly QueueActionDefinition[];
  onAction: (id: string, action: QueueActionId, reason: string) => Promise<void>;
  onCloseLead?: (id: string, input: LeadClosingInput) => Promise<void>;
};

export function OperationsQueueTable({ columns, items, actions, onAction, onCloseLead }: OperationsQueueTableProps) {
  if (items.length === 0) {
    return (
      <EmptyState
        hint="Nothing here needs your decision right now. New records appear automatically."
        icon="approved"
        title="This queue is clear"
      />
    );
  }
  const hasActions = actions.length > 0 || Boolean(onCloseLead);
  return (
    <div className="table-scroll">
      <table className="operations-table">
        <thead><tr>{columns.map((column) => <th key={column}>{humanizeField(column)}</th>)}{hasActions && <th>Action</th>}</tr></thead>
        <tbody>
          {items.map((item) => {
            const availableActions = actions.filter((action) => action.statuses.includes(String(item.status)));
            return <tr key={String(item.id)}>
              {columns.map((column) => (
                <td key={column} data-label={humanizeField(column)}>
                  {column === "status"
                    ? <StatusBadge status={item[column]} />
                    : formatOperationalValue(column, item[column])}
                </td>
              ))}
              {hasActions && (
                <td data-label="Action">
                  {onCloseLead ? (
                    <LeadClosingControls
                      appointmentId={String(item.appointment_id ?? "")}
                      clientName={String(item.client_name ?? "Lead")}
                      onClose={(input) => onCloseLead(String(item.id), input)}
                    />
                  ) : availableActions.length > 0 ? (
                    <QueueActionControls
                      actions={availableActions}
                      itemLabel={String(item.name ?? item.client_name ?? item.artist_id ?? item.id)}
                      onAction={(action, reason) => onAction(String(item.id), action, reason)}
                    />
                  ) : <span className="muted-label">Waiting on another party</span>}
                </td>
              )}
            </tr>;
          })}
        </tbody>
      </table>
    </div>
  );
}
