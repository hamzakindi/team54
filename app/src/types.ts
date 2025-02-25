export interface DiabetesFormData {
  pregnancies: number;
  glucose: number;
  bloodPressure: number;
  skinThickness: number;
  insulin: number;
  bmi: number;
  diabetesPedigreeFunction: number;
  age: number;
}

export interface TestRecommendation {
  name: string;
  description: string;
  normalRange: string;
  priority: 'required' | 'recommended' | 'optional';
}

interface TestResponse {
  category: string;
  tests: TestRecommendation[];
}

export interface PredictionResponse {
  prediction: number;
  probability: number;
  testRecommendations: TestResponse;
  status: string;
}