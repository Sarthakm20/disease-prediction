from flask import Flask, request, jsonify
from flask_cors import CORS
from services.prediction_service import PredictionService

app = Flask(__name__)
CORS(app)
service = PredictionService()

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    symptoms = data.get('symptoms', [])
    try:
        result = service.predict_disease(symptoms)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    return jsonify({"symptoms": service.get_symptoms()})

if __name__ == '__main__':
    app.run(debug=True)