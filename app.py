from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host='10.0.2.126',
        user='flaskuser',
        password='StrongPassword123',
        database='universitydb'
    )

# Home - View Courses
@app.route('/')
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM courses")
    courses = cur.fetchall()
    conn.close()
    return render_template('index.html', courses=courses)

# Register for Course
@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = get_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        student_name = request.form['student_name']
        course_id = request.form['course_id']

        cur.execute(
            "INSERT INTO registrations(student_name, course_id) VALUES (%s,%s)",
            (student_name, course_id)
        )

        conn.commit()
        conn.close()

        return redirect('/')

    cur.execute("SELECT * FROM courses")
    courses = cur.fetchall()

    conn.close()

    return render_template('register.html', courses=courses)

# View Registrations
@app.route('/all_registrations')
def all_registrations():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT registrations.student_name,
               courses.course_name
        FROM registrations
        JOIN courses
        ON registrations.course_id = courses.id
    """)

    registrations = cur.fetchall()

    conn.close()

    return render_template(
    'all_registrations.html',
    registrations=registrations
)

# Admin Panel
@app.route('/admin')
def admin():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM courses")
    courses = cur.fetchall()

    conn.close()

    return render_template(
        'admin.html',
        courses=courses
    )

# Add Course
@app.route('/add_course', methods=['POST'])
def add_course():
    course_name = request.form['course_name']

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO courses(course_name) VALUES (%s)",
        (course_name,)
    )

    conn.commit()
    conn.close()

    return redirect('/admin')

# Delete Course
@app.route('/delete_course/<int:id>')
def delete_course(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM courses WHERE id=%s",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/admin')


@app.route('/mycourses', methods=['GET', 'POST'])
def mycourses():

    courses = []

    if request.method == 'POST':

        student_name = request.form['student_name']

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT courses.course_name
            FROM registrations
            JOIN courses
            ON registrations.course_id = courses.id
            WHERE registrations.student_name = %s
        """, (student_name,))

        courses = cur.fetchall()

        conn.close()

    return render_template(
        'mycourses.html',
        courses=courses
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)