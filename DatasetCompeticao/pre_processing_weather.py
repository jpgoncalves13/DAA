from datetime import datetime

# Read the file
file_path = 'datasets/open_meteo.csv'  # Replace 'data.txt' with your file path
output_file_path = 'datasets/radiation_data.csv'  # Replace 'updated_data.txt' with your desired output file path

with open(file_path, 'r') as file:
    lines = file.readlines()

updated_data = []

# Convert date format and store updated data
for line in lines:
    data = line.strip().split(',')
    original_date = None
    try:
        original_date = datetime.strptime(data[0], "%Y-%m-%dT%H:%M")
    except ValueError:
        continue
    updated_date_str = original_date.strftime("%Y-%m-%d %H:00:00 +0000 UTC")
    updated_data.append(f"{updated_date_str},{','.join(data[1:])}\n")

# Write updated data to a new file
with open(output_file_path, 'w') as output_file:
    output_file.writelines(updated_data)

print("Data updated and saved to 'updated_data.txt'.")