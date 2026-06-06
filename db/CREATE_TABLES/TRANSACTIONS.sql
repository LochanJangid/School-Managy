CREATE TABLE IF NOT EXISTS Transactions (
	id INT PRIMARY KEY,
	student_id INT NOT NULL,
	amount DECIMAL NOT NULL,
	taken_by INT NOT NULL,
	FOREIGN KEY (student_id) REFERENCES Students(id),
	FOREIGN KEY (taken_by) REFERENCES Staff(id)
);