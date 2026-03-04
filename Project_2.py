import os
import yaml
import pandas as pd
from sqlalchemy import create_engine

# --- CONFIGURATION ---
DATA_PATH = r'C:\Users\Administrator\Downloads\Data\extracted'
DB_USER = 'Selva'
DB_PASS = 'guru'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'first_schema'

# Create SQL Engine
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def process_data():
    all_rows = []
    for root, dirs, files in os.walk(DATA_PATH):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = yaml.safe_load(f)
                    if isinstance(content, list):
                        all_rows.extend(content)
                    elif isinstance(content, dict):
                        all_rows.append(content)

    full_df = pd.DataFrame(all_rows)

    # Use lowercase 'date' as confirmed by your previous debug log
    if 'date' in full_df.columns:
        full_df['date'] = pd.to_datetime(full_df['date'])
    
    print("Connecting to MySQL and uploading data...")
    # This creates the table 'nifty50_stocks'
    full_df.to_sql(name='nifty50_stocks', con=engine, if_exists='replace', index=False)
    
    print("✅ Success! Table 'nifty50_stocks' is now in your database.")

if __name__ == "__main__":
    process_data()