# utils/preprocessing.py
import re
import string

def clean_text(text):
    """
    Clean and preprocess text for plagiarism detection.
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove short words (optional)
    text = ' '.join([word for word in text.split() if len(word) > 2])
    
    return text

def combine_texts(text1, text2, separator=" [SEP] "):
    """Combine two cleaned texts with a separator."""
    return text1 + separator + text2