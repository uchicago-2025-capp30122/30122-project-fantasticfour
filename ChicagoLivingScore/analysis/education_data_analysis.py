import pandas as pd
import numpy as np
from pathlib import Path
import geopandas as gpd

def load_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.lower().str.strip() 
    df["zip_code"] = df["zip"].astype(str).str.lower().str.strip() 
    return df

def standardize_column(series):
    min_val = series.min()
    max_val = series.max()
    if min_val == max_val:  # Avoid division by zero
        return series.apply(lambda x: 1 if x == max_val else 0)
    return (series - min_val) / (max_val - min_val)

def map_categorical_values(df):
    mapping_creative = {
        "excelling": 4, "strong": 3, "developing": 2, "emerging": 1, 
        "incomplete data": 0, np.nan: 0
    }
    
    mapping_family = mapping_leadership = {
        "very strong": 4, "strong": 3, "neutral": 2, "weak": 1, 
        "very weak": 0, "not enough data": 0, np.nan: 0
    }
    
    mapping_culture = {
        "well organized": 4, "organized": 3, "moderately organized": 2, 
        "partially organized": 1, "not yet organized": 0, np.nan: 0
    }

    df["creative_school_certification"] = df["creative_school_certification"].str.lower().map(mapping_creative)
    df["school_survey_involved_families"] = df["school_survey_involved_families"].str.lower().map(mapping_family)
    df["school_survey_effective_leaders"] = df["school_survey_effective_leaders"].str.lower().map(mapping_leadership)
    df["culture_climate_rating"] = df["culture_climate_rating"].str.lower().map(mapping_culture)

    return df

def compute_zip_level_metrics(df):
    zip_group = df.groupby("zip_code")

    # SAT Score Aggregation
    sat_scores = zip_group["sat_grade_11_score_school_avg"].mean()
    min_sat = sat_scores.min()
    sat_scores.fillna(min_sat, inplace=True)

    # Standardize SAT Scores
    sat_scores = standardize_column(sat_scores)
    sat_scores = pd.Series(sat_scores, index=zip_group.groups.keys(), name="academic_results")

    # Other Metrics Aggregation
    categories = [
        "creative_school_certification",
        "school_survey_involved_families",
        "school_survey_effective_leaders",
        "culture_climate_rating"
    ]

    other_scores = zip_group[categories].mean()
    student_attendance = zip_group[["student_attendance_year_1_pct", "student_attendance_year_2_pct"]].mean().mean(axis=1)

    # Standardize all non-SAT variables
    for col in other_scores.columns:
        other_scores[col] = standardize_column(other_scores[col])

    student_attendance = standardize_column(student_attendance)
    student_attendance = pd.Series(student_attendance, index=zip_group.groups.keys(), name="student_attendance")

    # Compute Non-Academic Score
    non_academic_score = other_scores.mean(axis=1)
    non_academic_score = standardize_column(non_academic_score)
    non_academic_score = pd.Series(non_academic_score, index=zip_group.groups.keys(), name="non_academic_education_score")

    # Compute Final Score
    final_score = 0.5 * sat_scores + 0.5 * non_academic_score
    final_score = pd.Series(final_score, index=zip_group.groups.keys(), name="final_score_per_zip")

    # Combine All Results
    zip_results = pd.concat([sat_scores, other_scores, student_attendance, non_academic_score, final_score], axis=1)

    return zip_results


def find_nearest_values(zip_code):
    step = 1
    found_values = {col: None for col in info_zip_codes.columns if col != zip_col}

    while step < len(all_zip_codes):
        lower_zip = zip_code - step
        upper_zip = zip_code + step

        if lower_zip in zip_info_dict:
            for col in found_values.keys():
                if found_values[col] is None:
                    found_values[col] = zip_info_dict[lower_zip][col]

        if upper_zip in zip_info_dict:
            for col in found_values.keys():
                if found_values[col] is None:
                    found_values[col] = zip_info_dict[upper_zip][col]

        if all(value is not None for value in found_values.values()):
            break

        step += 1

    return pd.Series(found_values)

# Main Execution
def main(file_path):
    df = load_data(file_path)
    df = map_categorical_values(df)
    zip_results = compute_zip_level_metrics(df)
    return zip_results

if __name__ == '__main__':
    BASE_DIR = Path(__file__).parent.parent
    file_path = BASE_DIR / "data" / "raw_data"/  "Chicago_Public_Schools_2024.csv"
    zip_results = main(file_path)
    zip_results.reset_index(inplace=True)
    zip_results.rename(columns={"index": "zip_code"}, inplace=True)
    zip_results.to_csv("./data/cleaned_data/cleaned_data_education.csv", index=False)
    all_zip_codes = pd.read_csv("./data/cleaned_data/chicago_zip.csv")
    info_zip_codes = pd.read_csv("./data/cleaned_data/cleaned_data_education.csv")
    zip_col = "zip_code"
    all_zip_codes[zip_col] = all_zip_codes[zip_col].astype(int)
    info_zip_codes[zip_col] = info_zip_codes[zip_col].astype(int)

    all_zip_codes = all_zip_codes.sort_values(by=zip_col).reset_index(drop=True)
    zip_info_dict = info_zip_codes.set_index(zip_col).to_dict(orient="index")

    missing_zips = all_zip_codes[~all_zip_codes[zip_col].isin(info_zip_codes[zip_col])]
    missing_values_df = missing_zips[zip_col].apply(find_nearest_values)
    missing_zips = pd.concat([missing_zips, missing_values_df], axis=1)
    final_data = pd.concat([info_zip_codes, missing_zips], ignore_index=True)
    final_data = final_data.sort_values(by=zip_col).reset_index(drop=True)

    final_data.to_csv("./data/cleaned_data/cleaned_data_education.csv", index=False)
    # generate a education csv file that has locations of schools 
    BASE_DIR = Path(__file__).parent.parent
    INPUT_FILE = BASE_DIR / "data" / "raw_data" / "education.csv"
    OUTPUT_FILE = BASE_DIR / "data" / "cleaned_data"/"cleaned_education.csv"

    original_df = gpd.read_file(INPUT_FILE)
    gdf_edu = gpd.GeoDataFrame(original_df[['School_ID', 'Short_Name', 'Long_Name', 'School_Type','School_Latitude','School_Longitude','Website',"Creative_School_Certification"]]) # use variables we need
    gdf_edu.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
