import React, { useState } from "react";
import './App.css';

function App() {
  const [form, setForm] = useState({
    name: "",
    age: "",
    source: "",
    destination: "",
    date: "",
    train_number: "",
  });

  const [message, setMessage] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Basic validation
    if (
      !form.name || !form.age || !form.source ||
      !form.destination || !form.date || !form.train_number
    ) {
      setMessage("Please fill in all fields.");
      return;
    }

    try {
      const res = await fetch("http://localhost:9000/book-ticket", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ...form,
          age: Number(form.age), // Convert age to number
        }),
      });

      const data = await res.json();

      if (res.ok) {
        setMessage(`Success! Your ticket ID is ${data.ticket_id}`);
      } else {
        setMessage(`Failed: ${data.detail || "Unknown error"}`);
      }
    } catch (error) {
      setMessage("Error connecting to server.");
    }
  };

  return (
    <div className="container">
      <h2>Train Ticket Booking</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label><br />
          <input name="name" value={form.name} onChange={handleChange} />
        </div>
        <div>
          <label>Age:</label><br />
          <input name="age" type="number" value={form.age} onChange={handleChange} />
        </div>
        <div>
          <label>Source:</label><br />
          <input name="source" value={form.source} onChange={handleChange} />
        </div>
        <div>
          <label>Destination:</label><br />
          <input name="destination" value={form.destination} onChange={handleChange} />
        </div>
        <div>
          <label>Travel Date:</label><br />
          <input name="date" type="date" value={form.date} onChange={handleChange} />
        </div>
        <div>
          <label>Train Number:</label><br />
          <input name="train_number" value={form.train_number} onChange={handleChange} />
        </div>
        <br />
        <button type="submit">Book Ticket</button>
      </form>

      {message && (
        <p className={`message ${message.startsWith("Success") ? "success" : "error"}`}>
          {message}
        </p>
      )}
    </div>
  );
}

export default App;
