# This file takes the third person moral machine dataset and extract types of scenrios that are relevant to our analysis
import tarfile
import csv
from io import StringIO

 
# Path to the .csv.tar.gz data file
file_path = "moral_perspective/third-person/SharedResponses.csv.tar.gz"

# We consider gender, age and random scenarios
filtered_rows_Random = []
filtered_rows_G_A = []


# Extract based on scenarios
with tarfile.open(file_path, "r") as tar:
    # Extract the .csv file
    csv_filename = tar.getnames()[0]  # Assuming there's only one file in the archive
    print(csv_filename)
    csv_file = tar.extractfile(csv_filename)
        
    # Decode the binary content to string (assuming UTF-8 encoding)
    csv_content = csv_file.read().decode('utf-8')
    print('content')

    # Create a file-like object from the decoded content
    csv_data = StringIO(csv_content)
    print('data')
        
    # Decompress the file-like object
            # Read CSV using DictReader
    csv_reader = csv.DictReader(csv_data)
    for row in csv_reader:
                # Check if the row satisfies the condition
        if row.get("ScenarioTypeStrict") == "Random" and row.get("ScenarioType") == "Random":
                    # If the condition is satisfied, add the row to the list
            filtered_rows_Random.append(row)
        if row.get("ScenarioTypeStrict") in {"Gender", "Age"} and row.get("ScenarioType") in {"Gender", "Age"}:
                    # If the condition is satisfied, add the row to the list
            filtered_rows_G_A.append(row)


print(len(filtered_rows_Random)) # 5541286
print(len(filtered_rows_G_A))


# Store the output to new csv
output_file = "moral_perspective/third-person/scenario_random.csv"

fieldnames = filtered_rows_Random[0].keys()

# Open the output CSV file in write mode
with open(output_file, "w", newline="") as f:
    # Create a DictWriter object with the fieldnames and specify the delimiter
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write each dictionary as a row in the CSV file
    for row in filtered_rows_Random:
        writer.writerow(row)



output_file_1 = "moral_perspective/third-person/scenario_gender_age.csv"

fieldnames = filtered_rows_G_A[0].keys()

# Open the output CSV file in write mode
with open(output_file_1, "w", newline="") as f:
    # Create a DictWriter object with the fieldnames and specify the delimiter
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write each dictionary as a row in the CSV file
    for row in filtered_rows_G_A:
        writer.writerow(row)



