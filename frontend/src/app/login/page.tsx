import { LoginForm } from "@/components/LoginForm";

export default function LoginPage() {
  return (
    <main className="login-shell">
      <section className="login-story">
        <div className="brand brand-large"><b>A</b><span>Atria</span></div>
        <div className="login-story-copy"><small>THE ART MOVES. WE MAKE IT FLOW.</small><h1>Where artists meet the world.</h1><p>Guests, Studios, schedules, growth and travel—beautifully orchestrated around the craft.</p></div>
        <span className="story-edition">ATRIA / PROFESSIONAL EDITION</span>
      </section>
      <section className="login-panel">
        <div className="login-card">
          <small>PRIVATE WORKSPACE</small><h2>Welcome back.</h2><p>Sign in with your professional account.</p>
          <LoginForm />
        </div>
      </section>
    </main>
  );
}
