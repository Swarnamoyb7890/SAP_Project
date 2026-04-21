-- Create Students table
CREATE TABLE IF NOT EXISTS Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    email TEXT UNIQUE
);

-- Create Courses table
CREATE TABLE IF NOT EXISTS Courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    credits INTEGER
);

-- Create Enrollments table (linking Students and Courses)
CREATE TABLE IF NOT EXISTS Enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    grade TEXT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

-- Insert sample data into Students
INSERT INTO Students (first_name, last_name, age, gender, email) VALUES
('John', 'Doe', 20, 'Male', 'john.doe@example.com'),
('Jane', 'Smith', 22, 'Female', 'jane.smith@example.com'),
('Alice', 'Johnson', 21, 'Female', 'alice.j@example.com'),
('Bob', 'Brown', 23, 'Male', 'bob.b@example.com'),
('Charlie', 'Davis', 20, 'Male', 'charlie.d@example.com');

-- Insert sample data into Courses
INSERT INTO Courses (course_name, credits) VALUES
('Mathematics', 4),
('Physics', 4),
('Computer Science', 3),
('History', 2);

-- Insert sample data into Enrollments
INSERT INTO Enrollments (student_id, course_id, grade) VALUES
(1, 1, 'A'),
(1, 3, 'B'),
(2, 1, 'A'),
(2, 2, 'B'),
(3, 3, 'A'),
(4, 4, 'C'),
(5, 1, 'B'),
(5, 2, 'A');
