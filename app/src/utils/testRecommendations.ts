export interface TestRecommendation {
  name: string;
  description: string;
  normalRange: string;
  priority: 'required' | 'recommended' | 'optional';
}

export interface TestResponse {
  category: string;
  tests: TestRecommendation[];
}

interface ApiResponse {
  status: 'success' | 'error';
  category: string;
  tests: [string, string, string, string][]; // [name, description, normalRange, priority]
}

const RECOMMENDATIONS_API_URL = process.env.NEXT_PUBLIC_RECOMMENDATIONS_API_URL || 'http://localhost:8001/api/recommendations';

// Convert snake_case to readable format
function formatTestName(name: string): string {
  return name
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

export async function getTestRecommendations(probability: number): Promise<TestResponse> {
  try {
    // Validate probability
    if (typeof probability !== 'number' || isNaN(probability) || probability < 0 || probability > 1) {
      throw new Error('Probability must be a number between 0 and 1');
    }

    const response = await fetch(RECOMMENDATIONS_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ probability }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }

    const data: ApiResponse = await response.json();
    
    // Add logging of raw API response
    console.log('API Response:', JSON.stringify(data, null, 2));
    
    if (data.status !== 'success') {
      throw new Error('API returned non-success status');
    }
    
    // Transform API response to match TestResponse format
    const transformedTests: TestRecommendation[] = data.tests.map(([name, description, normalRange, priority]) => ({
      name: formatTestName(name),
      description,
      normalRange,
      priority: priority.toLowerCase() as 'required' | 'recommended' | 'optional'
    }));

    // Log transformed response
    console.log('Transformed Response:', JSON.stringify({
      category: data.category,
      tests: transformedTests
    }, null, 2));

    return {
      category: data.category,
      tests: transformedTests
    };
  } catch (error) {
    console.error('Error fetching test recommendations:', error);
    if (error instanceof TypeError) {
      throw new Error('Network or parsing error occurred');
    } else if (error instanceof Response) {
      throw new Error(`Server responded with status: ${error.status}`);
    }
    throw error instanceof Error ? error : new Error('Failed to fetch test recommendations');
  }
}