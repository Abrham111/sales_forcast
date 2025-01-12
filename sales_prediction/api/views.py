# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PredictionSerializer
from .model import model  # Import the pre-loaded model
import pandas as pd

class SalesPredictionView(APIView):
  def post(self, request):
    serializer = PredictionSerializer(data=request.data)
    
    # Validate the incoming data
    if serializer.is_valid():
      input_data = serializer.validated_data
      prediction_result = self.make_prediction(input_data)
      
      return Response({'prediction': prediction_result.tolist()}, status=status.HTTP_200_OK)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def make_prediction(self, input_data):
    # Convert input data to DataFrame
    df = pd.DataFrame([input_data])
    
    # Preprocess the input data using the scaler
    scaled_data = model['scaler'].transform(df)  # Access the scaler from the loaded model
    
    # Make prediction
    prediction = model['model'].predict(scaled_data)  # Access the model from the loaded model
    return prediction