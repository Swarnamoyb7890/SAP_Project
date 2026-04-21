-- 1. SELECT: Retrieve all students
SELECT * FROM Students;

-- 2. WHERE: Filter students older than 21
SELECT first_name, last_name, age 
FROM Students 
WHERE age > 21;

-- 3. ORDER BY: List students by age in descending order
SELECT first_name, last_name, age 
FROM Students 
ORDER BY age DESC;

-- 4. GROUP BY: Count students by gender
SELECT gender, COUNT(*) as student_count 
FROM Students 
GROUP BY gender;

-- 5. Combined: Average age of students per gender, ordered by average age
SELECT gender, AVG(age) as average_age 
FROM Students 
GROUP BY gender 
ORDER BY average_age ASC;

-- 6. JOIN with WHERE and GROUP BY: Count enrollments per course for courses with > 3 credits
SELECT c.course_name, COUNT(e.enrollment_id) as enrollment_count
FROM Courses c
LEFT JOIN Enrollments e ON c.course_id = e.course_id
WHERE c.credits >= 3
GROUP BY c.course_name
ORDER BY enrollment_count DESC;
