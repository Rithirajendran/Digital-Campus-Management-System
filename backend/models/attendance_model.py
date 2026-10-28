from db_config import cursor, db


# -----------------------------
# Mark Attendance (Staff)
# -----------------------------
def mark_attendance(student_id, status):

    query = """
    INSERT INTO attendance (student_id, date, status)
    VALUES (%s, CURDATE(), %s)
    """

    cursor.execute(query, (student_id, status))
    db.commit()


# -----------------------------
# Add Attendance with Subject
# -----------------------------
def add_attendance(student_id, subject, status):

    query = """
    INSERT INTO attendance(student_id, date, status, subject)
    VALUES(%s, CURDATE(), %s, %s)
    """

    cursor.execute(query, (student_id, status, subject))
    db.commit()


# -----------------------------
# Get Attendance Records
# -----------------------------
def get_attendance(student_id):

    query = """
    SELECT date, status
    FROM attendance
    WHERE student_id=%s
    ORDER BY date DESC
    """

    cursor.execute(query, (student_id,))
    return cursor.fetchall()


# -----------------------------
# ✅ SUBJECT-WISE ATTENDANCE (FIXED)
# -----------------------------
def get_subject_attendance(student_id):

    query = """
    SELECT 
        subject,

        ROUND(
            SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2
        ) AS present_percentage,

        ROUND(
            SUM(CASE WHEN status='OnDuty' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2
        ) AS onduty_percentage,

        ROUND(
            SUM(CASE WHEN status='Absent' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2
        ) AS absent_percentage

    FROM attendance
    WHERE student_id = %s
    GROUP BY subject
    """

    cursor.execute(query, (student_id,))
    return cursor.fetchall()


# -----------------------------
# Attendance Summary (Graph)
# -----------------------------
def get_attendance_summary(student_id):

    query = """
    SELECT
        SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END),
        SUM(CASE WHEN status='Absent' THEN 1 ELSE 0 END)
    FROM attendance
    WHERE student_id=%s
    """

    cursor.execute(query, (student_id,))
    result = cursor.fetchone()

    present = result[0] or 0
    absent = result[1] or 0

    return present, absent


# -----------------------------
# Overall Attendance %
# -----------------------------
def get_overall_attendance(student_id):

    query = """
    SELECT
    ROUND(SUM(status='Present')/COUNT(*)*100,2) AS present,
    ROUND(SUM(status='OnDuty')/COUNT(*)*100,2) AS onduty,
    ROUND(SUM(status='Absent')/COUNT(*)*100,2) AS absent
    FROM attendance
    WHERE student_id=%s
    """

    cursor.execute(query,(student_id,))
    return cursor.fetchone()