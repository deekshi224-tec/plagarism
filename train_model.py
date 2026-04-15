# train_model.py
import pandas as pd
import pickle
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Simple clean function (in case import fails)
def clean_text_simple(text):
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = ''.join([c for c in text if c.isalnum() or c.isspace()])
    text = ' '.join(text.split())
    return text

print("="*70)
print("🔍 TRAINING PLAGIARISM DETECTION MODEL")
print("="*70)

# Create training data directly (no external file)
print("\n📝 Creating training data...")

data = []

# ============ PLAGIARIZED PAIRS (label = 1) ============
plagiarized_pairs = [
    # Identical texts
    ("Artificial intelligence is transforming the world", 
     "Artificial intelligence is transforming the world"),
    ("Machine learning algorithms learn from data", 
     "Machine learning algorithms learn from data"),
    ("The quick brown fox jumps over the lazy dog", 
     "The quick brown fox jumps over the lazy dog"),
    ("Python is a popular programming language", 
     "Python is a popular programming language"),
    ("Data science is an interdisciplinary field", 
     "Data science is an interdisciplinary field"),
    
    # Very similar texts (paraphrased)
    ("AI is revolutionizing the way we work", 
     "Artificial intelligence is changing how we work"),
    ("Machine learning can predict future outcomes", 
     "ML models can forecast future results"),
    ("The company reported record profits", 
     "The business announced record earnings"),
    ("Climate change is a global concern", 
     "Global warming is a worldwide issue"),
    ("The movie received critical acclaim", 
     "The film got critical praise"),
    ("Exercise is important for health", 
     "Physical activity is crucial for health"),
    ("The new smartphone has amazing features", 
     "The latest phone has great features"),
    ("Scientists discovered a new species", 
     "Researchers found a new species"),
]

# ============ ORIGINAL PAIRS (label = 0) ============
original_pairs = [
    # Completely different topics
    ("Artificial intelligence is transforming technology", 
     "The weather today is beautiful and sunny"),
    ("Machine learning algorithms learn from data", 
     "My favorite food is pizza and pasta"),
    ("The company reported record profits", 
     "The cat sat on the comfortable mat"),
    ("Climate change is a serious concern", 
     "The movie received critical acclaim"),
    ("Scientists discovered a new species", 
     "The stock market experienced volatility"),
    ("Exercise is important for health", 
     "The new smartphone has amazing features"),
    ("AI is revolutionizing healthcare", 
     "The beach is crowded during summer"),
    ("Machine learning models predict outcomes", 
     "Coffee is my favorite morning beverage"),
    ("Quantum computing uses qubits", 
     "The concert was amazing last night"),
    ("Space exploration reveals new planets", 
     "The book was interesting and well-written"),
    ("Deep learning requires large datasets", 
     "The garden has beautiful flowers"),
    ("Natural language processing is complex", 
     "The food was delicious and tasty"),
]

# Add plagiarized pairs (label=1)
for text1, text2 in plagiarized_pairs:
    data.append({'text1': text1, 'text2': text2, 'label': 1})

# Add original pairs (label=0)
for text1, text2 in original_pairs:
    data.append({'text1': text1, 'text2': text2, 'label': 0})

df = pd.DataFrame(data)

print(f"✅ Created training data with {len(df)} samples")
print(f"   Plagiarized (label=1): {(df['label']==1).sum()} samples")
print(f"   Original (label=0): {(df['label']==0).sum()} samples")

# Preprocess texts
print("\n🔄 Preprocessing texts...")

# Use simple clean function
df['text1_clean'] = df['text1'].apply(clean_text_simple)
df['text2_clean'] = df['text2'].apply(clean_text_simple)

# Combine texts with separator
df['combined'] = df['text1_clean'] + " [SEP] " + df['text2_clean']

print(f"\n📝 Sample combined text:")
print(f"  {df['combined'].iloc[0][:150]}...")

# Create TF-IDF features
print("\n🔧 Creating TF-IDF features...")
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 3),
    stop_words='english',
    min_df=2
)

X = vectorizer.fit_transform(df['combined'])
y = df['label'].values

print(f"  Feature matrix: {X.shape[0]} samples, {X.shape[1]} features")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n📈 Data split:")
print(f"  Training: {X_train.shape[0]} samples")
print(f"  Testing: {X_test.shape[0]} samples")

# Train model
print("\n🤖 Training Logistic Regression...")
model = LogisticRegression(
    max_iter=1000,
    C=1.0,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n✅ Model Accuracy: {accuracy:.2%}")
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Original', 'Plagiarized']))

# Save model
print("\n💾 Saving model...")
os.makedirs("models", exist_ok=True)

with open("models/plagiarism_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("models/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Model saved to models/")

# Test the model with different inputs
print("\n" + "="*70)
print("🧪 TESTING MODEL WITH DIFFERENT INPUTS")
print("="*70)

test_cases = [
    ("The quick brown fox jumps over the lazy dog", 
     "The quick brown fox jumps over the lazy dog", 
     "IDENTICAL TEXTS"),
    
    ("Artificial intelligence is transforming the world", 
     "AI is transforming the world", 
     "VERY SIMILAR TEXTS"),
    
    ("Machine learning is great", 
     "ML is wonderful", 
     "SIMILAR TEXTS"),
    
    ("The weather is beautiful today", 
     "Python is a programming language", 
     "DIFFERENT TEXTS"),
    
    ("Cats are pets", 
     "Quantum computing uses qubits", 
     "COMPLETELY DIFFERENT"),
]

print("\n📊 Test Results:")
print("-"*70)

for text1, text2, desc in test_cases:
    # Clean and combine
    t1_clean = clean_text_simple(text1)
    t2_clean = clean_text_simple(text2)
    combined = t1_clean + " [SEP] " + t2_clean
    
    # Predict
    vec = vectorizer.transform([combined])
    pred = model.predict(vec)[0]
    proba = model.predict_proba(vec)[0]
    confidence = max(proba)
    
    result = "🔴 PLAGIARISM DETECTED" if pred == 1 else "🟢 ORIGINAL"
    
    print(f"\n{desc}:")
    print(f"  Text 1: {text1[:50]}...")
    print(f"  Text 2: {text2[:50]}...")
    print(f"  Result: {result}")
    print(f"  Confidence: {confidence:.1%}")
    print(f"  Original Probability: {proba[0]:.1%}")
    print(f"  Plagiarized Probability: {proba[1]:.1%}")

print("\n" + "="*70)
print("✅ Training complete!")
print("\n📌 NOTE: You should see DIFFERENT confidence levels for different inputs!")
print("   - Identical texts should show HIGH plagiarism confidence (80-99%)")
print("   - Different texts should show LOW plagiarism confidence (10-30%)")
print("\nNow run the UI:")
print("   python -m streamlit run ui/streamlit_app.py")
print("="*70)