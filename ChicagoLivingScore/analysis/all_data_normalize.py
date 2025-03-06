import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd
import pathlib

class DataNormalizer:
    def __init__(self):
        self.base_dir = pathlib.Path(__file__).parent.parent
        self.env_file = self.base_dir / "data" / "cleaned_data" / "cleaned_data_environment.csv"
        self.crime_file = self.base_dir / "data" / "cleaned_data" / "cleaned_data_crime.csv"
        self.econ_file = self.base_dir / "data" / "cleaned_data" / "cleaned_data_economic_infrastructure.csv"
    
    def min_max_normalize(self, series, invert=False):
        min_val = series.min()
        max_val = series.max()
        if max_val - min_val != 0:
            normalized = (series - min_val) / (max_val - min_val)
        else:
            normalized = series * 0  
        return 1 - normalized if invert else normalized

    def process_environment(self):

        df_env = pd.read_csv(self.env_file)
        df_env["environment_score"] = self.min_max_normalize(df_env["count"], invert=True)
        output_path = self.base_dir / "data" / "cleaned_data" / "cleaned_data_environment.csv"
        df_env.to_csv(output_path, index=False)
        print(f"Environment data processed and saved")
        return df_env

    def process_crime(self):

        df_crime = pd.read_csv(self.crime_file)
        df_crime["crime_score"] = self.min_max_normalize(df_crime["count"], invert=True)
        output_path = self.base_dir / "data" / "cleaned_data" / "cleaned_data_crime.csv"
        df_crime.to_csv(output_path, index=False)
        print(f"Crime data processed and saved")
        return df_crime

    def process_econmic(self):

        df_econ = pd.read_csv(self.econ_file)
        df_econ["mean travel time to work (minutes)"] = self.min_max_normalize(df_econ["mean travel time to work (minutes)"], invert=True)
        df_econ["unemployed"] = self.min_max_normalize(df_econ["unemployed"], invert=True)
        output_path = self.base_dir / "data" / "cleaned_data" / "cleaned_data_economic_infrastructure.csv"
        df_econ.to_csv(output_path, index=False)
        print(f"Economics data processed and saved")
        return df_econ

if __name__ == "__main__":
    normalizer = DataNormalizer()
    normalizer.process_environment()
    normalizer.process_crime()
    normalizer.process_econmic()
