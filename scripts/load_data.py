# -*- coding: utf-8 -*-
"""
Created on Thu May  7 10:13:11 2026

@author: salva
"""

import os 
import sqlite3
import pandas as pd 

# --- PATH SETUP --- 
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
data_dir = os.path.join(project_root, "data")
scripts_dir = os.path.join(project_root, "scripts")
sql_dir = os.path.join(project_root, 'sql')

data_path = os.path.join(data_dir, "german.data")
db_path = os.path.join(data_dir, "credit_risk.db")

# --- 1. STAGING RAW DATA ---
col_names = [f'c{i}' for i in range(0,21)]
df = pd.read_csv(data_path, sep=' ', header=None, names=col_names)

conn = sqlite3.connect(db_path)
df.to_sql('stg_german_credit', conn, if_exists='replace', index=False)
print("Step 1: Raw data staged.")

# --- 2. EXECUTE TRANSFORMATION SCRIPTS --- 
# Helper function used to read and run the .sql files 
def run_sql_file(filename, connection):
    path = os.path.join(sql_dir, filename)
    with open(path, 'r') as f:
        sql = f.read()
    # execute_script handles multiple commands
    connection.executescript(sql)
    
# ORDERED: Schema -> Transform -> View
run_sql_file('01_create_schema.sql', conn)
run_sql_file('02_transform_and_load.sql', conn)
print("Step 2: Schema created and data transformed.")

# --- 3. EXPORT CLEANED CSV --- 
with open(os.path.join(scripts_dir, '03_create_master_view.sql'), 'r') as f:
    view_script = f.read()
    
# DROP and CREATE VIEW for database 
conn.executescript(view_script)

# Create DataFrame from the view 
df_cleaned = pd.read_sql_query("SELECT * FROM view_master_credit_data", conn)

# Export and close
df_cleaned.to_csv(os.path.join(data_dir, "cleaned_german_credit.csv"), index=False)
print(f"Step 3: Exported {len(df_cleaned)} rows to cleaned_german_credit.csv")

conn.close()
