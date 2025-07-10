import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from joblib import dump
from collections import defaultdict

# Load dataset
df = pd.read_csv('data.csv')

# Clean and process symptoms
symptom_columns = [col for col in df.columns if col != 'Disease']
df[symptom_columns] = df[symptom_columns].fillna('')

# Create symptom string for vectorization
df['Symptoms_str'] = df[symptom_columns].apply(
    lambda row: ' '.join(symptom.strip().lower() for symptom in row if symptom.strip()), 
    axis=1
)

# Vectorize symptom strings
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['Symptoms_str'])

# Encode disease labels
le = LabelEncoder()
y = le.fit_transform(df['Disease'])

# Train model
model = RandomForestClassifier(class_weight='balanced', random_state=42)
model.fit(X, y)

# Build comprehensive symptom -> diseases map
symptom_to_diseases = defaultdict(list)

for _, row in df.iterrows():
    disease = row['Disease']
    symptoms = {symptom.strip().lower() for symptom in row[symptom_columns] if symptom.strip()}
    
    for symptom in symptoms:
        if disease not in symptom_to_diseases[symptom]:  # Avoid duplicate diseases
            symptom_to_diseases[symptom].append(disease)

# Convert to regular dict for serialization
symptom_to_diseases = dict(symptom_to_diseases)

# Get all unique symptoms (sorted)
symptom_options = sorted(symptom_to_diseases.keys())

# Save everything
dump(model, 'trained_model.pkl')
dump(vectorizer, 'vectorizer.pkl')
dump(le, 'label_encoder.pkl')
dump(symptom_to_diseases, 'symptom_to_diseases.pkl')
dump(symptom_options, 'symptom_options.pkl')

print("✅ Model and mappings saved.")