from pathlib import Path
import pandas as pd


def load_data_clean(file_path):
    """loads and cleans the data"""
    df = pd.read_csv(file_path)
    #our data includes unnescessary rows that we don't need
    df = df.drop(df[df['Label'] == 'Margin of Error'].index)
    df = df.drop(df[df['Label'] == 'Percent'].index)
    df = df.drop(df[df['Label'] == 'Percent Margin of Error'].index)
    # cleaning our data
    df.columns = df.columns.str.lower().str.strip()
    df.rename(columns={"label": "zipcode"}, inplace=True) #rename the column 'label' to 'zipcode'
    df["zipcode"] = df["zipcode"].str.extract(r'(\d{5})').dropna().astype(float)
    
    return df

def normalize(df):
    """uses the min - max formula to normalize the data """
    for column in df.columns[1:]:  # skip zipcode column
        min_value = df[column].min()
        max_value = df[column].max()
        # Avoid division by zero if min and max are the same
        df[column] = (df[column] - min_value) / (max_value - min_value)

    return df


def normalize_data(file_path):
    
    df = load_data_clean(file_path)
    columns_to_keep = [
        "zipcode", "unemployed", "walked", 
        "mean travel time to work (minutes)", "mean household income (dollars)", 
        "per capita income (dollars)", "employed with health insurance coverage"
    ]
    df = df[[col for col in columns_to_keep if col in df.columns]]
    df['zipcode'] = df['zipcode'].shift(1) #our zip vlues did match the required column due to the format of the data so we had to move the colmns down 1 step
    
    # List of Chicago ZIP codes (replace with actual list if needed)
    chicago_zipcodes = [
    60601, 60602, 60603, 60604, 60605, 60606, 60607, 60608, 60609, 60610, 60611, 
    60612, 60613, 60614, 60615, 60616, 60617, 60618, 60619, 60620, 60621, 60622, 
    60623, 60624, 60625, 60626, 60628, 60629, 60630, 60631, 60632, 60633, 60634, 
    60636, 60637, 60638, 60639, 60640, 60641, 60642, 60643, 60643, 60644, 60645, 
    60646, 60647, 60649, 60651, 60652, 60653, 60654, 60655, 60656, 60657, 60659, 
    60660, 60661, 60666, 60707, 60827
    ]

   
    # only keep chicago zip codes
    df = df[df['zipcode'].isin(chicago_zipcodes)]

    for column in df.columns[1:]:  # skip zipcode column 
        df[column] = df[column].astype(str).str.replace(',', '').astype(float)  #convert values to floats also as there were commas in our values, we had to take them out

    # normalize the data using our helper
    df_normalized = normalize(df)

    # for better readability, we have rounded off our values
    df_normalized = df_normalized.round(2)
    
    # export csv
    output_path = Path("./data/cleaned_data/cleaned_data_economic_infrastructure.csv")
    df_normalized.to_csv(output_path, index=False)
    
    print(("Processed data saved"))

def main(file_path):
    processed_data = normalize_data(file_path)
    return processed_data


file_path = Path("../data/raw_data/raw_data_eco_infra.csv")
zip_results = main(file_path)
# Save Results
print(f"Processing Complete. Results saved to {output_path}")


