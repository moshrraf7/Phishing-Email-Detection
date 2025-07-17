import pickle
import os
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def train_model(data_file, model_file):
    # Validate input files
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file not found: {data_file}")
    
    # Create model directory if it doesn't exist
    model_dir = os.path.dirname(model_file)
    if model_dir and not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    try:
        # Load preprocessed data
        with open(data_file, "rb") as f:
            data = pickle.load(f)
            if len(data) != 3:
                raise ValueError("Invalid data file format")
            X, y, vectorizer = data
    except (pickle.UnpicklingError, EOFError, ImportError) as e:
        raise RuntimeError(f"Failed to load data: {e}")

    # Validate data
    if len(X) == 0 or len(y) == 0:
        raise ValueError("Empty dataset provided")
    
    if len(X) != len(y):
        raise ValueError("Mismatch between features and labels")

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train a Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Not Phishing', 'Phishing']))

    try:
        # Save the trained model and vectorizer together
        with open(model_file, "wb") as f:
            pickle.dump({'model': model, 'vectorizer': vectorizer}, f)
    except Exception as e:
        raise RuntimeError(f"Failed to save model: {e}")

    print(f"Model and vectorizer saved to {model_file}")

if __name__ == "__main__":
    try:
        train_model("data/preprocessed_data.pkl", "models/phishing_detector.pkl")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
