"use client";

import { useState } from 'react';
import { DiabetesFormData, PredictionResponse } from '@/types';

const initialFormData: DiabetesFormData = {
  pregnancies: 0,
  glucose: 0,
  bloodPressure: 0,
  skinThickness: 0,
  insulin: 0,
  bmi: 0,
  diabetesPedigreeFunction: 0,
  age: 0,
};

export default function PredictionForm() {
  const [formData, setFormData] = useState<DiabetesFormData>(initialFormData);
  const [prediction, setPrediction] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      const data: PredictionResponse = await response.json();
      setPrediction(data.prediction === 1 ? 'Positive' : 'Negative');
    } catch (error) {
      console.error('Error:', error);
      setPrediction('Error occurred during prediction');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: parseFloat(value) || 0
    }));
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-xl">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Diabetes Prediction</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        {Object.keys(initialFormData).map((field) => (
          <div key={field}>
            <label className="block text-sm font-medium text-gray-800 mb-1">
              {field.charAt(0).toUpperCase() + field.slice(1).replace(/([A-Z])/g, ' $1')}
            </label>
            <input
              type="number"
              name={field}
              step="0.01"
              title={field.charAt(0).toUpperCase() + field.slice(1).replace(/([A-Z])/g, ' $1')}
              placeholder={field.charAt(0).toUpperCase() + field.slice(1).replace(/([A-Z])/g, ' $1')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-500"
              value={formData[field as keyof DiabetesFormData]}
              onChange={handleInputChange}
              required
            />
          </div>
        ))}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-blue-300 font-medium"
        >
          {isLoading ? 'Processing...' : 'Predict'}
        </button>
      </form>
      {prediction && (
        <div className={`mt-6 p-4 rounded-md ${
          prediction === 'Positive' 
            ? 'bg-red-100 text-red-800' 
            : 'bg-green-100 text-green-800'
        }`}>
          <p className="text-center font-semibold">
            Prediction result (rule based): {prediction}
          </p>
        </div>
      )}
    </div>
  );
}