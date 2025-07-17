from flask import Flask, request, jsonify
import sys
import os

# Add src directory to path to import predict_email
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from predict import predict_email

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get email from JSON request
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        email = request.json.get('email')
        if not email:
            return jsonify({"error": "Email text is required"}), 400
        
        if not isinstance(email, str):
            return jsonify({"error": "Email must be a string"}), 400

        # Use the updated predict_email function
        model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'phishing_detector.pkl')
        result = predict_email(model_path, email)
        
        return jsonify({
            "prediction": result,
            "email": email[:100] + "..." if len(email) > 100 else email  # Truncate long emails in response
        })
        
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
