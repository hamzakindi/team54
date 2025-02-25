import requests
import json

def test_prediction(data, test_name=""):
    """Make a prediction request and print the results"""
    # Try Next.js server first, then Python server as fallback
    urls = [
        "http://localhost:3000/api/predict",
        "http://localhost:8000/predict"
    ]
    
    for url in urls:
        try:
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json=data
            )
            print(f"\n=== {test_name} ===")
            print(f"URL: {url}")
            print(f"Request: {json.dumps(data, indent=2)}")
            print(f"Response Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return
        except requests.RequestException as e:
            continue
    print(f"\nError: Could not connect to any server for {test_name}")

# Test cases
high_risk_case = {
    "pregnancies": 6,
    "glucose": 195,
    "bloodPressure": 130,
    "skinThickness": 40,
    "insulin": 180,
    "bmi": 37.2,
    "diabetesPedigreeFunction": 0.6,
    "age": 45
}

low_risk_case = {
    "pregnancies": 1,
    "glucose": 85,
    "bloodPressure": 66,
    "skinThickness": 29,
    "insulin": 100,
    "bmi": 23.5,
    "diabetesPedigreeFunction": 0.351,
    "age": 31
}

minimum_values_case = {
    "pregnancies": 0,
    "glucose": 0,
    "bloodPressure": 0,
    "skinThickness": 0,
    "insulin": 0,
    "bmi": 0,
    "diabetesPedigreeFunction": 0,
    "age": 0
}

custom_values_case = {
    "pregnancies": 5,
    "glucose": 117,
    "bloodPressure": 92,
    "skinThickness": 0,
    "insulin": 0,
    "bmi": 34.1,
    "diabetesPedigreeFunction": 0.337,
    "age": 38
}

dataset_values_case = {
    "pregnancies": 10,
    "glucose": 125,
    "bloodPressure": 70,
    "skinThickness": 26,
    "insulin": 115,
    "bmi": 31.1,
    "diabetesPedigreeFunction": 0.205,
    "age": 41
}

negative_case = {
    "pregnancies": 3,
    "glucose": 126,
    "bloodPressure": 88,
    "skinThickness": 41,
    "insulin": 235,
    "bmi": 39.3,
    "diabetesPedigreeFunction": 0.704,
    "age": 27
}

positive_case = {
    "pregnancies": 7,
    "glucose": 196,
    "bloodPressure": 90,
    "skinThickness": 0,
    "insulin": 0,
    "bmi": 39.8,
    "diabetesPedigreeFunction": 0.451,
    "age": 41
}

if __name__ == "__main__":
    test_prediction(high_risk_case, "High Risk Case")
    test_prediction(low_risk_case, "Low Risk Case")
    test_prediction(minimum_values_case, "Minimum Values Case")
    test_prediction(custom_values_case, "Custom Values Case")
    test_prediction(dataset_values_case, "Dataset Values Case")
    test_prediction(negative_case, "Negative Case")
    test_prediction(positive_case, "Positive Case")