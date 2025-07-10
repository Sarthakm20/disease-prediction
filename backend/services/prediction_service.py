import joblib
import numpy as np
import pandas as pd
from utils.validator import validate_symptoms

class PredictionService:
    def __init__(self):
        self.data = pd.read_csv('data/processed/cleaned_data.csv')
        self.symptoms = self.data.columns.tolist()
        self.encoder = joblib.load('models/label_encoder.pkl')
        self.models = {
            'rf': joblib.load('models/random_forest.pkl'),
            'svm': joblib.load('models/svm.pkl'),
            'xgb': joblib.load('models/xgboost.pkl')
        }
        
    def get_symptoms(self):
        return self.symptoms
    
    def _prepare_input(self, symptoms):
        validated = validate_symptoms(symptoms, self.symptoms)
        input_data = np.zeros(len(self.symptoms))
        for symptom in validated:
            idx = self.symptoms.index(symptom)
            input_data[idx] = 1
        return input_data.reshape(1, -1)
    
    def predict_disease(self, symptoms):
        X = self._prepare_input(symptoms)
        predictions = {}
        
        for name, model in self.models.items():
            pred = self.encoder.inverse_transform([model.predict(X)[0]])[0]
            predictions[name] = pred
            
        final_pred = mode([pred for pred in predictions.values()])
        
        return {
            "individual_predictions": predictions,
            "final_prediction": final_pred,
            "confidence": self._calculate_confidence(X)
        }
    
    def _calculate_confidence(self, X):
        probs = []
        for model in self.models.values():
            if hasattr(model, 'predict_proba'):
                probs.append(model.predict_proba(X)[0])
        return float(np.mean(probs)) if probs else 0.85