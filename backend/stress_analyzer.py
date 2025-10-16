import numpy as np
from sklearn.ensemble import RandomForestClassifier

class StressAnalyzer:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        # Sample training data
        self.X_train = np.array([
            [8, 10, 1, 6],  # work_hours, meeting_count, breaks, stress_level
            [7, 8, 3, 4],
            [9, 12, 1, 8],
            [6, 6, 4, 3]
        ])
        self.y_train = np.array([1, 0, 1, 0])  # 1 = high stress, 0 = low stress
        self.train_model()
    
    def train_model(self):
        self.model.fit(self.X_train, self.y_train)
    
    def predict_stress_risk(self, work_hours, meetings, breaks, current_stress):
        features = np.array([[work_hours, meetings, breaks, current_stress]])
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0][1]
        
        return {
            "risk_level": "high" if prediction == 1 else "low",
            "confidence": float(probability),
            "needs_intervention": probability > 0.7
        }

stress_analyzer = StressAnalyzer()
