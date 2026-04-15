# app/predictor.py
import pickle
import os
import sys
from utils.preprocessing import clean_text

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_model = None
_vectorizer = None

def load_models():
    """Load the trained model and vectorizer"""
    global _model, _vectorizer
    
    if _model is not None and _vectorizer is not None:
        return _model, _vectorizer
    
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, "models", "plagiarism_model.pkl")
        vectorizer_path = os.path.join(base_dir, "models", "vectorizer.pkl")
        
        with open(model_path, "rb") as f:
            _model = pickle.load(f)
        
        with open(vectorizer_path, "rb") as f:
            _vectorizer = pickle.load(f)
        
        return _model, _vectorizer
        
    except Exception as e:
        raise Exception(f"Error loading models: {e}")

def detect_plagiarism(text1, text2):
    """
    Detect plagiarism between two texts
    Returns: (prediction, confidence, probabilities)
    """
    try:
        model, vectorizer = load_models()
        
        # Clean texts
        text1_clean = clean_text(text1)
        text2_clean = clean_text(text2)
        
        # Combine with separator
        combined = text1_clean + " [SEP] " + text2_clean
        
        # Transform and predict
        vector = vectorizer.transform([combined])
        prediction = model.predict(vector)[0]
        probabilities = model.predict_proba(vector)[0]
        confidence = max(probabilities)
        
        return int(prediction), float(confidence), probabilities.tolist()
        
    except Exception as e:
        raise Exception(f"Error: {e}")

def analyze_text_pair(text1, text2):
    """Comprehensive analysis"""
    try:
        prediction, confidence, probabilities = detect_plagiarism(text1, text2)
        
        return {
            "prediction": prediction,
            "is_plagiarized": bool(prediction == 1),
            "confidence": confidence,
            "confidence_percentage": confidence * 100,
            "original_probability": probabilities[0],
            "plagiarized_probability": probabilities[1],
            "status": "⚠️ Plagiarism Detected!" if prediction == 1 else "✅ Original Content"
        }
    except Exception as e:
        return {"error": True, "message": str(e)}

def get_model_info():
    """Get model information"""
    try:
        model, vectorizer = load_models()
        return {
            "model_type": type(model).__name__,
            "classes": model.classes_.tolist(),
            "features": vectorizer.get_feature_names_out().shape[0]
        }
    except:
        return {"error": "Model not loaded"}