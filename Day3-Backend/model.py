import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import os

class SecurityModel:
    def __init__(self):
        self.model = None
        self.load_or_create()
    
    def load_or_create(self):
        """Load existing model or create new one"""
        model_path = 'security_model.pkl'
        
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            print("✅ Model loaded from file")
        else:
            print("🔄 Creating new model...")
            # Create dummy training data
            X, y = make_classification(
                n_samples=1000, 
                n_features=10, 
                n_redundant=0,
                n_informative=10,
                random_state=42
            )
            
            self.model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=10
            )
            self.model.fit(X, y)
            joblib.dump(self.model, model_path)
            print("✅ Model trained and saved")
    
    def predict(self, features):
        """Predict security risk"""
        features = np.array(features).reshape(1, -1)
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        
        return {
            'prediction': int(prediction),
            'confidence': float(max(probabilities)),
            'risk_score': float(probabilities[1]) if prediction == 1 else float(1 - probabilities[0]),
            'risk_level': 'HIGH' if prediction == 1 else 'LOW'
        }

# Test
if __name__ == "__main__":
    model = SecurityModel()
    test = model.predict([0.5, 0.3, 0.8, 0.2, 0.9, 0.1, 0.7, 0.4, 0.6, 0.3])
    print("Test prediction:", test)