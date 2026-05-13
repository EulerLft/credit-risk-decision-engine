CREATE TABLE dim_customer (
	customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
	age INTEGER,
	sex TEXT, 
	marital_status TEXT, 
	job TEXT,
	employment_duration TEXT,
	housing TEXT,
	guarantors TEXT,
	num_dependants INTEGER
);

CREATE TABLE dim_account (
	account_id INTEGER PRIMARY KEY AUTOINCREMENT,
	customer_id INTEGER,
	checking_status TEXT, 
	savings_status TEXT, 
	FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id)
);

CREATE TABLE fact_loan_application (
	loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
	customer_id INTEGER, 
	amount INTEGER,
	installment_rate REAL,
	duration INTEGER,
	purpose TEXT,
	credit_history TEXT,
	risk_label INTEGER,
	FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id)
);


