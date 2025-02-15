import pandas as pd
import os

# Update these paths to match your setup
CSV_DIRECTORY = "c:/Users/timba/Downloads/archive/MedHack AI Hospital/csv"
# New output directory for Excel files
OUTPUT_DIRECTORY = "c:/Users/timba/Downloads/archive/MedHack AI Hospital/patient_reports"

def export_to_excel(patient_data, patient_id):
    """
    Export patient data to a multi-sheet Excel file.
    """
    if not patient_data:
        print("No data to export")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
        
    output_file = f"patient_{patient_id}_summary.xlsx"
    full_path = os.path.join(OUTPUT_DIRECTORY, output_file)
    
    with pd.ExcelWriter(full_path) as writer:
        for category, data in patient_data.items():
            if isinstance(data, pd.DataFrame):
                data.to_excel(writer, sheet_name=category[:31], index=False)
    
    print(f"\nData exported to: {full_path}")

# [Rest of the code remains the same...]

def get_patient_id_column(df):
    """
    Determine the patient ID column name in the dataframe.
    """
    possible_names = ['PATIENT', 'Id', 'patient_id', 'PATIENT_ID', 'PatientId', 'Patient']
    for col in possible_names:
        if col in df.columns:
            return col
    return None

def load_patient_data(patient_id):
    """
    Load and combine all data for a specific patient from multiple CSV files.
    """
    csv_files = {
        'demographics': 'patients.csv',
        'allergies': 'allergies.csv',
        'conditions': 'conditions.csv',
        'devices': 'devices.csv',
        'encounters': 'encounters.csv',
        'imaging': 'imaging.csv',
        'immunizations': 'immunizations.csv',
        'medications': 'medications.csv',
        'observations': 'observations.csv',
        'procedures': 'procedures.csv'
    }
    
    patient_data = {}
    
    for category, filename in csv_files.items():
        try:
            file_path = os.path.join(CSV_DIRECTORY, filename)
            df = pd.read_csv(file_path)
            
            id_column = get_patient_id_column(df)
            
            if id_column is None:
                print(f"Warning: Could not find patient ID column in {filename}")
                print(f"Available columns: {', '.join(df.columns)}")
                continue
                
            patient_records = df[df[id_column] == patient_id]
            
            if not patient_records.empty:
                patient_data[category] = patient_records
            
        except Exception as e:
            print(f"Error loading {filename}: {str(e)}")
    
    return patient_data

def display_patient_summary(patient_data):
    """
    Display a summary of all patient information.
    """
    print("\n=== Patient Summary ===\n")
    
    if not patient_data:
        print("No data found for this patient ID.")
        return
        
    for category, data in patient_data.items():
        print(f"\n--- {category.upper()} ---")
        if isinstance(data, pd.DataFrame):
            print(f"Number of records: {len(data)}")
            if len(data) > 5:
                print("\nFirst 5 records:")
                print(data.head())
                print(f"\n... and {len(data) - 5} more records")
            else:
                print(data)
        print("-" * 50)

def main():
    patient_id = input("Enter patient ID: ")
    patient_data = load_patient_data(patient_id)
    display_patient_summary(patient_data)
    
    # Auto-export without asking
    export_to_excel(patient_data, patient_id)

if __name__ == "__main__":
    main()