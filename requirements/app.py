from flask import Flask, request, jsonify
import sys
import os

# Add the src directory to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
src_dir = os.path.join(project_root, "src")
sys.path.append(src_dir)

from predict import predict_email

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    email = request.json.get('email')
    if not email:
        return jsonify({"error": "Email text is required"}), 400

    # Get absolute paths
    model_file = os.path.join(project_root, "models", "phishing_detector.pkl")
    vectorizer_file = os.path.join(project_root, "data", "preprocessed_data.pkl")
    
    result = predict_email(model_file, vectorizer_file, email)
    return jsonify({"prediction": result})

if __name__ == "__main__":
    app.run(debug=True)
