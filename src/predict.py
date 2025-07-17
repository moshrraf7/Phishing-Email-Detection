import pickle
import os
import sys

def predict_email(model_file, email_text):
    # Validate input parameters
    if not email_text or not isinstance(email_text, str):
        raise ValueError("Email text must be a non-empty string")
    
    if not os.path.exists(model_file):
        raise FileNotFoundError(f"Model file not found: {model_file}")
    
    try:
        # Load the model and vectorizer
        with open(model_file, "rb") as f:
            data = pickle.load(f)
            
            # Handle both old and new format for backwards compatibility
            if isinstance(data, dict):
                # New format: dictionary with 'model' and 'vectorizer' keys
                if 'model' not in data or 'vectorizer' not in data:
                    raise ValueError("Invalid model file format")
                model = data['model']
                vectorizer = data['vectorizer']
            else:
                # Old format: just the model (fallback)
                model = data
                # Try to load vectorizer from separate file
                vectorizer_file = "data/preprocessed_data.pkl"
                if not os.path.exists(vectorizer_file):
                    raise FileNotFoundError("Vectorizer file not found and model file doesn't contain vectorizer")
                
                with open(vectorizer_file, "rb") as vf:
                    vdata = pickle.load(vf)
                    if len(vdata) != 3:
                        raise ValueError("Invalid vectorizer file format")
                    _, _, vectorizer = vdata
                    
    except (pickle.UnpicklingError, EOFError, ImportError) as e:
        raise RuntimeError(f"Failed to load model: {e}")

    # Vectorize the input email
    email_vector = vectorizer.transform([email_text]).toarray()

    # Make a prediction
    prediction = model.predict(email_vector)
    return "Phishing" if prediction[0] == 1 else "Not Phishing"

if __name__ == "__main__":
    email_text = "Your account has been compromised. Click here to reset your password."
    try:
        result = predict_email("models/phishing_detector.pkl", email_text)
        print(f"Prediction: {result}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
