"""
This module handles saving image captions to a CSV file.
It contains a function to save a list of captions along with their corresponding image URLs.
"""

import csv

def save_captions_to_csv(captions, filename="captions.csv"):
    """
    Save the list of captions to a CSV file.
    """
    try:
        with open(filename, "w", newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Image URL", "Caption"])
            writer.writerows(captions)
        return filename
    except Exception as e:
        print(f"Error saving captions to CSV: {e}")
        return None
