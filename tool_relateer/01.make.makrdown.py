#!/usr/bin/env python3
"""
Script to read data from a CSV file and create markdown files for the first 500 items.
Each markdown file will be named with the date and title, and will contain the CSV line.
"""

import csv
import os
import re
from datetime import datetime
from pathlib import Path

# Constants
CSV_FILE_PATH = "data/dutch-news-articles.csv"
OUTPUT_DIR = "news-items"
MAX_ITEMS = 500

def sanitize_filename(title):
    """
    Sanitize the title to be used as part of a filename.
    Remove invalid characters and limit length.
    """
    # Remove invalid filename characters
    sanitized = re.sub(r'[\\/*?:"<>|]', "", title)
    # Replace spaces and other separators with hyphens
    sanitized = re.sub(r'[\s,;]+', "-", sanitized)
    # Limit length to avoid excessively long filenames
    return sanitized[:100]

def main():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Counter for processed items
    count = 0
    
    print(f"Reading CSV file: {CSV_FILE_PATH}")
    print(f"Creating markdown files in: {OUTPUT_DIR}")
    
    with open(CSV_FILE_PATH, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        # Read header row
        header = next(csv_reader)
        
        # Process rows
        for row in csv_reader:
            if count >= MAX_ITEMS:
                break
                
            try:
                # Extract date and title
                date_str = row[0].split()[0]  # Get just the date part (YYYY-MM-DD)
                title = row[1]
                
                # Format date for filename (YYYYmmdd)
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                date_formatted = date_obj.strftime("%Y%m%d")
                
                # Create filename
                sanitized_title = sanitize_filename(title)
                filename = f"{date_formatted}.{sanitized_title}.md"
                file_path = os.path.join(OUTPUT_DIR, filename)
                
                # Create content (the whole CSV line)
                content = ",".join(row)
                
                # Write to markdown file
                with open(file_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(content)
                
                count += 1
                if count % 50 == 0:
                    print(f"Created {count} markdown files...")
                    
            except Exception as e:
                print(f"Error processing row: {e}")
                continue
    
    print(f"Completed! Created {count} markdown files in {OUTPUT_DIR}")

if __name__ == "__main__":
    main() 