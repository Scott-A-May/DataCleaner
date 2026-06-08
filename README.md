# Automated Data Cleaner

Cleans and standardizes messy CSV data and outputs a formatted multi-tab Excel workbook with a full audit trail.

## Overview

This tool accepts a messy CSV file, applies a series of standardization and cleaning steps, and produces a formatted Excel workbook with three tabs: cleaned data, a log of every change made, and a summary statistics report.

## Features

- Standardizes column names (lowercase, underscores, trimmed whitespace)
- Trims leading/trailing whitespace from all text cells
- Standardizes text casing (Title Case) for name and state fields
- Removes exact duplicate rows
- Converts numbers stored as text to numeric format
- Fills missing numeric values with column median
- Fills missing text values with "Unknown"
- Outputs a three-tab Excel workbook:
  - **Cleaned Data** — the cleaned dataset
  - **Changes Made** — row-level audit trail of every change
  - **Summary Stats** — run date, row counts, and total issues fixed

## Project Structure

DataCleaner/
├── data_cleaner.py       # Main cleaning script
├── create_test_data.py   # Generates sample messy CSV for testing
├── messy_data.csv        # Sample input file
├── cleaned_data.xlsx     # Sample output file
└── requirements.txt      # Python dependencies

## Technologies Used

- Python 3.14
- pandas
- openpyxl
- numpy

## Setup

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Place your CSV file in the project folder and update this line in `data_cleaner.py`:  INPUT_FILE = "your_file.csv"
4. Run the script:  python data_cleaner.py

5. Open `cleaned_data.xlsx` to review results

## Notes

- Numeric nulls are filled with the column median
- Non-numeric values in numeric columns are coerced to NaN before filling
- Text nulls are filled with "Unknown"
- The script currently standardizes casing for `first_name`, `last_name`, and `state` columns — update the `text_columns` list in the script to match your dataset

## Author

Scott A. May | [GitHub](https://github.com/Scott-A-May)
   
