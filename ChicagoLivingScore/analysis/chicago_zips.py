import pandas as pd
from pathlib import Path

# Correct zipcode list
chicago_zipcodes = [
    60601, 60602, 60603, 60604, 60605, 60606, 60607, 60608, 60609, 60610, 60611, 
    60612, 60613, 60614, 60615, 60616, 60617, 60618, 60619, 60620, 60621, 60622, 
    60623, 60624, 60625, 60626, 60628, 60629, 60630, 60631, 60632, 60633, 60634, 
    60636, 60637, 60638, 60639, 60640, 60641, 60642, 60643, 60643, 60644, 60645, 
    60646, 60647, 60649, 60651, 60652, 60653, 60654, 60655, 60656, 60657, 60659, 
    60660, 60661, 60666, 60707, 60827
    ]

BASE_DIR = Path(__file__).parent.parent
DATA_FILE = BASE_DIR / "data" / "cleaned_data" /"chicago_zip.csv"
df = pd.DataFrame(chicago_zipcodes, columns=["zip_code"])
df.to_csv(DATA_FILE, index=False)
