// App.jsx
import React from "react";
import PredictForm from "./PredictForm";
import './index.css'; // or './App.css' based on where you added Tailwind directives


function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-center mb-6">🗳️ Voter Turnout Predictor</h1>
      <PredictForm />
    </div>
  );
}

export default App;
