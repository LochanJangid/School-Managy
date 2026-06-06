CREATE TABLE IF NOT EXISTS Fees_Structure (
	class VARCHAR(5) UNIQUE NOT NULL,
	medium CHAR(1) NOT NULL,
	fees INT,
	PRIMARY KEY(class, medium)
);