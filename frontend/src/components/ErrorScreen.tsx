import type { ReactNode } from "react";

import { Icon } from "./Icon";

type ErrorScreenProps = {
  title: string;
  message: string;
  action?: ReactNode;
};

export function ErrorScreen({ title, message, action }: ErrorScreenProps) {
  return (
    <main className="centered-state">
      <span className="state-mark state-mark-danger"><Icon name="alert" /></span>
      <h1>{title}</h1>
      <p role="alert">{message}</p>
      {action}
    </main>
  );
}
