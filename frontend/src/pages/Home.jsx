import { Link } from 'react-router-dom';

const services = [
  ['Room Management', 'Track room availability and allocation.'],
  ['Student Management', 'Maintain organized student records.'],
  ['Fee Management', 'Track paid and pending hostel fees.'],
  ['Complaint Management', 'Register and track student complaints.'],
  ['Visitor Records', 'Maintain visitor entry and exit records.'],
  ['Admin Dashboard', 'View important hostel information in one place.'],
];

export default function Home() {
  return (
    <div>
      <section className="hero">
        <div>
          <p className="eyebrow">SMART HOSTEL MANAGEMENT</p>
          <h1>Manage your hostel from one simple platform.</h1>
          <p className="hero-text">
            HostelEase is a web-based system for students and administrators to manage
            rooms, fees, complaints, visitors and hostel records efficiently.
          </p>
          <div className="actions">
            <Link className="primary-button" to="/login">Get Started</Link>
            <a className="secondary-button" href="#services">Explore Services</a>
          </div>
        </div>
        <div className="hero-card">
          <h2>HostelEase</h2>
          <p>Smart Hostel Management System</p>
          <div className="mini-stat"><strong>Students</strong><span>Management</span></div>
          <div className="mini-stat"><strong>Rooms</strong><span>Allocation</span></div>
          <div className="mini-stat"><strong>Fees</strong><span>Tracking</span></div>
          <div className="mini-stat"><strong>Complaints</strong><span>Status</span></div>
        </div>
      </section>

      <section id="services" className="section">
        <div className="section-heading">
          <p className="eyebrow">CORE MODULES</p>
          <h2>Everything in one place</h2>
        </div>
        <div className="service-grid">
          {services.map(([title, text]) => (
            <article className="service-card" key={title}>
              <h3>{title}</h3>
              <p>{text}</p>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
