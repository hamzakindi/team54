using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

public class DiabetesTestData
{
    public int Pregnancies { get; set; }
    public double Glucose { get; set; }
    public double BloodPressure { get; set; }
    public double SkinThickness { get; set; }
    public double Insulin { get; set; }
    public double BMI { get; set; }
    public double DiabetesPedigreeFunction { get; set; }
    public int Age { get; set; }
}

public class ApiTest
{
    private static readonly HttpClient client = new HttpClient();
    private static readonly string[] urls = new[]
    {
        "http://localhost:3000/api/predict",
        "http://localhost:8000/predict"
    };

    public static async Task TestPrediction(DiabetesTestData data, string testName)
    {
        foreach (var url in urls)
        {
            try
            {
                var content = new StringContent(
                    JsonSerializer.Serialize(data),
                    Encoding.UTF8,
                    "application/json"
                );

                var response = await client.PostAsync(url, content);
                var responseBody = await response.Content.ReadAsStringAsync();

                Console.WriteLine($"\n=== {testName} ===");
                Console.WriteLine($"URL: {url}");
                Console.WriteLine($"Request: {JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true })}");
                Console.WriteLine($"Response Status: {(int)response.StatusCode}");
                Console.WriteLine($"Response: {responseBody}");
                return;
            }
            catch (Exception ex)
            {
                continue;
            }
        }
        Console.WriteLine($"\nError: Could not connect to any server for {testName}");
    }

    public static async Task Main()
    {
        var highRiskCase = new DiabetesTestData
        {
            Pregnancies = 6,
            Glucose = 195,
            BloodPressure = 130,
            SkinThickness = 40,
            Insulin = 180,
            BMI = 37.2,
            DiabetesPedigreeFunction = 0.6,
            Age = 45
        };

        var lowRiskCase = new DiabetesTestData
        {
            Pregnancies = 1,
            Glucose = 85,
            BloodPressure = 66,
            SkinThickness = 29,
            Insulin = 100,
            BMI = 23.5,
            DiabetesPedigreeFunction = 0.351,
            Age = 31
        };

        var minimumValuesCase = new DiabetesTestData
        {
            Pregnancies = 0,
            Glucose = 0,
            BloodPressure = 0,
            SkinThickness = 0,
            Insulin = 0,
            BMI = 0,
            DiabetesPedigreeFunction = 0,
            Age = 0
        };

        var customValuesCase = new DiabetesTestData
        {
            Pregnancies = 5,
            Glucose = 117,
            BloodPressure = 92,
            SkinThickness = 0,
            Insulin = 0,
            BMI = 34.1,
            DiabetesPedigreeFunction = 0.337,
            Age = 38
        };

        var datasetValuesCase = new DiabetesTestData
        {
            Pregnancies = 10,
            Glucose = 125,
            BloodPressure = 70,
            SkinThickness = 26,
            Insulin = 115,
            BMI = 31.1,
            DiabetesPedigreeFunction = 0.205,
            Age = 41
        };

        var negativeCase = new DiabetesTestData
        {
            Pregnancies = 3,
            Glucose = 126,
            BloodPressure = 88,
            SkinThickness = 41,
            Insulin = 235,
            BMI = 39.3,
            DiabetesPedigreeFunction = 0.704,
            Age = 27
        };

        var positiveCase = new DiabetesTestData
        {
            Pregnancies = 7,
            Glucose = 196,
            BloodPressure = 90,
            SkinThickness = 0,
            Insulin = 0,
            BMI = 39.8,
            DiabetesPedigreeFunction = 0.451,
            Age = 41
        };

        await TestPrediction(highRiskCase, "High Risk Case");
        await TestPrediction(lowRiskCase, "Low Risk Case");
        await TestPrediction(minimumValuesCase, "Minimum Values Case");
        await TestPrediction(customValuesCase, "Custom Values Case");
        await TestPrediction(datasetValuesCase, "Dataset Values Case");
        await TestPrediction(negativeCase, "Negative Case");
        await TestPrediction(positiveCase, "Positive Case");
    }
}