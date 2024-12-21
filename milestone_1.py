import requests
import pandas as pd
import json
import os
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt

# Function to fetch data from an API
def fetch_api_data(api_url, query_params):
    try:
        response = requests.get(api_url, params=query_params)
        response.raise_for_status()
        return response.json()  # Return JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching API data: {e}")
        return None

# Function to read data from a Google Forms CSV export
def read_google_forms_data(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path)
        return df
    except FileNotFoundError as e:
        print(f"Error reading Google Forms CSV: {e}")
        return None

# Function to read data from an Excel file
def read_excel_data(excel_file_path):
    try:
        df = pd.read_excel(excel_file_path)
        return df
    except FileNotFoundError as e:
        print(f"Error reading Excel file: {e}")
        return None

# Save combined data to a JSON file
def save_to_json_file(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {os.path.abspath(file_name)}")

# Function to process and visualize API data
def process_and_visualize_api_data(api_data):
    if "articles" in api_data:
        print("\nNumber of articles fetched:", len(api_data["articles"]))

        # Extract Titles of Articles
        print("\n1. Article Titles:")
        titles = [article.get("title", "No title") for article in api_data["articles"]]
        for title in titles[:5]:
            print(title)  # Display first 5 titles

        # Filter Articles Published After January 1, 2023
        print("\n2. Filter Articles Published After January 1, 2023:")
        date_threshold = datetime(2023, 1, 1)
        filtered_articles = [
            article for article in api_data["articles"]
            if datetime.strptime(article["date"], "%Y-%m-%dT%H:%M:%SZ") > date_threshold
        ]
        print(f"Number of articles after January 1, 2023: {len(filtered_articles)}")

        # Count Articles by Source
        print("\n3. Article Count by Source:")
        sources = [article.get("source", "Unknown source") for article in api_data["articles"]]
        source_counts = Counter(sources)
        for source, count in source_counts.items():
            print(f"{source}: {count}")

        # Visualize Article Count by Source
        print("\nVisualizing Article Count by Source:")
        plt.bar(source_counts.keys(), source_counts.values())
        plt.xlabel('Source')
        plt.ylabel('Number of Articles')
        plt.title('Article Distribution by Source')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

# Example usage
if __name__ == "__main__":
    # API configurations
    api_url = "https://eventregistry.org/api/v1/article/getArticles"
    query_params = {
        "q": "supply chain OR logistics OR geopolitics",
        "from": "2023-01-01",
        "to": "2024-12-12",
        "lang": "en",
        "pageSize": 100,
        "apiKey": "your_api_key"
    }

    print("Fetching API data...")
    api_data = fetch_api_data(api_url, query_params)

    # Process and visualize API data
    if api_data:
        process_and_visualize_api_data(api_data)

    # Read Google Forms data (replace with the actual file path)
    google_forms_file = "google_forms_data.csv"
    print("\nReading Google Forms data...")
    forms_data = read_google_forms_data(google_forms_file)

    # Read Excel data (replace with the actual file path)
    excel_file = "excel_data.xlsx"
    print("\nReading Excel data...")
    excel_data = read_excel_data(excel_file)

    # Combine all data into a dictionary
    combined_data = {
        "api_data": api_data,
        "google_forms_data": forms_data.to_dict(orient="records") if forms_data is not None else None,
        "excel_data": excel_data.to_dict(orient="records") if excel_data is not None else None
    }

    # Save combined data to a JSON file
    output_file = "combined_data.json"
    save_to_json_file(combined_data, output_file)
