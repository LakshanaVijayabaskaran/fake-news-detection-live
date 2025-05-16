import React, { useState } from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';
import './App.css';

const COLORS = ['#FF6B6B', '#4ECDC4']; // Fake = Red, Real = Teal

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [confidence, setConfidence] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    const prediction = data.prediction;
    setResult(prediction > 0.5 ? 'Fake News' : 'Real News');
    setConfidence(prediction);
  };

  const chartData =
    confidence !== null
      ? [
          { name: 'Fake', value: confidence },
          { name: 'Real', value: 1 - confidence },
        ]
      : [];

  return (
    <div
      style={{
        fontFamily: 'Segoe UI, sans-serif',
        backgroundColor: '#f7f9fa',
        minHeight: '100vh',
        padding: '2rem',
        textAlign: 'center',
      }}
    >
      <h1 style={{ color: '#333', marginBottom: '1.5rem' }}>
        📰 <span style={{ color: '#444' }}>Fake News Detector</span>
      </h1>
      <form onSubmit={handleSubmit}>
        <textarea
          rows={6}
          cols={70}
          style={{
            padding: '1rem',
            fontSize: '1rem',
            borderRadius: '8px',
            border: '1px solid #ccc',
            boxShadow: '0px 1px 4px rgba(0,0,0,0.1)',
            resize: 'none',
          }}
          placeholder="Paste news content here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <br />
        <button
          type="submit"
          style={{
            marginTop: '1rem',
            padding: '0.7rem 2rem',
            fontSize: '1rem',
            backgroundColor: '#4ECDC4',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
            boxShadow: '0px 2px 6px rgba(0,0,0,0.1)',
          }}
        >
          🔍 Check
        </button>
      </form>

      {result && (
        <div
          style={{
            marginTop: '2.5rem',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <h2>
            🧠 Result:{' '}
            <span style={{ color: result === 'Fake News' ? '#FF6B6B' : '#4ECDC4' }}>
              {result}
            </span>
          </h2>
          <h3 style={{ marginTop: '0.5rem', color: '#666' }}>
            Confidence: {(Math.max(confidence, 1 - confidence) * 100).toFixed(2)}%
          </h3>

          <PieChart width={300} height={300}>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={100}
              paddingAngle={3}
              dataKey="value"
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </div>
      )}
    </div>
  );
}

export default App;
