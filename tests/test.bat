:: Test predict endpoint
curl -X POST http://localhost:8000/predict ^
-H "Content-Type: application/json" ^
-d "{\"pregnancies\": 1, \"glucose\": 103, \"bloodPressure\": 30, \"skinThickness\": 38, \"insulin\": 83, \"bmi\": 43.3, \"diabetesPedigreeFunction\": 0.183, \"age\": 33}"

:: Test health endpoint
curl http://localhost:8000/health