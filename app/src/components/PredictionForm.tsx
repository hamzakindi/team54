"use client";

import { useState } from 'react';
import { DiabetesFormData, PredictionResponse, TestRecommendation } from '@/types';

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
  const [probability, setProbability] = useState<number|undefined>(0);
  const [testRecommendations, setTestRecommendations] = useState<TestRecommendation[]>([]);
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
      setProbability(data.probability);
      setTestRecommendations(data.testRecommendations.tests);
    } catch (error) {
      console.error('Error:', error);
      setPrediction('Error occurred during prediction');
      setProbability(0);
      setTestRecommendations([]);
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
    <div className="h-full bg-white rounded-lg shadow-xl overflow-hidden">
      <div className="grid grid-cols-1 md:grid-cols-2 h-full">
        {/* Form Section */}
        <div className="h-full p-6 md:p-8 md:border-r border-gray-200 overflow-y-auto">
          <div className="space-y-6">
            <h3 className="text-xl font-semibold text-gray-700">
              Patient Information
            </h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {Object.keys(initialFormData).map((field) => (
                  <div key={field} className="relative">
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      {field.charAt(0).toUpperCase() + field.slice(1).replace(/([A-Z])/g, ' $1')}
                    </label>
                    <input
                      type="number"
                      name={field}
                      step="0.01"
                      title={field.charAt(0).toUpperCase() + field.slice(1).replace(/([A-Z])/g, ' $1')}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md 
                               focus:ring-2 focus:ring-blue-500 focus:border-blue-500 
                               text-gray-900 placeholder-gray-400 shadow-sm"
                      value={formData[field as keyof DiabetesFormData]}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                ))}
              </div>
              <button
                type="submit"
                disabled={isLoading}
                className="w-full mt-6 bg-blue-600 text-white py-3 px-4 rounded-md
                         hover:bg-blue-700 disabled:bg-blue-300 font-medium
                         transform transition duration-200 hover:scale-[1.02]
                         focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                {isLoading ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                    </svg>
                    Processing...
                  </span>
                ) : 'Analyze Risk'}
              </button>
            </form>
          </div>
        </div>

        {/* Results Section */}
        <div className={`h-full p-6 md:p-8 bg-gray-50 overflow-y-auto ${prediction ? 'block' : 'hidden md:block'}`}>
          {prediction ? (
            <div className="space-y-6">
              <h3 className="text-xl font-semibold text-gray-700 mb-6">
                Assessment Results
              </h3>
              
              <div className={`p-6 rounded-lg border-2 ${
                prediction === 'Positive' 
                  ? 'border-red-200 bg-red-50 text-red-800' 
                  : 'border-green-200 bg-green-50 text-green-800'
              }`}>
                <div className="text-center space-y-2">
                  <p className="text-2xl font-bold">
                    {prediction === 'Positive' ? 'High Risk' : 'Low Risk'}
                  </p>
                  <div className="flex items-center justify-center gap-2">
                    <div className="h-2 w-full bg-gray-200 rounded-full">
                      <div 
                        className={`h-2 rounded-full ${prediction === 'Positive' ? 'bg-red-500' : 'bg-green-500'}`}
                        style={{ width: `${probability ? probability * 100 : 0}%` }}
                      />
                    </div>
                    <span className="text-sm font-medium w-20">
                      {probability ? (probability * 100).toFixed(1) : 0}%
                    </span>
                  </div>
                </div>
              </div>

              {testRecommendations.length > 0 && (
                <div className="mt-6">
                  <h4 className="text-lg font-semibold text-gray-700 mb-4">
                    Recommended Tests
                  </h4>
                  <div className="space-y-3">
                    {testRecommendations.map((test, index) => (
                      <div 
                        key={index} 
                        className="p-4 bg-white rounded-lg border border-gray-200 hover:shadow-md transition-shadow"
                      >
                        <div className="flex items-center justify-between">
                          <h5 className="font-medium text-gray-900">{test.name}</h5>
                          <span className={`px-3 py-1 text-xs rounded-full font-medium ${
                            test.priority === 'required' 
                              ? 'bg-red-100 text-red-800 border border-red-200'
                              : 'bg-yellow-100 text-yellow-800 border border-yellow-200'
                          }`}>
                            {test.priority}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mt-2">{test.description}</p>
                        <p className="text-sm text-gray-500 mt-1 font-medium">
                          Normal Range: {test.normalRange}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="h-full flex items-center justify-center">
              <p className="text-gray-500 text-center">
                Enter patient information and click &quot;Analyze Risk&quot; 
                to see the assessment results
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}