
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

export default function Register() {
  const navigate = useNavigate();
  const [message, setMessage] = useState('');

  async function handleSubmit(event) {
    event.preventDefault();
    setMessage('Registering...');

    const form = new FormData(event.currentTarget);

    const user = {
      name: form.get('name'),
      email: form.get('email'),
      password: form.get('password'),
      phone: form.get('phone'),
      studentId: form.get('studentId'),
      roomNumber: form.get('roomNumber')
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user)
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.message || 'Registration failed.');
        return;
      }

      setMessage('Registration successful! Redirecting to login...');
      setTimeout(() => navigate('/login'), 1000);
    } catch (error) {
      setMessage('Backend se connection nahi ho raha. Check karo Flask running hai ya nahi.');
    }
  }

  return (
    <section className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <p className="eyebrow">HOSTELEase</p>
        <h1>Create Account</h1>

        <label>Full Name
          <input name="name" type="text" placeholder="Enter full name" required />
        </label>

        <label>Email
          <input name="email" type="email" placeholder="Enter email" required />
        </label>

        <label>Phone
          <input name="phone" type="tel" placeholder="Enter phone number" required />
        </label>

        <label>Student ID
          <input name="studentId" type="text" placeholder="Enter student ID" required />
        </label>

        <label>Room Number
          <input name="roomNumber" type="text" placeholder="Enter room number" required />
        </label>

        <label>Password
          <input name="password" type="password" placeholder="Create password" minLength="6" required />
        </label>

        <button className="primary-button full" type="submit">
          Register
        </button>

        {message && <p role="status">{message}</p>}

        <p className="auth-footer">
          Already registered? <Link to="/login">Login</Link>
        </p>
      </form>
    </section>
  );
}
