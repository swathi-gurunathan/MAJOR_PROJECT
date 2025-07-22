import React, { useState } from 'react';
import axios from 'axios';

function FlightBooking() {
  const [formData, setFormData] = useState({
    from: '',
    to: '',
    departureDate: '',
    returnDate: '',
    passengers: 1,
  });

  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  // Handles form input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  // Function to call backend API on button click
  const handleSubmit = () => {
    // Clear previous response/error
    setResponse(null);
    setError(null);

    axios.post('http://localhost:9000/api/flight-book', formData)
      .then(res => {
        console.log("Backend response:", res.data);
        setResponse(res.data);
      })
      .catch(error => {
        if (error.response) {
          // Backend returned an error response (non 2xx)
          console.error('Response error:', error.response.data);
          setError(`Server responded with error: ${JSON.stringify(error.response.data)}`);
        } else if (error.request) {
          // Request was made but no response received
          console.error('No response received:', error.request);
          setError('No response received from server.');
        } else {
          // Other errors setting up request
          console.error('Error setting up request:', error.message);
          setError(`Request error: ${error.message}`);
        }
      });
  };

  return (
    <div style={{ maxWidth: 400, margin: 'auto', padding: 20 }}>
      <h2>Flight Booking</h2>

      <label>From:</label>
      <input 
        type="text" 
        name="from" 
        value={formData.from} 
        onChange={handleChange} 
        placeholder="Departure city"
        style={{ width: '100%', marginBottom: 10 }}
      />

      <label>To:</label>
      <input 
        type="text" 
        name="to" 
        value={formData.to} 
        onChange={handleChange} 
        placeholder="Destination city"
        style={{ width: '100%', marginBottom: 10 }}
      />

      <label>Departure Date:</label>
      <input 
        type="date" 
        name="departureDate" 
        value={formData.departureDate} 
        onChange={handleChange} 
        style={{ width: '100%', marginBottom: 10 }}
      />

      <label>Return Date (optional):</label>
      <input 
        type="date" 
        name="returnDate" 
        value={formData.returnDate} 
        onChange={handleChange} 
        style={{ width: '100%', marginBottom: 10 }}
      />

      <label>Passengers:</label>
      <input 
        type="number" 
        name="passengers" 
        min="1" 
        value={formData.passengers} 
        onChange={handleChange} 
        style={{ width: '100%', marginBottom: 15 }}
      />

      <button onClick={handleSubmit} style={{ width: '100%', padding: 10, fontSize: 16 }}>
        Book Flight
      </button>

      {response && (
        <div style={{ marginTop: 20, padding: 10, backgroundColor: '#e0ffe0' }}>
          <h3>Booking Successful:</h3>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}

      {error && (
        <div style={{ marginTop: 20, padding: 10, backgroundColor: '#ffe0e0', color: 'red' }}>
          <h3>Error:</h3>
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}

export default FlightBooking;
