# -*- coding: utf-8 -*-
"""
Created on Mon May 11 11:11:35 2026
@author: salva
"""

import os 
import pandas as pd 
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression 
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

# --- PATH SET UP --- 
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, '..', 'data', 'cleaned_german_credit.csv')


def run_grid_search():
    df = pd.read_csv(data_path)
    
    feature_cols = ['checking_status', 'savings_status', 'credit_history', 'guarantors', 
                    'purpose', 'marital_status', 'housing', 'employment_duration', 'amount', 'duration']
    
    X = pd.get_dummies(df[feature_cols], dtype=int, drop_first=True)
    y = df['risk_label']

    # Split into training and testing datasets 
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=42, stratify=y)
    
    # Pipeline handles scaling inside each Cross-Validation
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', LogisticRegression(
            solver='saga', 
            penalty='elasticnet',
            max_iter=5000, 
            random_state=42))
        ])
    
    # Parameter must use the prefix 'model__'
    param_grid = {
        'model__C': [0.1, 1, 10, 100],
        'model__l1_ratio': [0, 1],
        'model__class_weight': ['balanced', None]
    }
    
    # Optimizing for recall to minimize false negatives
    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        scoring='recall',
        cv=5,
        verbose=1
    )
    
    grid_search.fit(X_train, y_train)
    
    print(f"Best Parameters: {grid_search.best_params_}")
    
    # Evaluate best estimator on holdout data
    y_pred = grid_search.predict(X_test)
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))

if __name__ == "__main__":
    run_grid_search()