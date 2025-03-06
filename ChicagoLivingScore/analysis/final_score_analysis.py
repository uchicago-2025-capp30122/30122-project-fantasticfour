import pandas as pd
import pathlib

class FinalScoreCalculator:
    def __init__(self):
        self.base_dir = pathlib.Path(__file__).parent.parent
        
        # Input file path
        self.zip_list_file = self.base_dir / "data" / "cleaned_data" / "chicago_zip.csv"
        self.housing_file = self.base_dir / "data" / "cleaned_data" / "cleaned_data_housing.csv"
        self.econ_file = self.base_dir / "data" / "cleaned_data" / "cleaned_data_economic_infrastructure.csv"
        self.education_file = self.base_dir / "data" / "cleaned_data" / "cleaned_data_education.csv"
        self.crime_file = self.base_dir / "data" / "cleaned_data" / "cleaned_data_crime.csv"
        self.environment_file = self.base_dir / "data" / "cleaned_data" / "cleaned_data_environment.csv"
        
        # Output file path
        self.output_file = self.base_dir / "data" / "cleaned_data" / "final_living_score.csv"

    def normalize_zip(self, zipcode):
        # Convert the zipcode to a string and remove any trailing '.0'
        return str(zipcode).split('.')[0]

    def read_and_normalize(self, file_path, zip_col="zipcode"):
        df = pd.read_csv(file_path)
        df[zip_col] = df[zip_col].apply(self.normalize_zip)
        return df
    

    def impute_by_nearest(self, df, col):
        df = df.copy()
        df['zip_int'] = df['zipcode'].astype(int)
        
        missing_idx = df[df[col].isnull()].index
        
        for idx in missing_idx:
            current_zip = df.loc[idx, 'zip_int']
            valid = df[df[col].notnull()]
            if valid.empty:
                continue  
            valid = valid.assign(distance=(valid['zip_int'] - current_zip).abs())
            nearest = valid.nsmallest(4, 'distance')

            mean_val = nearest[col].mean()
            df.loc[idx, col] = mean_val
        
       
        df.drop(columns=['zip_int'], inplace=True)
        return df

    def merge_data(self):
        """    
        final_score = 
                    0.17 * Unemployed 
                    + 0.17 * Mean travel time to work (minutes) 
                    + 0.19 * Mean household income (dollars) 
                    + 0.03 * Employed and With private health insurance 
                    + 0.15 * education 
                    + 0.17 * crime 
                    + 0.12 * environment
        """

        df_zip = self.read_and_normalize(self.zip_list_file)
        df_zip = df_zip[['zipcode']]

        # Read and normalize each CSV file
        df_housing = self.read_and_normalize(self.housing_file)
        df_econ = self.read_and_normalize(self.econ_file)
        df_edu = self.read_and_normalize(self.education_file)
        df_crime = self.read_and_normalize(self.crime_file)
        df_env = self.read_and_normalize(self.environment_file)
        

        # Housing data metrics
        df_housing = df_housing[['zipcode', 'avg_price_per_sqft']].rename(
            columns={'avg_price_per_sqft': 'avg_price_per_sqft'}
        )
        # Econ and infra metrics
        df_econ = df_econ[['zipcode', 'unemployed', 'mean travel time to work (minutes)', 
                           'mean household income (dollars)', 'employed with health insurance coverage']]
        # Rename for clarification
        df_econ = df_econ.rename(columns={
            'unemployed': 'unemployed_score',
            'mean travel time to work (minutes)': 'commute_time_score',
            'mean household income (dollars)': 'avg_income_score',
            'employed with health insurance coverage': 'private_insurance_score'
        })
        
        # Education data metrics
        df_edu = df_edu[['zipcode', 'final_score_per_zip']].rename(
            columns={'final_score_per_zip': 'education_score'}
        )
        
        # Crime data metrics
        df_crime = df_crime[['zipcode', 'crime_score']].rename(
            columns={'crime_score': 'crime_score'}
        )
        
        # Environment data metrics
        df_env = df_env[['zipcode', 'environment_score']].rename(
            columns={'environment_score': 'environment_score'}
        )
        
        # Merge all datasets on zipcode 
        df_merge = df_zip.merge(df_housing, on="zipcode", how="left") \
                             .merge(df_econ, on="zipcode", how="left") \
                             .merge(df_edu, on="zipcode", how="left") \
                             .merge(df_crime, on="zipcode", how="left") \
                             .merge(df_env, on="zipcode", how="left")
        
        cols_to_impute = ['avg_price_per_sqft', 'unemployed_score', 'commute_time_score', 
                          'avg_income_score', 'private_insurance_score', 'education_score', 
                          'crime_score', 'environment_score']
        
        for col in cols_to_impute:
            df_merge = self.impute_by_nearest(df_merge, col)
    
        
        # Compute the final living score using the given weights:
        df_merge["final_score"] = (0.17 * df_merge["unemployed_score"] +
                                   0.17 * df_merge["commute_time_score"] +
                                   0.19 * df_merge["avg_income_score"] +
                                   0.03 * df_merge["private_insurance_score"] +
                                   0.15 * df_merge["education_score"] +
                                   0.17 * df_merge["crime_score"] +
                                   0.12 * df_merge["environment_score"]).round(2)
        
        return df_merge

    def save_final_score(self):
 
        df_final = self.merge_data()
        output_path = self.output_file
        df_final.to_csv(output_path, index=False)
        print(f"Final living score data saved")
        return df_final


if __name__ == "__main__":
    calc = FinalScoreCalculator()
    calc.save_final_score()
