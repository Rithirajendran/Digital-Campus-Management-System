from db_config import cursor

def student_login(email, password):

    query = "SELECT * FROM students WHERE email=%s AND password=%s"
    cursor.execute(query, (email, password))

    return cursor.fetchone()


def get_student_details(student_id):

    query = "SELECT * FROM students WHERE student_id=%s"
    cursor.execute(query, (student_id,))

    return cursor.fetchone()

def get_mentor(student_id):

    query = """
    SELECT staff.staff_name, staff.email
    FROM students
    JOIN staff ON students.mentor_id = staff.staff_id
    WHERE students.student_id = %s
    """

    cursor.execute(query, (student_id,))

    return cursor.fetchone()