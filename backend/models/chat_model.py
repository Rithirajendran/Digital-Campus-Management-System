from db_config import cursor, db

def send_message(student_id, staff_id, sender, message):

    is_read = 0 if sender == "student" else 1

    query = """
    INSERT INTO chat (student_id, staff_id, sender, message, type, is_read)
    VALUES (%s,%s,%s,%s,'personal',%s)
    """

    cursor.execute(query, (student_id, staff_id, sender, message, is_read))
    db.commit()


def get_messages(student_id, staff_id):

    query = """
    SELECT sender, message, created_at, type
    FROM chat
    WHERE student_id=%s AND staff_id=%s
    ORDER BY created_at ASC
    """

    cursor.execute(query, (student_id, staff_id))
    return cursor.fetchall()
# ===============================
# BROADCAST MESSAGE
# ===============================
def send_to_all_students(staff_id, message, students):

    for s in students:
        student_id = s[0]

        cursor.execute("""
        INSERT INTO chat (student_id, staff_id, sender, message, type)
        VALUES (%s, %s, %s, %s, 'broadcast')
        """, (student_id, staff_id, "staff", message))

    db.commit()

def get_pending_messages(staff_id):

    query = """
    SELECT c.student_id, s.student_name, COUNT(*) as total
    FROM chat c
    JOIN students s ON c.student_id = s.student_id
    WHERE c.staff_id=%s AND c.sender='student' AND c.is_read=0
    GROUP BY c.student_id, s.student_name
    """

    cursor.execute(query, (staff_id,))
    return cursor.fetchall()

def get_unread_counts(staff_id):

    query = """
    SELECT student_id, COUNT(*)
    FROM chat
    WHERE staff_id=%s AND sender='student' AND is_read=0
    GROUP BY student_id
    """

    cursor.execute(query, (staff_id,))
    return cursor.fetchall()
def get_students_with_messages(staff_id):

    query = """
    SELECT DISTINCT student_id
    FROM chat
    WHERE staff_id = %s
    ORDER BY created_at DESC
    """

    cursor.execute(query, (staff_id,))
    return cursor.fetchall()    