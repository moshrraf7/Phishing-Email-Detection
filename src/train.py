import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

def train_model(data_file, model_file):
    # Load preprocessed data
    with open(data_file, "rb") as f:
        X, y, _ = pickle.load(f)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Random Forest model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")

    # Save the trained model
    with open(model_file, "wb") as f:
        pickle.dump(model, f)

    print(f"Model saved to {model_file}")

if __name__ == "__main__":
    # Get the directory of the script and navigate to project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    data_file = os.path.join(project_root, "data", "preprocessed_data.pkl")
    model_file = os.path.join(project_root, "models", "phishing_detector.pkl")
    
    train_model(data_file, model_file)
