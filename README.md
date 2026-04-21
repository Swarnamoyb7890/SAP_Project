# Student Database Manager

A Flask-based web application for managing student information, course enrollment, and academic records using SQLite.

## Features

- **Student Management**: Add, view, update, and delete student records
- **Course Management**: View available courses and their details
- **Enrollment System**: Automatically enroll students in courses with grade tracking
- **Data Cleanup**: Remove unenrolled students from the database
- **REST API**: Full API endpoints for programmatic access
- **Web Interface**: Bootstrap-based responsive user interface
- **Query System**: Execute predefined SQL queries on demand

## Technologies Used

- **Backend**: Python, Flask
- **Database**: SQLite
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **API**: RESTful JSON endpoints

## Project Structure

```
├── app.py                    # Main Flask application with REST API endpoints
├── run_sql.py               # Utility script to execute SQL scripts
├── setup_database.sql       # Database schema and sample data initialization
├── queries.sql              # Predefined SQL queries
├── templates/
│   └── index.html           # Web UI template
└── student_database.db      # SQLite database (created at runtime)
```

## Getting Started

### Prerequisites

- Python 3.6+
- Flask
- SQLite3 (usually included with Python)

### Installation

1. Clone or download the project to your local machine

2. Install required dependencies:

   ```bash
   pip install flask
   ```

3. Initialize the database:
   ```bash
   python run_sql.py
   ```
   This creates the `student_database.db` file with the schema and sample data.

### Running the Application

1. Start the Flask server:

   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:

   ```
   http://localhost:5000
   ```

3. Use the web interface to manage students and courses

## API Endpoints

### Students

- **GET** `/api/students` - Retrieve all students
- **POST** `/api/students` - Add a new student
- **DELETE** `/api/students/<id>` - Delete a student by ID
- **POST** `/api/students/cleanup` - Remove unenrolled students

### Courses

- **GET** `/api/courses` - Retrieve all available courses

### Queries

- **GET** `/api/queries/<id>` - Execute a predefined query by ID

## Database Schema

### Students Table

- `student_id` (Primary Key)
- `first_name`
- `last_name`
- `age`
- `gender`
- `email` (Unique)

### Courses Table

- `course_id` (Primary Key)
- `course_name`
- `credits`

### Enrollments Table

- `enrollment_id` (Primary Key)
- `student_id` (Foreign Key)
- `course_id` (Foreign Key)
- `grade`

## Example Usage

### Adding a Student via API

```bash
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "age": 20,
    "gender": "Male",
    "email": "john@example.com",
    "course_id": 1
  }'
```

### Getting All Students

```bash
curl http://localhost:5000/api/students
```

## Features Explanation

### Student Enrollment

When adding a new student, you can optionally provide a `course_id` to automatically enroll them in a course with a "Pending" grade status.

### Cascade Delete

When deleting a student, any associated enrollment records are automatically removed to maintain referential integrity.

### Cleanup Function

The cleanup endpoint removes students who are not enrolled in any courses, helping keep the database clean.

## Notes

- The SQLite database is stored in the project directory as `student_database.db`
- Sample data is automatically loaded on first initialization
- All timestamps and IDs are auto-managed by the database
- The application uses row factories for convenient dictionary access to database results

## License

This project is provided as-is for educational purposes.
