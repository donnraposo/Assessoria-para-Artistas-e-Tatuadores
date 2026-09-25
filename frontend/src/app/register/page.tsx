import Link from "next/link";

import { RegisterForm } from "@/components/RegisterForm";

export default function RegisterPage() {
  return (
    <main className="login-shell">
      <section className="login-story">
        <div className="brand brand-large"><b>A</b><span>Atria</span></div>
        <div className="login-story-copy">
          <small>JOIN THE STUDIO</small>
          <h1>Bring your craft to Atria.</h1>
          <p>Create your professional account and let us handle scheduling, guests and growth around your work.</p>
        </div>
        <span className="story-edition">ATRIA / PROFESSIONAL EDITION</span>
      </section>
      <section className="login-panel">
        <div className="login-card">
          <small>NEW ACCOUNT</small>
          <h2>Create your account.</h2>
          <p>Register as an Artist or a Studio.</p>
          <RegisterForm />
          <p className="login-switch">Already have an account? <Link href="/login">Sign in</Link></p>
        </div>
      </section>
    </main>
  );
}
