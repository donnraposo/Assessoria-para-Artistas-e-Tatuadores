import type { ReactNode } from "react";

type PageHeadingProps = {
  title: string;
  description?: string;
  eyebrow?: string;
  aside?: ReactNode;
};

export function PageHeading({ title, description, eyebrow, aside }: PageHeadingProps) {
  return (
    <section className="page-heading">
      <div>
        {eyebrow && <small className="eyebrow">{eyebrow}</small>}
        <h2>{title}</h2>
        {description && <p>{description}</p>}
      </div>
      {aside}
    </section>
  );
}
