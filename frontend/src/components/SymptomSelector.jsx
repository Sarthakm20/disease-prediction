import React, { useState } from 'react';

const SymptomSelector = ({ symptoms, onSelection }) => {
  const [selected, setSelected] = useState([]);

  const toggleSymptom = (symptom) => {
    const newSelected = selected.includes(symptom)
      ? selected.filter(s => s !== symptom)
      : [...selected, symptom];
    
    setSelected(newSelected);
    onSelection(newSelected);
  };

  return (
    <div className="symptom-grid">
      {symptoms.map(symptom => (
        <div 
          key={symptom} 
          className={`symptom-card ${selected.includes(symptom) ? 'selected' : ''}`}
          onClick={() => toggleSymptom(symptom)}
        >
          {symptom}
        </div>
      ))}
    </div>
  );
};

export default SymptomSelector;