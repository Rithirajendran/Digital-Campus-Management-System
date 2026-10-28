from db_config import cursor, db

def add_notification(student_id, message, ntype):
    query = """
    INSERT INTO notifications(student_id, message, type)
    VALUES(%s,%s,%s)
    """
    cursor.execute(query, (student_id, message, ntype))
    db.commit()


def get_notifications(student_id):
    query = """
    SELECT message, type, created_at
    FROM notifications
    WHERE student_id=%s
    ORDER BY id DESC
    """
    cursor.execute(query, (student_id,))
    return cursor.fetchall()