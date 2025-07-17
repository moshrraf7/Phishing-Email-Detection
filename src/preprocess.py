import pandas as pd
import numpy as np
import re
import os
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def clean_text(text):
    """Clean and normalize text data"""
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def preprocess_data(input_file, output_file):
    # Validate input file
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        # Load the CSV file
        data = pd.read_csv(input_file)
    except Exception as e:
        raise RuntimeError(f"Failed to load CSV file: {e}")

    # Ensure the dataset has 'text' and 'label' columns
    if 'text' not in data.columns or 'label' not in data.columns:
        raise ValueError("Input CSV must have 'text' and 'label' columns.")

    # Data validation and cleaning
    print(f"Original dataset size: {len(data)}")
    
    # Remove rows with missing values
    data = data.dropna()
    print(f"After removing NaN values: {len(data)}")
    
    # Clean text data
    data['text'] = data['text'].apply(clean_text)
    
    # Remove empty text entries after cleaning
    data = data[data['text'].str.len() > 0]
    print(f"After removing empty text: {len(data)}")
    
    # Validate labels (should be 0 or 1)
    unique_labels = data['label'].unique()
    if not all(label in [0, 1] for label in unique_labels):
        raise ValueError("Labels must be 0 (Not Phishing) or 1 (Phishing)")
    
    if len(data) == 0:
        raise ValueError("No valid data remaining after preprocessing")

    # Vectorize the text using TF-IDF with better parameters
    vectorizer = TfidfVectorizer(
        max_features=5000,  # Limit features to prevent overfitting
        stop_words='english',  # Remove common English stop words
        min_df=2,  # Ignore terms that appear in fewer than 2 documents
        max_df=0.95,  # Ignore terms that appear in more than 95% of documents
        ngram_range=(1, 2)  # Include both unigrams and bigrams
    )
    
    # Keep as sparse matrix for memory efficiency
    X = vectorizer.fit_transform(data['text'])
    print(f"TF-IDF matrix shape: {X.shape}")
    print(f"TF-IDF matrix sparsity: {(1 - X.nnz / (X.shape[0] * X.shape[1])) * 100:.2f}%")

    # Extract labels
    y = data['label'].values

    # Save preprocessed data and vectorizer
    try:
        with open(output_file, "wb") as f:
            # Save sparse matrix for memory efficiency
            pickle.dump((X, y, vectorizer), f)
    except Exception as e:
        raise RuntimeError(f"Failed to save preprocessed data: {e}")

    print(f"Preprocessed data saved to {output_file}")
    print(f"Class distribution: {np.bincount(y)}")

if __name__ == "__main__":
    try:
        preprocess_data("data/phishing_emails.csv", "data/preprocessed_data.pkl")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
