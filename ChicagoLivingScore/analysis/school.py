import pandas as pd
import numpy as np

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

# Main Execution
def main(file_path):
    df = load_data(file_path)
    df = map_categorical_values(df)
    zip_results = compute_zip_level_metrics(df)
    return zip_results

file_path = "milestones/milestone3/data_preprocess/Schools/Chicago_Public_Schools_2024.csv"
zip_results = main(file_path)
# Save Results
zip_results.to_csv("zip_code_education_results.csv")
print("Processing Complete. Results saved to 'zip_code_education_results.csv'")
