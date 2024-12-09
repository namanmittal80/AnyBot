import json

def remove_duplicates(input_file, output_file):
    # Load the JSON file
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Use a dictionary to track unique URLs
    unique_data = {}
    for item in data:
        url = item["url"]
        if url not in unique_data:
            unique_data[url] = item

    # Convert dictionary values back to a list
    cleaned_data = list(unique_data.values())

    # Save the cleaned data to a new JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    print(f"Cleaned data saved to {output_file}")

# Example usage
input_file = "output.json"  # Input JSON file with duplicate URLs
output_file = "cleaned_output.json"  # Output file without duplicates
remove_duplicates(input_file, output_file)