import { NextResponse } from 'next/server';
import { type NextRequest } from 'next/server';

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

    // Calculate risk score with validated input
    let riskScore = 0;
    
    if (input.glucose > 140) riskScore += 0.3;
    if (input.glucose > 200) riskScore += 0.2;
    if (input.bmi > 30) riskScore += 0.2;
    if (input.bmi > 35) riskScore += 0.1;
    if (input.bloodPressure > 120) riskScore += 0.1;
    if (input.age > 40) riskScore += 0.1;
    if (input.insulin > 166) riskScore += 0.1;
    if (input.skinThickness > 35) riskScore += 0.05;
    if (input.diabetesPedigreeFunction > 0.5) riskScore += 0.15;

    const probability = Math.min(riskScore, 1);
    const prediction = probability >= 0.5 ? 1 : 0;

    return NextResponse.json({
      prediction,
      probability: Number(probability.toFixed(3)),
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