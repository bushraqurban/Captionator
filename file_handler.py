import csv

def save_captions_to_csv(captions, filename="captions.csv"):
    """
    Save the list of captions to a CSV file.
    """
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Image URL", "Caption"])
            writer.writerows(captions)
        return filename
    except Exception as e:
        print(f"Error saving captions to CSV: {e}")
        return None
