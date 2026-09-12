import Link from "next/link";

import { LoginForm } from "@/components/LoginForm";

export default function LoginPage() {
  return (
    <main className="login-shell">
      <section className="login-story">
        <div className="brand brand-large"><b>A</b><span>Atria</span></div>
        <div><small>GUEST OPERATIONS</small><h1>Make every Guest operation feel effortless.</h1><p>Artists, Studios, schedules, sales, marketing, finance and travel—beautifully coordinated.</p></div>
      </section>
      <section className="login-panel">
        <div className="login-card">
          <small>WELCOME BACK</small><h2>Sign in to Atria</h2><p>Use your professional account to continue.</p>
          <LoginForm />
          <p className="login-switch">
            New to Atria? <Link href="/register">Create an account</Link>
          </p>
        </div>
      </section>
    </main>
  );
}
