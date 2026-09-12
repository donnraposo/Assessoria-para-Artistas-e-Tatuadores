import Link from "next/link";

import { RegisterForm } from "@/components/RegisterForm";

export default function RegisterPage() {
  return (
    <main className="login-shell">
      <section className="login-story">
        <div className="brand brand-large">
          <b>A</b>
          <span>Atria</span>
        </div>
        <div>
          <small>GUEST OPERATIONS</small>
          <h1>Join as an Artist or a Studio.</h1>
          <p>
            Create your account to submit your profile for review and start operating on
            Atria.
          </p>
        </div>
      </section>
      <section className="login-panel">
        <div className="login-card">
          <small>GET STARTED</small>
          <h2>Create your account</h2>
          <p>Choose your role and tell us who you are.</p>
          <RegisterForm />
          <p className="login-switch">
            Already have an account? <Link href="/login">Sign in</Link>
          </p>
        </div>
      </section>
    </main>
  );
}
