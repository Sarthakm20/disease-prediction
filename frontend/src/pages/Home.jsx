import React, { useState } from 'react';
import axios from 'axios';
import SymptomSelector from '../components/SymptomSelector';

const Home = () => {
  const [symptoms, setSymptoms] = useState([]);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/predict', { symptoms });
      setResults(response.data.result);
    } catch (error) {
      alert('Prediction failed: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Disease Prediction System</h1>
      
      <SymptomSelector 
        symptoms={[]}  // Will be populated from API
        onSelection={setSymptoms}
      />
      
      <button onClick={handlePredict} disabled={loading || symptoms.length === 0}>
        {loading ? 'Analyzing...' : 'Predict Disease'}
      </button>
      
      {results && (
        <div className="results">
          <h2>Prediction Results</h2>
          <p><strong>Final Diagnosis:</strong> {results.final_prediction}</p>
          <div className="individual-preds">
            {Object.entries(results.individual_predictions).map(([model, pred]) => (
              <div key={model}>
                <strong>{model}:</strong> {pred}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;