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

const baseTests: TestRecommendation[] = [
  {
    name: "Fasting Blood Glucose (FBG)",
    description: "Measures blood sugar levels after fasting for 8 hours",
    normalRange: "70-99 mg/dL",
    priority: "required"
  },
  {
    name: "HbA1c",
    description: "Reflects average blood glucose over past 2-3 months",
    normalRange: "Below 5.7%",
    priority: "required"
  }
];

const mediumRiskTests: TestRecommendation[] = [
  ...baseTests,
  {
    name: "Oral Glucose Tolerance Test (OGTT)",
    description: "Measures how well your body processes glucose",
    normalRange: "Below 140 mg/dL after 2 hours",
    priority: "required"
  },
  {
    name: "Fasting Insulin Level",
    description: "Measures insulin resistance",
    normalRange: "3-25 mIU/L",
    priority: "recommended"
  },
  {
    name: "Lipid Profile",
    description: "Measures different types of cholesterol",
    normalRange: "Varies by component",
    priority: "recommended"
  }
];

const highRiskTests: TestRecommendation[] = [
  ...mediumRiskTests,
  {
    name: "C-Peptide Test",
    description: "Measures insulin production by pancreas",
    normalRange: "0.5-2.0 ng/mL",
    priority: "required"
  },
  {
    name: "GAD Antibodies",
    description: "Helps distinguish between type 1 and type 2 diabetes",
    normalRange: "Below 5 IU/mL",
    priority: "recommended"
  },
  {
    name: "Microalbuminuria",
    description: "Checks for kidney damage",
    normalRange: "Below 30 mg/24 hours",
    priority: "required"
  }
];

export function getTestRecommendations(probability: number): TestResponse {
  if (probability < 0.3) {
    return {
      category: "LOW_RISK_TESTS",
      tests: baseTests
    };
  }

  if (probability < 0.7) {
    return {
      category: "MEDIUM_RISK_TESTS",
      tests: mediumRiskTests
    };
  }

  return {
    category: "HIGH_RISK_TESTS",
    tests: highRiskTests
  };
}