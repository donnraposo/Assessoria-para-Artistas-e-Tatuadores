"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { deleteArtistPortfolioItem, getArtistPortfolio, getCurrentUser, logout, type CurrentUser, type PortfolioItem } from "@/lib/api";

import { EmptyState } from "./EmptyState";
import { ErrorScreen } from "./ErrorScreen";
import { Icon } from "./Icon";
import { LoadingScreen } from "./LoadingScreen";
import { PageHeading } from "./PageHeading";
import { PortfolioUploadForm } from "./PortfolioUploadForm";
import { Sidebar } from "./Sidebar";
import { WorkspaceHeader } from "./WorkspaceHeader";

export function ArtistPortfolioScreen() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [items, setItems] = useState<PortfolioItem[] | null>(null);
  const [error, setError] = useState("");

  const refreshPortfolio = async () => setItems(await getArtistPortfolio());

  useEffect(() => {
    Promise.all([getCurrentUser(), getArtistPortfolio()])
      .then(([currentUser, portfolio]) => {
        if (!currentUser.roles.includes("ARTIST")) {
          router.replace("/");
          return;
        }
        setUser(currentUser);
        setItems(portfolio);
      })
      .catch((requestError: Error) => setError(requestError.message));
  }, [router]);

  if (error) return <ErrorScreen message={error} title="Unable to load portfolio." />;
  if (!user || !items) return <LoadingScreen message="Loading portfolio…" />;

  return (
    <main className="shell">
      <Sidebar name={user.full_name} role="Artist" />
      <section className="workspace">
        <WorkspaceHeader
          eyebrow="Artist account"
          onSignOut={() => logout().then(() => router.replace("/login"))}
          title="Portfolio"
        />
        <PageHeading
          aside={<span className="live-indicator"><i />Private</span>}
          description="Only you and the Advisory team can see these images. They are used to evaluate your application."
          title={`${items.length} ${items.length === 1 ? "artwork" : "artworks"}`}
        />
        <section className="form-panel portfolio-upload-panel"><PortfolioUploadForm nextPosition={items.length} onUploaded={refreshPortfolio} /></section>
        <div className="guest-grid portfolio-grid">
          {items.length === 0 ? (
            <EmptyState
              hint="Use the form above to add your first image — JPEG, PNG or WebP up to 10 MB."
              icon="portfolio"
              title="No artwork uploaded yet"
            />
          ) : items.map((item) => <article className="guest-card portfolio-card" key={item.id}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img alt={item.caption || item.original_name} className="portfolio-image" src={item.access_url} />
            <small>{item.style || "Artwork"}</small><h3>{item.caption || item.original_name}</h3><p>{item.original_name} · {Math.round(item.size_bytes / 1024)} KB</p>
            <button className="reject-action" onClick={() => window.confirm("Remove this artwork permanently?") && deleteArtistPortfolioItem(item.id).then(refreshPortfolio)} type="button"><Icon name="trash" />Remove</button>
          </article>)}
        </div>
      </section>
    </main>
  );
}
