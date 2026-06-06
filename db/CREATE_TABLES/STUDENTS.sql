CREATE TABLE IF NOT EXISTS Students(
	id INT PRIMARY KEY,
	serial_number INT UNIQUE,
	student_name VARCHAR(50) NOT NULL,
	father_name VARCHAR(50),
	mother_name VARCHAR(50),
	address VARCHAR(50),
	phone_number VARCHAR(10), -- 10 digit phone numbers only
	CONSTRAINT chk_phone CHECK (LENGTH(phone_number) = 10), -- valid that number is 10 digit 
	class VARCHAR(5) NOT NULL,
	medium CHAR(1) NOT NULL, -- E (English), H(hindi)
	rte CHAR(1) NOT NULL, -- Y (Yes), N (No)
	gender CHAR(1), -- F (Female), M(Male)
	dob DATE,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (class, medium)
		REFERENCES FeesStructure(class, medium)
);