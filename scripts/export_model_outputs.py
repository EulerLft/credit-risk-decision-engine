# -*- coding: utf-8 -*-
"""
Created on Mon May 11 13:41:10 2026
@author: salva
"""

import os 
import joblib
import pandas as pd 
from modeling_engine import train_and_evaluate

# --- PATH SET UP --- 
script_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.join(script_dir, '..')

# Define the specific absolute paths for data and models 
data_dir = os.path.join(project_root, 'data')
models_dir = os.path.join(project_root, 'models')
input_data_path = os.path.join(data_dir, 'cleaned_german_credit.csv')
output_data_path = os.path.join(data_dir, 'credit_risk_predictions_lr_v5.csv')
model_output_path = os.path.join(models_dir, 'credit_risk_model_lr_v5.joblib')

def export_assets():
    # Load the dataset used for training
    df = pd.read_csv(input_data_path )
    
    # Re-run the optimized training to get the final model object 
    model, training_cols, metrics = train_and_evaluate(df)
    
    # Save the model for Streamlit
    joblib.dump(model, model_output_path)
    print(f"Model saved successfully at: {model_output_path}")
    
    # Generate predictions for the full dataset
    feature_cols = ['checking_status', 'savings_status', 'credit_history', 'guarantors', 
                    'purpose', 'marital_status', 'housing', 'employment_duration', 'amount', 'duration']    
    
    X = pd.get_dummies(df[feature_cols], dtype=int, drop_first=True)
    X = X.reindex(columns=training_cols, fill_value=0)
    
    # Add the executive insights columns 
    df['predicted_risk_label'] = model.predict(X)
    df['risk_probability'] = model.predict_proba(X)[:, 1]
    
    # Export to CSV for Tableau
    df.to_csv(output_data_path, index=False)
    print(f"Tableau export created: {output_data_path}")
    
if __name__ == "__main__":
    export_assets()
    
    
