from statistics import mode
from sklearn.exceptions import NotFittedError

def validate_symptoms(input_symptoms, valid_symptoms):
    if not isinstance(input_symptoms, list):
        raise ValueError("Symptoms must be a list")
    
    invalid = [s for s in input_symptoms if s not in valid_symptoms]
    if invalid:
        raise ValueError(f"Invalid symptoms: {', '.join(invalid)}")
    
    return list(set(input_symptoms))  # Remove duplicates