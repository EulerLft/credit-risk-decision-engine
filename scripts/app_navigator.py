# -*- coding: utf-8 -*-
"""
Credit Risk Prediction App
@author: Sal Fernandez
Description: A Streamlit-based web interface for real-time credit risk assessment. 
Pre-trained Logistic Regression model predicts likelihood of loan default based on applicant data.
Created on Wed May 13 09:29:07 2026
"""

import os 
import pandas as pd 
import streamlit as st
import joblib

# --- PATH SET UP --- 
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
MODEL_DIR = os.path.join(PROJECT_DIR, "models")

model_path = os.path.join(MODEL_DIR, 'credit_risk_model_lr_v5.joblib')

# --- PAGE CONFIG ---
# Sets the browser tab title and centers the application layout 
st.set_page_config(page_title='Credit Risk Predictor', layout='centered')

# --- LOAD ML MODEL --- 
@st.cache_resource
def load_model():
    """
    Loads and caches the joblib model to prevent redundant I/O operations.
    Returns: sklearn.pipeline.Pipeline: The trained modeling pipeline.
    """
    return joblib.load(model_path)

# Initialize the model
model = load_model()

# --- APP UI  DESIGN ---
st.title("🏦 Credit Risk Assessment Tool")
st.markdown("""
This tool uses a machine learning engine to evaluate credit risk. 
Please input the applicant's details below to generate a risk profile.
""")

with st.form("applicant_form"):
    st.subheader("Applicant Financial & Demographic Profiles")
    col1, col2 = st.columns(2)
    
    with col1:
        checking_status = st.selectbox("Checking Account Status",
                                       ['< 0 DM', '0 - 200 DM', '>= 200 DM', 'no account'])
        savings_status = st.selectbox("Savings Account Status", 
                                      ['< 100 DM', '100 - 500 DM', '500 - 1,000 DM', '>= 1,000 DM', 'unknown/no savings'])
        credit_history = st.selectbox("Credit History Status", 
                                      ['critical account/other credits existing', 'existing credits paid back duly', 
                                       'delay paying off in the past', 'all credits at this bank paid back duly', 'no credits/paid back duly'])
        purpose = st.selectbox("Loan Purpose", 
                               ['car (new)', 'car (used)', 'furniture/equipment', 'radio/television', 'domestic appliance', 'repairs', 
                                'education', 'vacation', 'retraining', 'business', 'other'])
        amount = st.number_input("Requested Credit Amount (DM)", min_value=0, value=1000, step=1)
    
    with col2:
        duration = st.number_input("Loan Duration (months)", min_value=1, value=12, step=1)
        employment_duration = st.selectbox("Employment Duration", 
                                           ['unemployed', '< 1 year', '1 - 4 years', '4 - 7 years', '> 7 years', 'unknown'])
        marital_status = st.selectbox('Marital Status', 
                                      ['divorved/separated', 'single', 'married/widowed', 'non-single/single'])
        housing = st.selectbox('Housing Status', 
                               ['rent', 'own', 'for free'])
        guarantors = st.selectbox('Guarantors / Co-applicants', 
                                 ['none', 'co-applicant', 'gurantor', 'unknown'])
    submit = st.form_submit_button("Generate Loan Assessment")
        
# --- INTERFACE ENGINE --- 
if submit: 
    # Package user input into a structure consistent with the training dataset 
    input_dict = {
        'checking_status': checking_status,
        'savings_status': savings_status,
        'credit_history': credit_history,
        'guarantors': guarantors,
        'purpose': purpose,
        'marital_status': marital_status, 
        'housing': housing,
        'employment_duration': employment_duration,
        'amount': int(amount),
        'duration': int(duration)
        }
    input_df = pd.DataFrame([input_dict])
    
    # Convert categorical variables into dummy/indicator variables 
    input_encoded = pd.get_dummies(input_df, dtype=int)
    
    # Align the dynamic input with the fixed feature set expected by the model 
    # Missing columns (unselected categories) are filled with 0 
    model_features = model.feature_names_in_
    input_encoded = input_encoded.reindex(columns=model_features, fill_value=0)
    
    # Perform the prediction and calculate probability 
    probability = model.predict_proba(input_encoded)[0][1]
    verdict = "High Risk" if probability > 0.5 else "Low Risk"
    
    # --- RESULTS VISUALIZATION ---
    st.divider()
    
    # Display the final classification
    if verdict == "High Risk":
        st.error(f"**Final Verdict:** {verdict}")
    else:
        st.success(f"**Final Verdict:** {verdict}")
        
    # Visual metric showing the probability percentage 
    st.metric("Estimated Probability of Default", f"{probability*100:.2f}%")
    
    # Progress bar to represent risk intensity visually 
    st.progress(probability)
    st.caption("Risk Evaluation: A probability threshold of 0.5 is used to determine the risk category.")
    
    