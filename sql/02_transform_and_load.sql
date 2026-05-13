INSERT INTO dim_customer(customer_id, age, sex, marital_status, job, employment_duration, housing, guarantors, num_dependants)
SELECT 
	ROWID,
	c12,
	CASE 
		WHEN c8 IN ('A91', 'A93', 'A94') THEN 'male'
		ELSE 'female'
	END AS sex,
	CASE 
		WHEN c8 = 'A91' THEN 'divorved/separated'
		WHEN c8 = 'A93' THEN 'single'
		WHEN c8 = 'A94' THEN 'married/widowed'
		WHEN c8 IN ('A92', 'A95') THEN 'non-single/single'
	END AS marital_status,
	CASE
		WHEN c16 = 'A171' THEN 'unemployed'
		WHEN c16 = 'A172' THEN 'unskilled employee'
		WHEN c16 = 'A173' THEN 'skilled employee'
		WHEN c16 = 'A174' THEN 'highly skilled employee'
	END AS job,
	CASE 
		WHEN c6 = 'A71' THEN 'unemployed'
		WHEN c6 = 'A72' THEN '< 1 year'
		WHEN c6 = 'A73' THEN '1 - 4 years'
		WHEN c6 = 'A74' THEN '4 - 7 years'
		WHEN c6 = 'A75' THEN '> 7 years'
		ELSE 'unknown'
	END AS employment_duration,
	CASE 
		WHEN c14 = 'A151' THEN 'rent'
		WHEN c14 = 'A152' THEN 'own'
		WHEN c14 = 'A153' THEN 'for free'
	END AS housing,
	CASE 
		WHEN c9 = 'A101' THEN 'none'
		WHEN c9 = 'A102' THEN 'co-applicant'
		WHEN c9 = 'A103' THEN 'gurantor'
		ELSE 'unknown'
	END AS guarantors,
	c17
FROM stg_german_credit;

INSERT INTO dim_account(customer_id, checking_status, savings_status)
SELECT
	ROWID,
	CASE
		WHEN c0 = 'A11' THEN '< 0 DM'
		WHEN c0 = 'A12' THEN '0 - 200 DM'
		WHEN c0 = 'A13' THEN '>= 200 DM'
		ELSE 'no account'
	END AS checking_status,
	CASE 
		WHEN c5 = 'A61' THEN '< 100 DM'
		WHEN c5 = 'A62' THEN '100 - 500 DM'
		WHEN c5 = 'A63' THEN '500 - 1,000 DM'
		WHEN c5 = 'A64' THEN '> 1,000 DM'
		ELSE 'unknown/no savings'
	END AS savings_status
FROM stg_german_credit; 
	
INSERT INTO fact_loan_application(customer_id, amount, installment_rate, duration, purpose, credit_history, risk_label)
SELECT 
	ROWID,
	c4, 
	c7,
	c1, 
	CASE
		WHEN c3 = 'A40' THEN 'car (new)'
		WHEN c3 = 'A41' THEN 'car (used)'
		WHEN c3 = 'A42' THEN 'furniture/equipment'
		WHEN c3 = 'A43' THEN 'radio/television'
		WHEN c3 = 'A44' THEN 'domestic appliance'
		WHEN c3 = 'A45' THEN 'repairs'
		WHEN c3 = 'A46' THEN 'education'
		WHEN c3 = 'A47' THEN 'vacation'
		WHEN c3 = 'A48' THEN 'retraining'
		WHEN c3 = 'A49' THEN 'business'
		ELSE 'other'
	END AS purpose,
	CASE 
		WHEN c2 = 'A30' THEN 'no credits/paid back duly'
		WHEN c2 = 'A31' THEN 'all credits at this bank paid back duly'
		WHEN c2 = 'A32' THEN 'existing credits paid back duly'
		WHEN c2 = 'A33' THEN 'delay paying off in the past'
		WHEN c2 = 'A34' THEN 'critical account/other credits existing (outside this bank)'
 	END AS credit_history,	
	CASE 
		WHEN c20 = 1 THEN 0
		WHEN c20 = 2 THEN 1
	END AS risk_label
FROM stg_german_credit;
