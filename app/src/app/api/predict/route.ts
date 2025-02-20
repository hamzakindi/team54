import { NextResponse } from 'next/server';
import { type NextRequest } from 'next/server';

const EXTERNAL_API_URL = 'http://localhost:8000/predict';

const constraints = {
  pregnancies: { min: 0, max: 20 },
  glucose: { min: 0, max: 500 },
  bloodPressure: { min: 0, max: 300 },
  skinThickness: { min: 0, max: 100 },
  insulin: { min: 0, max: 2000 },
  bmi: { min: 0, max: 150 },
  diabetesPedigreeFunction: { min: 0, max: 20 },
  age: { min: 0, max: 120 }
};

export async function POST(request: NextRequest) {
  try {
    // Check if request has a body
    if (!request.body) {
      return NextResponse.json({
        message: 'Request body is missing',
        status: 'error'
      }, { status: 400 });
    }

    // Parse JSON with error handling
    const input = await request.json().catch(() => null);
    
    // Check if JSON parsing was successful
    if (!input) {
      return NextResponse.json({
        message: 'Invalid JSON format',
        status: 'error'
      }, { status: 400 });
    }

    // Check for required fields
    const requiredFields = Object.keys(constraints);
    const missingFields = requiredFields.filter(field => !(field in input));
    
    if (missingFields.length > 0) {
      return NextResponse.json({
        message: 'Missing required fields',
        errors: missingFields,
        status: 'error'
      }, { status: 400 });
    }

    // Validate input values
    const validationErrors = [];
    for (const [field, value] of Object.entries(input)) {
      const constraint = constraints[field as keyof typeof constraints];
      if (typeof value !== 'number' || isNaN(value) || value < constraint.min || value > constraint.max) {
        validationErrors.push(
          `${field} must be a number between ${constraint.min} and ${constraint.max}`
        );
      }
    }

    if (validationErrors.length > 0) {
      return NextResponse.json({
        message: 'Validation failed',
        errors: validationErrors,
        status: 'error'
      }, { status: 400 });
    }

    // Make call to external API
    const externalResponse = await fetch(EXTERNAL_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(input)
    });

    if (!externalResponse.ok) {
      const errorData = await externalResponse.json();
      throw new Error(errorData.message || 'External API request failed');
    }

    const predictionData = await externalResponse.json();

    return NextResponse.json({
      prediction: Number(predictionData.prediction),
      probability: predictionData.probability,
      status: 'success'
    });

  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json({ 
      message: error instanceof Error ? error.message : 'Error making prediction',
      status: 'error'
    }, { status: 500 });
  }
}