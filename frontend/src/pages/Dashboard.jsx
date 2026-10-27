const cards = [
  ['Students', '0'],
  ['Total Rooms', '0'],
  ['Available Rooms', '0'],
  ['Pending Fees', '0'],
  ['Open Complaints', '0'],
  ['Visitors Today', '0'],
];

export default function Dashboard() {
  return (
    <section className="dashboard section">
      <div className="section-heading">
        <p className="eyebrow">DASHBOARD</p>
        <h1>Hostel Overview</h1>
        <p className="muted">These values will be connected to Flask + MongoDB in the backend phase.</p>
      </div>
      <div className="stats-grid">
        {cards.map(([label, value]) => (
          <article className="stat-card" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </article>
        ))}
      </div>
    </section>
  );
}
