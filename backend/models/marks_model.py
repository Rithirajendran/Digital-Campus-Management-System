from db_config import cursor, db


# ==============================
# ADD MARKS
# ==============================
def add_marks(student_id, subject, exam_type, marks, total_marks):

    query = """
    INSERT INTO marks (student_id, subject, exam_type, marks, total_marks)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (student_id, subject, exam_type, marks, total_marks))
    db.commit()


# ==============================
# GET MARKS
# ==============================
def get_marks(student_id):

    query = """
    SELECT subject, marks, total_marks, exam_type
    FROM marks
    WHERE student_id = %s
    """

    cursor.execute(query, (student_id,))
    return cursor.fetchall()