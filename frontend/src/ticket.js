import React from 'react';
import './ticket.css';
import { Link } from 'react-router-dom'


const Ticket = () => {
  return (
    <div>
      <header>
        <h1>OurHour</h1>
        <nav>
          <ul>
            <li><Link to="/login">Instructor Portal</Link></li>
          </ul>
        </nav>
      </header>
      <main>
        <form>
          <label htmlFor="name">Course ID</label>
          <input type="text" id="name" name="name" required />
          <label htmlFor="email">Name:</label>
          <input type="email" id="email" name="email" required />
          <label htmlFor="phone">Phone:</label>
          <input type="tel" id="phone" name="phone" required />
          <label for="length">Estimated Time Required:</label>
          <select name="length" id="length">
            <option value="Short">Short</option>
            <option value="Medium">Medium</option>
            <option value="Long">Long</option>
          </select>
          <label htmlFor="message">Issue:</label>
          <textarea id="message" name="message" rows="3" required></textarea>
          <button type="submit">Submit</button>
        </form>
      </main>
    </div>
  );
};

export default Ticket;
