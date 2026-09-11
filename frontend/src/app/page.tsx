const metrics = [
  ["Confirmed revenue", "$42,680", "+18.4% this period"],
  ["Guest occupancy", "76%", "128 of 168 hours"],
  ["Bookings closed", "34", "21.7% conversion"],
  ["Ad spend", "$8,240", "6.2× ROAS"],
];
const sessions = [
  ["09:00", "Marina Costa", "Luna Prado", "Black Room"],
  ["14:00", "Gabriel Luz", "Noah Martins", "Atelier 27"],
  ["18:30", "Camila Rocha", "Luna Prado", "Black Room"],
];

export default function HomePage() {
  return <main className="shell">
    <aside>
      <div className="brand"><b>A</b><span>Atria</span></div>
      <small>OPERATIONS</small>
      <nav>{["Overview","Guests","Schedule","Artists","Studios","Marketing","Finance"].map((x,i)=><a className={i===0?"active":""} href="#" key={x}><i>{String(i+1).padStart(2,"0")}</i>{x}</a>)}</nav>
      <div className="profile"><b>MR</b><span><strong>Marina Reis</strong><small>Administrator</small></span></div>
    </aside>
    <section className="work">
      <header><div><small>Friday, September 11</small><h1>Good morning, Marina.</h1></div><button>＋ New Guest</button></header>
      <div className="title"><div><h2>Overview</h2><p>Track your operation in real time.</p></div><button>Last 30 days⌄</button></div>
      <section className="metrics">{metrics.map(([label,value,detail])=><article key={label}><small>{label}</small><strong>{value}</strong><p>{detail}</p></article>)}</section>
      <section className="grid">
        <article className="panel performance"><div className="panel-title"><div><h3>Period performance</h3><p>Confirmed revenue by week</p></div><strong>$42.6K</strong></div><div className="chart">{[42,55,48,72,88].map((h,i)=><div key={h}><i style={{height:`${h}%`}}/><small>Week {i+1}</small></div>)}</div></article>
        <article className="panel guest"><div className="panel-title"><div><h3>Featured Guest</h3><p>Lisbon · Sep 14–28</p></div><em>Capturing leads</em></div><div className="artist"><b>LP</b><span><strong>Luna Prado</strong><small>Fine line · Blackwork</small></span><strong>76%</strong></div><div className="progress"><i/></div><div className="stats"><span><small>Schedule</small><b>64h / 84h</b></span><span><small>Bookings</small><b>18 tattoos</b></span><span><small>Revenue</small><b>€12,480</b></span></div><button>View full operation →</button></article>
      </section>
      <section className="panel agenda"><div className="panel-title"><div><h3>Today&apos;s schedule</h3><p>3 confirmed sessions · 9 booked hours</p></div><a href="#">Open schedule →</a></div>{sessions.map(([time,client,artist,studio])=><div className="session" key={time}><time>{time}</time><i/><span><strong>{client}</strong><small>Confirmed client</small></span><span><small>Artist</small><strong>{artist}</strong></span><span><small>Studio</small><strong>{studio}</strong></span><em>Confirmed</em></div>)}</section>
    </section>
  </main>;
}
