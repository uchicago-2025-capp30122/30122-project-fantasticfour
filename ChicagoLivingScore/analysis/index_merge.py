import pandas as pd
import pathlib

class FinalScoreCalculator:
    def __init__(self):
        self.base_dir = pathlib.Path(__file__).parent.parent
        
        # Input file path
        self.housing_file = self.base_dir / "data" / "cleaned_data" / "cleaned_data_housing.csv"
        self.econ_file = self.base_dir / "data" / "cleaned_data" / "cleaned_data_econ_infrastructure.csv"
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

    def merge_data(self):
        """    
        final_score = 0.21 * housing 
                    + 0.12 * Unemployed 
                    + 0.10 * Mean travel time to work (minutes) 
                    + 0.10 * Mean household income (dollars) 
                    + 0.04 * Employed and With private health insurance 
                    + 0.14 * education 
                    + 0.17 * crime 
                    + 0.12 * environment
        """
        # Read and normalize each CSV file
        df_housing = self.read_and_normalize(self.housing_file)
        df_econ = self.read_and_normalize(self.econ_file)
        df_edu = self.read_and_normalize(self.education_file)
        df_crime = self.read_and_normalize(self.crime_file)
        df_env = self.read_and_normalize(self.environment_file)
        

        # Housing data metrics
        df_housing = df_housing[['zipcode', 'norm_avg_price_per_sqft']].rename(
            columns={'norm_avg_price_per_sqft': 'housing_score'}
        )
        # Econ and infra metrics
        df_econ = df_econ[['zipcode', 'Unemployed', 'Mean travel time to work (minutes)', 
                           'Mean household income (dollars)', 'Employed and With private health insurance']]
        # Rename for clarification
        df_econ = df_econ.rename(columns={
            'Unemployed': 'unemployed_score',
            'Mean travel time to work (minutes)': 'commute_time_score',
            'Mean household income (dollars)': 'avg_income_score',
            'Employed and With private health insurance': 'private_insurance_score'
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
        
        # Merge all data on zipcode 
        df_merge = df_housing.merge(df_econ, on="zipcode", how="outer") \
                             .merge(df_edu, on="zipcode", how="outer") \
                             .merge(df_crime, on="zipcode", how="outer") \
                             .merge(df_env, on="zipcode", how="outer")
        
        # Fill any missing values with 0
        df_merge.fillna(0, inplace=True)
        
        # Calculate the economic part score
        df_merge["econ_score"] = (0.12 * df_merge["unemployed_score"] +
                                  0.10 * df_merge["commute_time_score"] +
                                  0.10 * df_merge["avg_income_score"] +
                                  0.04 * df_merge["private_insurance_score"])
        
        # Compute the final living score using the given weights:
        # housing: 21%, econ_score: 36%, education: 14%, crime: 17%, environment: 12%
        df_merge["final_score"] = (0.21 * df_merge["housing_score"] +
                                   0.36 * df_merge["econ_score"] +
                                   0.14 * df_merge["education_score"] +
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
