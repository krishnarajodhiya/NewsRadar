"""
Model Training Script
Creates and trains a Logistic Regression model with TF-IDF vectorizer
Saves the model and vectorizer as pickle files
Uses Kaggle's Fake and Real News Dataset for training
"""
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from pathlib import Path
from preprocessor import preprocess_text
import kagglehub

# Model directory
MODEL_DIR = Path(__file__).parent.parent / "models"
MODEL_PATH = MODEL_DIR / "model.pkl"
VECTORIZER_PATH = MODEL_DIR / "vectorizer.pkl"


def create_sample_dataset():
    """
    Download and load the Kaggle Fake and Real News Dataset
    https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
    
    Dataset contains:
    - True.csv: Real news articles
    - Fake.csv: Fake news articles
    
    Uses a stratified sample for faster training while maintaining dataset quality
    """
    try:
        print("Downloading Kaggle Fake and Real News Dataset...")
        path = kagglehub.dataset_download("clmentbisaillon/fake-and-real-news-dataset")
        
        # Load the CSV files
        print(f"Dataset downloaded to: {path}")
        
        true_df = pd.read_csv(os.path.join(path, "True.csv"))
        fake_df = pd.read_csv(os.path.join(path, "Fake.csv"))
        
        # Add label column
        true_df['label'] = 'REAL'
        fake_df['label'] = 'FAKE'
        
        # Combine text columns (title + text) for better training
        true_df['text'] = true_df['title'] + ' ' + true_df['text']
        fake_df['text'] = fake_df['title'] + ' ' + fake_df['text']
        
        # Select relevant columns
        true_df = true_df[['text', 'label']]
        fake_df = fake_df[['text', 'label']]
        
        # Combine datasets
        data = pd.concat([true_df, fake_df], ignore_index=True)
        
        # Use stratified sample for faster training (5000 samples = 50x more than original)
        # This balances speed with accuracy
        sample_size = min(5000, len(data))
        print(f"\nOriginal dataset: {len(data)} samples")
        data = data.groupby('label', group_keys=False).apply(
            lambda x: x.sample(n=min(len(x), sample_size//2), random_state=42)
        )
        
        # Shuffle the dataset
        data = data.sample(frac=1, random_state=42).reset_index(drop=True)
        
        print(f"✓ Dataset loaded successfully!")
        print(f"  Training samples: {len(data)}")
        print(f"  Real news: {(data['label'] == 'REAL').sum()}")
        print(f"  Fake news: {(data['label'] == 'FAKE').sum()}")
        
        return data
        
    except Exception as e:
        print(f"⚠ Error downloading Kaggle dataset: {e}")
        print("Make sure your Kaggle API credentials are set up properly.")
        print("Instructions: https://github.com/Kaggle/kaggle-api#api-credentials")
        raise


def train_model():
    """Train and save the fake news detection model"""
    print("Loading training data...")
    
    # Create dataset
    df = create_sample_dataset()
    
    print(f"Dataset size: {len(df)}")
    print(f"FAKE news: {(df['label'] == 'FAKE').sum()}")
    print(f"REAL news: {(df['label'] == 'REAL').sum()}")
    
    print("\nPreprocessing text...")
    df['processed_text'] = df['text'].apply(preprocess_text)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df['processed_text'],
        df['label'],
        test_size=0.2,
        random_state=42,
        stratify=df['label']
    )
    
    print("\nCreating TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        min_df=1,
        max_df=0.8,
        ngram_range=(1, 2),
        sublinear_tf=True
    )
    
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"TF-IDF features: {X_train_tfidf.shape[1]}")
    
    print("\nTraining Logistic Regression model...")
    model = LogisticRegression(
        max_iter=200,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train_tfidf, y_train)
    
    print("\nEvaluating model...")
    y_pred = model.predict(X_test_tfidf)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    
    # Save model
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    print(f"\nSaving model to {MODEL_PATH}...")
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Saving vectorizer to {VECTORIZER_PATH}...")
    with open(VECTORIZER_PATH, 'wb') as f:
        pickle.dump(vectorizer, f)
    
    print("\n✓ Model training complete!")
    print(f"✓ Model saved at: {MODEL_PATH}")
    print(f"✓ Vectorizer saved at: {VECTORIZER_PATH}")


if __name__ == "__main__":
    train_model()
