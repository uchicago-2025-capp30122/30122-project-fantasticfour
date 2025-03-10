import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)
import json
import os
import pathlib
import pandas as pd
import numpy as np

# This file aims at cleaning housing data from Zillow
# Transform raw datasets 
# Normalize dataset by Min-Max normalization
# Generate new metrics "average housing price per sqft group by zip code"


class HousingDataProcessor:
    def __init__(self):
        pass
    
    # Convert raw JSON data to a CSV file
    def convert_json_to_csv(self, json_path, csv_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        properties = []
        for home in data:
            home_info = home.get("hdpData", {}).get("homeInfo", {})
            property_data = {
                "zpid": home.get("zpid"),
                "streetAddress": home_info.get("streetAddress"),
                "city": home_info.get("city"),
                "state": home_info.get("state"),
                "zipcode": home_info.get("zipcode"),
                "latitude": home_info.get("latitude"),
                "longitude": home_info.get("longitude"),
                "price": home_info.get("price"),
                "bathrooms": home_info.get("bathrooms"),
                "bedrooms": home_info.get("bedrooms"),
                "livingArea": home_info.get("livingArea"),
                "homeType": home_info.get("homeType")
            }
            properties.append(property_data)

        df = pd.DataFrame(properties)
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"CSV file has been converted：{csv_path}")
        return df

    def process_housing_data(self, input_csv, output_csv):
        """
        1. Process missing values in livingArea: fill missing with 0,
           then replace 0 with the global median.
        2. In order to deal with the imbalanced dataset, oversample the data so that each zipcode has at least min_count samples.
        3. Calculate price per sqft and average price per sqft per zipcode.
        4. Keep only zipcode and avg_price_per_sqft, round to 2 decimals, and
           normalize using min-max scaling (inverted so that higher cost gets a lower score).
        5. Save the final DataFrame to a CSV file.
        """
        df = pd.read_csv(input_csv)

        # Process livingArea: convert to numeric, fill missing with 0,
        # and replace 0 with the global median (of non-zero values)
        df['livingArea'] = pd.to_numeric(df['livingArea'], errors='coerce')
        df['livingArea'] = df['livingArea'].fillna(0)
        median = df.loc[df['livingArea'] != 0, 'livingArea'].median()
        df['livingArea'] = df['livingArea'].replace(0, median)

        # Oversample: ensure each zipcode has at least min_count samples
        min_count = 50  # Set up the threshold
        oversampled_data = []
        zip_counts = df['zipcode'].value_counts()


        for zc, count in zip_counts.items():
            df_zc = df[df['zipcode'] == zc]
            if count < min_count:
                # Sample with replacement if there are too few samples
                df_zc_oversampled = df_zc.sample(n=min_count, replace=True, random_state=42)
                oversampled_data.append(df_zc_oversampled)
            else:
                oversampled_data.append(df_zc)

        df_oversampled = pd.concat(oversampled_data, ignore_index=True)

        # Calculate price per sqft for each record
        # Compute average price per sqft per zipcode
        df_oversampled['price_per_sqft'] = df_oversampled['price'] / df_oversampled['livingArea']
        df_oversampled['avg_price_per_sqft'] = df_oversampled.groupby('zipcode')['price_per_sqft'].transform('mean')

        # Keep only zipcode and average price per sqft
        df_final = df_oversampled[['zipcode', 'avg_price_per_sqft']].drop_duplicates().reset_index(drop=True)
        df_final['avg_price_per_sqft'] = df_final['avg_price_per_sqft'].round(2)

        # Min-Max normalization (inverted) for avg_price_per_sqft
        min_val = df_final['avg_price_per_sqft'].min()
        max_val = df_final['avg_price_per_sqft'].max()

        if max_val - min_val != 0:
            df_final['norm_avg_price_per_sqft'] = 1 - ((df_final['avg_price_per_sqft'] - min_val) / (max_val - min_val))
        else:
            df_final['norm_avg_price_per_sqft'] = 1

        df_final['norm_avg_price_per_sqft'] = df_final['norm_avg_price_per_sqft'].round(2)
        
        df_final.to_csv(output_csv, index=False)
        print(f"Processed data saved to: {output_csv}")
        return df_final


if __name__ == '__main__':
    base_dir = pathlib.Path(__file__).parent

    processor = HousingDataProcessor()

    input_csv = base_dir.parent / "data" / "raw_data/raw_zillow_data" / "Housing_Data.csv"
    final_csv = base_dir.parent / "data" / "cleaned_data" / "Housing_Data_Final.csv"

    processor.process_housing_data(input_csv, final_csv)
