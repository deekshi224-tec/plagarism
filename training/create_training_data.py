# create_training_data.py
import pandas as pd
import os

# Create proper training data for plagiarism detection
def create_training_data():
    """Create training data with text pairs"""
    
    training_data = []
    
    # PLAGIARIZED PAIRS (Label = 1)
    plagiarized_pairs = [
        # Identical texts
        ("Artificial intelligence is transforming the world.", 
         "Artificial intelligence is transforming the world.", 1),
        
        ("Machine learning algorithms learn from data.", 
         "Machine learning algorithms learn from data.", 1),
        
        ("The quick brown fox jumps over the lazy dog.", 
         "The quick brown fox jumps over the lazy dog.", 1),
        
        # Very similar texts (paraphrased)
        ("AI is revolutionizing the way we work and live.", 
         "Artificial intelligence is changing how we work and live.", 1),
        
        ("Machine learning models can predict future outcomes.", 
         "ML models are able to predict future results.", 1),
        
        ("The company reported record profits this quarter.", 
         "The business announced record earnings this quarter.", 1),
        
        ("Climate change is a serious global concern.", 
         "Global warming is a major worldwide issue.", 1),
        
        ("Scientists discovered a new species of butterfly.", 
         "Researchers found a new butterfly species.", 1),
        
        ("The movie received critical acclaim from reviewers.", 
         "The film got critical praise from critics.", 1),
        
        ("Exercise is important for maintaining good health.", 
         "Physical activity is crucial for staying healthy.", 1),
        
        # Modified texts
        ("The stock market experienced significant volatility.", 
         "The stock market saw major ups and downs.", 1),
        
        ("The new smartphone has amazing features and capabilities.", 
         "The latest phone has great features and functions.", 1),
    ]
    
    # ORIGINAL PAIRS (Label = 0)
    original_pairs = [
        # Completely different topics
        ("Artificial intelligence is transforming technology.", 
         "The weather today is beautiful and sunny.", 0),
        
        ("Machine learning algorithms learn from data.", 
         "My favorite food is pizza and pasta.", 0),
        
        ("The company reported record profits this quarter.", 
         "The cat sat on the comfortable mat.", 0),
        
        # Different meanings
        ("Climate change is a serious global concern.", 
         "The movie received critical acclaim from reviewers.", 0),
        
        ("Scientists discovered a new species of butterfly.", 
         "The stock market experienced significant volatility.", 0),
        
        ("Exercise is important for maintaining good health.", 
         "The new smartphone has amazing features.", 0),
        
        # Different contexts
        ("AI is revolutionizing healthcare industry.", 
         "The beach is crowded during summer vacation.", 0),
        
        ("Machine learning models predict outcomes.", 
         "Coffee is my favorite morning beverage.", 0),
        
        ("The company announced new product launch.", 
         "Gardening is a relaxing and rewarding hobby.", 0),
        
        ("Global warming affects polar ice caps.", 
         "The restaurant serves delicious Italian food.", 0),
        
        ("Quantum computing uses qubits for calculations.", 
         "The concert was amazing last night.", 0),
        
        ("Space exploration reveals new planets.", 
         "The book was interesting and well-written.", 0),
    ]
    
    # Combine all data
    for t1, t2, label in plagiarized_pairs:
        training_data.append({
            'text1': t1,
            'text2': t2,
            'label': label
        })
    
    for t1, t2, label in original_pairs:
        training_data.append({
            'text1': t1,
            'text2': t2,
            'label': label
        })
    
    # Create DataFrame
    df = pd.DataFrame(training_data)
    
    # Save to CSV
    os.makedirs("dataset", exist_ok=True)
    df.to_csv("dataset/training_data.csv", index=False)
    
    print(f"✅ Created training data with {len(df)} samples")
    print(f"   Plagiarized pairs: {len(plagiarized_pairs)}")
    print(f"   Original pairs: {len(original_pairs)}")
    print(f"   Saved to: dataset/training_data.csv")
    
    return df

if __name__ == "__main__":
    create_training_data()