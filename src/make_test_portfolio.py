import os
import pandas as pd

# Get directories 
current_dir = os.getcwd()   
processed_dir = os.path.join(current_dir, 'data', 'processed')  # processed data directory

# Read sp1500 data
sp1500_df = pd.read_parquet(os.path.join(processed_dir, 'sp1500_199603_200111.parquet'))

