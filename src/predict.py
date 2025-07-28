import pickle
import os

def predict_email(model_file, vectorizer_file, email_text):
    # Load the model
    with open(model_file, "rb") as f:
        model = pickle.load(f)

    # Load the vectorizer
    with open(vectorizer_file, "rb") as f:
        _, _, vectorizer = pickle.load(f)

    # Vectorize the input email
    email_vector = vectorizer.transform([email_text]).toarray()

    # Make a prediction
    prediction = model.predict(email_vector)
    return "Phishing" if prediction[0] == 1 else "Not Phishing"

if __name__ == "__main__":
    # Get the directory of the script and navigate to project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    model_file = os.path.join(project_root, "models", "phishing_detector.pkl")
    vectorizer_file = os.path.join(project_root, "data", "preprocessed_data.pkl")
    
    email_text = "Your account has been compromised. Click here to reset your password."
    result = predict_email(model_file, vectorizer_file, email_text)
    print(f"Prediction: {result}")
