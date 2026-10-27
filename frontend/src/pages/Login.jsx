import { Link, useNavigate } from 'react-router-dom';

export default function Login() {
  const navigate = useNavigate();

  function handleSubmit(event) {
    event.preventDefault();
    navigate('/dashboard');
  }

  return (
    <section className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <p className="eyebrow">HOSTELEase</p>
        <h1>Student / Admin Login</h1>
        <p className="muted">Frontend demo for the first project phase.</p>
        <label>Email<input type="email" placeholder="Enter email" required /></label>
        <label>Password<input type="password" placeholder="Enter password" required /></label>
        <button className="primary-button full" type="submit">Login</button>
        <p className="auth-footer">New user? <Link to="/register">Create an account</Link></p>
      </form>
    </section>
  );
}
