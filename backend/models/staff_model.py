from db_config import cursor

def staff_login(email, password):

    query = "SELECT * FROM staff WHERE email=%s AND password=%s"
    cursor.execute(query, (email, password))

    return cursor.fetchone()


def get_assigned_students(staff_id):

    query = "SELECT * FROM students WHERE mentor_id=%s"
    cursor.execute(query, (staff_id,))

    return cursor.fetchall()




def get_mentor(student_id):

    query = """
    SELECT s.staff_name, s.email
    FROM staff s
    JOIN students st ON s.staff_id = st.mentor_id
    WHERE st.student_id = %s
    """

    cursor.execute(query, (student_id,))
    return cursor.fetchone()