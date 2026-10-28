from db_config import cursor


def admin_login(email, password):

    query = "SELECT * FROM admin WHERE email=%s AND password=%s"
    cursor.execute(query, (email, password))

    admin = cursor.fetchone()

    return admin


def get_total_students():

    cursor.execute("SELECT COUNT(*) FROM students")
    result = cursor.fetchone()

    return result[0]


def get_staff_count():

    cursor.execute("SELECT COUNT(*) FROM staff")
    result = cursor.fetchone()

    return result[0]


def get_average_attendance():

    cursor.execute("""
        SELECT 
        (SUM(status='Present') / COUNT(*)) * 100
        FROM attendance
    """)

    result = cursor.fetchone()

    if result[0] is None:
        return 0

    return round(result[0], 2)


def get_low_attendance_students():

    cursor.execute("""
        SELECT student_id,
        (SUM(status='Present') / COUNT(*)) * 100 AS attendance_percentage
        FROM attendance
        GROUP BY student_id
        HAVING attendance_percentage < 75
    """)

    result = cursor.fetchall()

    return result