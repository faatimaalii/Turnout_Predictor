import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { CheckCircle, AlertTriangle } from 'lucide-react';
import './index.css';

const PredictForm = () => {
  const [form, setForm] = useState({
    level: 'city',
    name: '',
    year: 2029,
    voters: ''
  });

  const [locations, setLocations] = useState({ provinces: [], cities: [] });
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  // Fetch locations (cities + provinces)
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/locations')
      .then((res) => {
        setLocations(res.data);
      })
      .catch((err) => {
        console.error('Failed to load locations:', err);
      });
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);

    try {
      const payload = {
        level: form.level,
        name: form.name,
        year: parseInt(form.year),
        voters: parseInt(form.voters),
      };

      const res = await axios.post('http://127.0.0.1:8000/predict', payload);
      setResult(res.data);
    } catch (err) {
      console.error(err.response?.data || err.message);
      setError('Prediction failed. Please check your input and try again.');
    }
  };

  const availableNames = form.level === 'city' ? locations.cities : locations.provinces;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-xl mx-auto bg-white shadow-2xl rounded-2xl p-8 space-y-6 border border-gray-200 transition-all duration-300 hover:shadow-blue-200">
        <h2 className="text-2xl font-bold text-center text-blue-700">🗳️ Election Turnout Predictor</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Level Dropdown */}
          <select
            name="level"
            value={form.level}
            onChange={(e) => {
              setForm({ ...form, level: e.target.value, name: '' });
            }}
            className="w-full p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
          >
            <option value="city">City</option>
            <option value="province">Province</option>
          </select>

          {/* City/Province Dropdown */}
          <select
            name="name"
            value={form.name}
            onChange={handleChange}
            className="w-full p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
            required
          >
            <option value="">Select a {form.level}</option>
            {availableNames.map((name) => (
              <option key={name} value={name}>{name}</option>
            ))}
          </select>

          {/* Year Input */}
          <input
            type="number"
            name="year"
            placeholder="Election Year"
            value={form.year}
            onChange={handleChange}
            className="w-full p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
            required
          />

          {/* Voters Input */}
          <input
            type="number"
            name="voters"
            placeholder="Registered Voters"
            value={form.voters}
            onChange={handleChange}
            className="w-full p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
            required
          />

          {/* Submit Button */}
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
          >
            🔍 Predict Turnout
          </button>
        </form>

        {/* Error Message */}
        {error && (
          <div className="text-red-600 bg-red-100 border border-red-200 p-3 rounded-md flex items-center space-x-2">
            <AlertTriangle size={20} className="text-red-500" />
            <span>{error}</span>
          </div>
        )}

        {/* Result Display */}
        {result && (
          <div className="text-center p-5 bg-blue-50 rounded-xl border border-blue-200">
            <p className="text-xl font-semibold text-blue-800">
              📊 Predicted Turnout: <span className="text-blue-600">{result.turnout}%</span>
            </p>
            <p className={`mt-2 flex justify-center items-center text-lg font-medium ${result.high_turnout ? 'text-green-600' : 'text-red-600'}`}>
              {result.high_turnout ? (
                <>
                  <CheckCircle className="mr-1" /> High Turnout Expected
                </>
              ) : (
                <>
                  <AlertTriangle className="mr-1" /> Low Turnout Expected
                </>
              )}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default PredictForm;
