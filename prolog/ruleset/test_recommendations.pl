% filepath: /c:/RnD/MedHack/team54/prolog/test_recommendations.pl

% Test definition structure
% test(Name, Description, NormalRange, Priority).

% Base tests
base_test(fasting_blood_glucose, 'Measures blood sugar levels after fasting for 8 hours', '70-99 mg/dL', required).
base_test(hba1c, 'Reflects average blood glucose over past 2-3 months', 'Below 5.7%', required).

% Medium risk additional tests
medium_risk_test(ogtt, 'Measures how well your body processes glucose', 'Below 140 mg/dL after 2 hours', required).
medium_risk_test(fasting_insulin, 'Measures insulin resistance', '3-25 mIU/L', recommended).
medium_risk_test(lipid_profile, 'Measures different types of cholesterol', 'Varies by component', recommended).

% High risk additional tests
high_risk_test(c_peptide, 'Measures insulin production by pancreas', '0.5-2.0 ng/mL', required).
high_risk_test(gad_antibodies, 'Helps distinguish between type 1 and type 2 diabetes', 'Below 5 IU/mL', recommended).
high_risk_test(microalbuminuria, 'Checks for kidney damage', 'Below 30 mg/24 hours', required).

% Rules to get recommendations based on probability
get_test_recommendations(Probability, Category, Tests) :-
    Probability < 0.3,
    Category = 'LOW_RISK_TESTS',
    findall([Name, Desc, Range, Priority], 
            base_test(Name, Desc, Range, Priority), 
            Tests).

get_test_recommendations(Probability, Category, Tests) :-
    Probability >= 0.3,
    Probability < 0.7,
    Category = 'MEDIUM_RISK_TESTS',
    findall([Name, Desc, Range, Priority],
            (base_test(Name, Desc, Range, Priority);
             medium_risk_test(Name, Desc, Range, Priority)),
            Tests).

get_test_recommendations(Probability, Category, Tests) :-
    Probability >= 0.7,
    Category = 'HIGH_RISK_TESTS',
    findall([Name, Desc, Range, Priority],
            (base_test(Name, Desc, Range, Priority);
             medium_risk_test(Name, Desc, Range, Priority);
             high_risk_test(Name, Desc, Range, Priority)),
            Tests).