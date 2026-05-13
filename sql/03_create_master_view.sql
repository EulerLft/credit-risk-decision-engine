DROP VIEW IF EXISTS view_master_credit_data;

CREATE VIEW view_master_credit_data AS
SELECT 
	c.customer_id, 
	c.age,
	c.sex, 
	c.marital_status, 
	c.job,
	c.employment_duration, 
	c.housing, 
	c.guarantors, 
	c.num_dependants,
	a.checking_status, 
	a.savings_status,
	f.amount, 
	f.duration, 
	f.purpose, 
	f.credit_history, 
	f.installment_rate, 
	f.risk_label
FROM dim_customer c
JOIN dim_account a 
	ON c.customer_id = a.customer_id
JOIN fact_loan_application f 
	ON c.customer_id = f.customer_id;
	