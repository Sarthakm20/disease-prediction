from flask import Flask, render_template, request
from joblib import load
from collections import Counter, defaultdict

app = Flask(__name__)

# Load model and tools
model = load('trained_model.pkl')
vectorizer = load('vectorizer.pkl')
le = load('label_encoder.pkl')
symptom_to_diseases = load('symptom_to_diseases.pkl')
symptom_options = load('symptom_options.pkl')

@app.route('/')
def home():
    return render_template('index.html', symptoms=symptom_options)

@app.route('/predict', methods=['POST'])
def predict():
    selected_symptoms = [s.strip().lower() for s in request.form.getlist('symptoms')]
    
    if not selected_symptoms:
        return "Please select at least one symptom."

    # Single symptom case
    if len(selected_symptoms) == 1:
        symptom = selected_symptoms[0]
        possible_diseases = symptom_to_diseases.get(symptom, [])
        
        if not possible_diseases:
            return render_template('result.html', 
                               diseases=[], 
                               single=True,
                               selected_symptoms=selected_symptoms)

        # Calculate percentages
        disease_counts = Counter(possible_diseases)
        total = len(possible_diseases)
        percentages = {
            disease: f"{(count / total) * 100:.1f}%"
            for disease, count in disease_counts.items()
        }

        return render_template(
            'result.html',
            diseases=list(disease_counts.keys()),
            percentages=percentages,
            single=True,
            selected_symptoms=selected_symptoms,
            symptom_to_diseases=symptom_to_diseases  # Pass the mapping
        )

    # Multiple symptoms case
    disease_scores = defaultdict(int)
    symptom_matches = defaultdict(list)  # Track which symptoms matched each disease
    
    # Score diseases based on symptom matches
    for symptom in selected_symptoms:
        for disease in symptom_to_diseases.get(symptom, []):
            disease_scores[disease] += 1
            symptom_matches[disease].append(symptom)
    
    if not disease_scores:
        return render_template('result.html', 
                           show_prediction=False, 
                           single=False, 
                           selected_symptoms=selected_symptoms)

    # Sort diseases by match score
    sorted_diseases = sorted(disease_scores.items(), key=lambda x: (-x[1], x[0]))
    max_score = sorted_diseases[0][1]
    
    # Get top matches and other possible diseases
    top_diseases = [d for d, score in sorted_diseases if score == max_score]
    other_diseases = [d for d, score in sorted_diseases if 0 < score < max_score][:5]  # Top 5 others
    
    # Calculate match percentage
    match_percentage = (max_score / len(selected_symptoms)) * 100
    
    return render_template(
        'result.html',
        predicted_disease=top_diseases[0],
        match_count=max_score,
        match_percentage=f"{match_percentage:.1f}%",
        total_symptoms=len(selected_symptoms),
        common_diseases=other_diseases,
        show_prediction=True,
        single=False,
        selected_symptoms=selected_symptoms,
        all_matching_diseases=top_diseases,
        symptom_to_diseases=symptom_to_diseases,  # Pass the mapping
        symptom_matches=symptom_matches  # Pass symptom matches for each disease
    )

if __name__ == '__main__':
    app.run(debug=True)