import type { Metadata } from "next";
import type { ReactNode } from "react";

import "./tokens.css";
import "./styles.css";

export const metadata: Metadata = {
  title: "Atria | Guest Operations",
  description: "Integrated management for artists, studios, guests, schedules, and results.",
};

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
