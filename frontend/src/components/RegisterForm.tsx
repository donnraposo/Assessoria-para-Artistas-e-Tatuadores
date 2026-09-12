"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";

import { register, type SelfServiceRole } from "@/lib/api";

export function RegisterForm() {
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<SelfServiceRole>("ARTIST");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      await register(fullName, email, password, role);
      router.replace("/");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Registration failed.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="login-form" onSubmit={handleSubmit}>
      <span className="role-picker">
        <label className={role === "ARTIST" ? "role-option active" : "role-option"}>
          <input
            checked={role === "ARTIST"}
            name="role"
            onChange={() => setRole("ARTIST")}
            type="radio"
            value="ARTIST"
          />
          Artist
        </label>
        <label className={role === "STUDIO" ? "role-option active" : "role-option"}>
          <input
            checked={role === "STUDIO"}
            name="role"
            onChange={() => setRole("STUDIO")}
            type="radio"
            value="STUDIO"
          />
          Studio
        </label>
      </span>
      <label htmlFor="full_name">Full name</label>
      <input
        autoComplete="name"
        id="full_name"
        onChange={(event) => setFullName(event.target.value)}
        required
        type="text"
        value={fullName}
      />
      <label htmlFor="email">Email</label>
      <input
        autoComplete="email"
        id="email"
        onChange={(event) => setEmail(event.target.value)}
        required
        type="email"
        value={email}
      />
      <label htmlFor="password">Password</label>
      <input
        autoComplete="new-password"
        id="password"
        minLength={8}
        onChange={(event) => setPassword(event.target.value)}
        required
        type="password"
        value={password}
      />
      {error && (
        <p className="form-error" role="alert">
          {error}
        </p>
      )}
      <button disabled={submitting} type="submit">
        {submitting ? "Creating account…" : "Create account"}
      </button>
    </form>
  );
}
