import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import joblib
from datetime import datetime

# Choose a loss function
def calculate_loss(y_true, y_pred):
  return mean_squared_error(y_true, y_pred)

def feature_importance(model, feature_names):
  return pd.DataFrame(model.feature_importances_, index=feature_names, columns=['importance']).sort_values('importance', ascending=False)

def confidence_interval(predictions, confidence=0.95):
  mean = np.mean(predictions)
  std_err = np.std(predictions) / np.sqrt(len(predictions))
  margin = std_err * 1.96  # for 95% confidence
  return mean - margin, mean + margin

def serialize_model(model, scaler, filename="model", path="."):
  """Save the trained model and scaler as a serialized .pkl file."""
  timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
  full_path = f"{path}/{filename}-{timestamp}.pkl"
  joblib.dump({'model': model, 'scaler': scaler}, full_path)
  print(f"Model and scaler saved as: {full_path}")

