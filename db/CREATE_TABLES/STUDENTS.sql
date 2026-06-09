CREATE TABLE IF NOT EXISTS Students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    serial_number INTEGER UNIQUE,
    student_name TEXT NOT NULL,
    father_name TEXT,
    mother_name TEXT,
    address TEXT,
    phone_number TEXT, 
    class TEXT NOT NULL,
    medium TEXT NOT NULL CHECK(medium IN ('E', 'H')), 
    rte TEXT NOT NULL CHECK(rte IN ('Y', 'N')), 
    gender TEXT CHECK(gender IN ('M', 'F')), 
    dob DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (class, medium) REFERENCES FeesStructure(class, medium)
);