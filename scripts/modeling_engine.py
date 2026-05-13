# -*- coding: utf-8 -*-
"""
Created on Sat May  9 10:47:30 2026

@author: salva
"""

import pandas as pd 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, recall_score, confusion_matrix

def preprocess_data(df):    
    # Isolate the selected feature columns for logistic regression
    feature_cols = ['checking_status', 'savings_status', 'credit_history', 'guarantors', 
                    'purpose', 'marital_status', 'housing', 'employment_duration', 'amount', 'duration']
    
    X = pd.get_dummies(df[feature_cols], dtype=int, drop_first=True)
    y = df.risk_label    
        
    return X, y, cols

def train_and_evaluate(df):
    # Isolate the selected feature columns for logistic regression
    feature_cols = ['checking_status', 'savings_status', 'credit_history', 'guarantors', 
                    'purpose', 'marital_status', 'housing', 'employment_duration', 'amount', 'duration']    
    
    X = pd.get_dummies(df[feature_cols], dtype=int, drop_first=True)
    y = df.risk_label    

    training_cols = X.columns    
    
    # Split features and target variables into training and testing sets 
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=42, stratify=y)
    
    # UPDATED: Locked in v5.0 Grid Search Best Parameters
    # We use solver='saga' and penalty='elasticnet' to support l1_ratio and avoid future warnings
    clf_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', LogisticRegression(
            solver='saga',
            penalty='elasticnet',
            C=0.1,
            l1_ratio=0, # 0 corresponds to L2 (Ridge) as found in best_params
            class_weight='balanced',
            random_state=42,
            max_iter=5000
            ))
        ])
    
    clf_pipeline.fit(X_train, y_train)
    y_pred = clf_pipeline.predict(X_test)
    
    # Calculate metrics 
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "conf_matrix": confusion_matrix(y_test, y_pred)
    }

    return clf_pipeline, training_cols, metrics


def predict_risk(new_applicant_df, model, training_cols):
    """ Process a new applicant and return the probability of default"""
    # One-hot encode new data
    new_X = pd.get_dummies(new_applicant_df, dtype=int)
    new_X = new_X.reindex(columns=training_cols, fill_value=0)
    
    probability = model.predict_proba(new_X)[0][1]
    prediction = model.predict(new_X)[0]
    
    return {
        "risk_probability": round(probability * 100, 2),
        "verdict": "High Risk" if prediction == 1 else "Low Risk"
    }

if __name__ == '__main__':
    import os
    # Localizing the data load inside the main block keeps the functions pure
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, '..', 'data', 'cleaned_german_credit.csv')
    
    if os.path.exists(data_path):
        df_sample = pd.read_csv(data_path)
        model, cols, metrics = train_and_evaluate(df_sample)
        
        print("-" * 30)
        print("MODEL TRAINING SUCCESSFUL")
        print(f"Accuracy: {metrics['accuracy']:.2f}")
        print(f"Recall:   {metrics['recall']:.2f}")
        print(f"F1 Score:   {metrics['f1']:.2f}")
        print("-" * 30)
        
        # Quick Test of the Prediction Function
        test_applicant = df_sample.iloc[[0]].drop('risk_label', axis=1)
        prediction = predict_risk(test_applicant, model, cols)
        print(f"Test Prediction for Customer 0: {prediction['verdict']} ({prediction['risk_probability']}%)")
    else:
        print(f"Error: Data file not found at {data_path}")