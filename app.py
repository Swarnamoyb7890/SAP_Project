from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'student_database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_FILE):
        conn = get_db_connection()
        with open('setup_database.sql', 'r') as f:
            conn.executescript(f.read())
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/students', methods=['GET', 'POST'])
def handle_students():
    conn = get_db_connection()
    if request.method == 'GET':
        students = conn.execute('SELECT * FROM Students').fetchall()
        conn.close()
        return jsonify([dict(row) for row in students])
    
    if request.method == 'POST':
        data = request.json
        try:
            # 1. Insert student
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO Students (first_name, last_name, age, gender, email) VALUES (?, ?, ?, ?, ?)',
                (data['first_name'], data['last_name'], data['age'], data['gender'], data['email'])
            )
            student_id = cursor.lastrowid
            
            # 2. Automatically enroll them in a course if provided
            if 'course_id' in data:
                cursor.execute(
                    'INSERT INTO Enrollments (student_id, course_id, grade) VALUES (?, ?, ?)',
                    (student_id, data['course_id'], 'Pending')
                )
            
            conn.commit()
            return jsonify({'message': 'Student added and enrolled successfully!'}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 400
        finally:
            conn.close()

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    try:
        # First delete any enrollments for this student (though for unenrolled ones there won't be any)
        conn.execute('DELETE FROM Enrollments WHERE student_id = ?', (student_id,))
        # Then delete the student
        conn.execute('DELETE FROM Students WHERE student_id = ?', (student_id,))
        conn.commit()
        return jsonify({'message': 'Student deleted successfully!'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/students/cleanup', methods=['POST'])
def cleanup_students():
    conn = get_db_connection()
    try:
        # Delete students who are not in the Enrollments table
        cursor = conn.execute('DELETE FROM Students WHERE student_id NOT IN (SELECT student_id FROM Enrollments)')
        conn.commit()
        return jsonify({'message': f'Deleted {cursor.rowcount} unenrolled students.'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/courses', methods=['GET'])
def get_courses():
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM Courses').fetchall()
    conn.close()
    return jsonify([dict(row) for row in courses])

@app.route('/api/queries/<int:query_id>', methods=['GET'])
def run_named_query(query_id):
    conn = get_db_connection()
    queries = {
        1: "SELECT * FROM Students",
        2: "SELECT first_name, last_name, age FROM Students WHERE age > 21",
        3: "SELECT first_name, last_name, age FROM Students ORDER BY age DESC",
        4: "SELECT gender, COUNT(*) as student_count FROM Students GROUP BY gender",
        5: "SELECT gender, AVG(age) as average_age FROM Students GROUP BY gender ORDER BY average_age ASC",
        6: "SELECT c.course_name, COUNT(e.enrollment_id) as enrollment_count FROM Courses c LEFT JOIN Enrollments e ON c.course_id = e.course_id WHERE c.credits >= 3 GROUP BY c.course_name ORDER BY enrollment_count DESC"
    }
    
    query = queries.get(query_id)
    if not query:
        return jsonify({'error': 'Query not found'}), 404
        
    results = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(row) for row in results])

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
