"use client";

import { useState, type FormEvent } from "react";

import { uploadArtistPortfolioItem } from "@/lib/api";

import { Icon } from "./Icon";

type PortfolioUploadFormProps = {
  nextPosition: number;
  onUploaded: () => Promise<void>;
};

const allowedTypes = ["image/jpeg", "image/png", "image/webp"];
const maximumSize = 10 * 1024 * 1024;

export function PortfolioUploadForm({ nextPosition, onUploaded }: PortfolioUploadFormProps) {
  const [file, setFile] = useState<File | null>(null);
  const [caption, setCaption] = useState("");
  const [style, setStyle] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = event.currentTarget;
    if (!file || !allowedTypes.includes(file.type) || file.size > maximumSize) {
      setError("Choose a JPEG, PNG or WebP image up to 10 MB.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      await uploadArtistPortfolioItem({ file, caption, style, position: nextPosition });
      setFile(null);
      setCaption("");
      setStyle("");
      form.reset();
      await onUploaded();
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to upload image.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="data-form portfolio-upload-form" onSubmit={handleSubmit}>
      <div className="section-heading"><div><small className="eyebrow">PRIVATE STORAGE</small><h3>Add artwork</h3><p>JPEG, PNG or WebP · Maximum 10 MB</p></div></div>
      <div className="form-grid">
        <label className="form-span">Artwork image<input accept="image/jpeg,image/png,image/webp" onChange={(event) => setFile(event.target.files?.[0] ?? null)} required type="file" /></label>
        <label>Caption<input maxLength={300} onChange={(event) => setCaption(event.target.value)} value={caption} /></label>
        <label>Style<input maxLength={80} onChange={(event) => setStyle(event.target.value)} value={style} /></label>
      </div>
      {error && <p className="form-error" role="alert">{error}</p>}
      <button disabled={loading || !file} type="submit"><Icon name="upload" />{loading ? "Uploading…" : "Upload artwork"}</button>
    </form>
  );
}
