#!/usr/bin/env python3
"""
Test script to verify phishing email detection accuracy
"""

import pickle

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

# Test cases
test_emails = [
    # Phishing emails
    ("URGENT: Your bank account will be closed! Click here NOW!", "Phishing"),
    ("You've won $10,000! Claim your prize immediately!", "Phishing"),
    ("Your PayPal account has been suspended. Verify your details.", "Phishing"),
    
    # Legitimate emails
    ("Thanks for the meeting yesterday. Here are the notes.", "Not Phishing"),
    ("Can we reschedule our lunch for tomorrow?", "Not Phishing"),
    ("Happy anniversary! Hope you both have a wonderful day.", "Not Phishing"),
]

print("=== Testing Phishing Email Detection ===\n")

correct_predictions = 0
total_predictions = len(test_emails)

for email_text, expected in test_emails:
    predicted = predict_email("models/phishing_detector.pkl", "data/preprocessed_data.pkl", email_text)
    is_correct = predicted == expected
    
    if is_correct:
        correct_predictions += 1
        status = "✓ CORRECT"
    else:
        status = "✗ INCORRECT"
    
    print(f"{status}")
    print(f"Email: {email_text}")
    print(f"Expected: {expected}, Predicted: {predicted}")
    print("-" * 60)

accuracy = (correct_predictions / total_predictions) * 100
print(f"\nOverall Test Accuracy: {correct_predictions}/{total_predictions} ({accuracy:.1f}%)")

if accuracy >= 80:
    print("🎉 Great! The model is working well!")
elif accuracy >= 60:
    print("⚠️  The model is working but could be improved.")
else:
    print("❌ The model needs improvement.")