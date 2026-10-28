from db_config import cursor, db


# ===============================
# Create Assignment (Staff)
# ===============================
def create_assignment(title, description, subject, deadline, staff_id):

    query = """
    INSERT INTO assignments(title, description, subject, deadline, staff_id)
    VALUES(%s,%s,%s,%s,%s)
    """

    cursor.execute(query,(title,description,subject,deadline,staff_id))
    db.commit()



# ===============================
# Get All Assignments (Student)
# ===============================
def get_assignments():

    query = "SELECT * FROM assignments"

    cursor.execute(query)

    return cursor.fetchall()



# ===============================
# Submit Assignment (Student)
# ===============================
def submit_assignment(assignment_id, student_id, file_path):

    query = """
    INSERT INTO submissions(assignment_id, student_id, file_path)
    VALUES(%s,%s,%s)
    """

    cursor.execute(query,(assignment_id,student_id,file_path))
    db.commit()



# ===============================
# View Submissions (Staff)
# ===============================
def get_submissions(assignment_id):

    query = """
    SELECT
        submissions.submission_id,
        students.student_name,
        submissions.file_path,
        submissions.marks,
        submissions.feedback
    FROM submissions
    JOIN students
    ON submissions.student_id = students.student_id
    WHERE submissions.assignment_id=%s
    """

    cursor.execute(query,(assignment_id,))

    return cursor.fetchall()



# ===============================
# Grade Assignment (Staff)
# ===============================
def grade_submission(submission_id, marks, feedback):

    query = """
    UPDATE submissions
    SET marks=%s, feedback=%s
    WHERE submission_id=%s
    """

    cursor.execute(query,(marks,feedback,submission_id))
    db.commit()


# ===============================
# Get Assignments by Staff
# ===============================
def get_staff_assignments(staff_id):

    query = """
    SELECT assignment_id, title, subject, deadline
    FROM assignments
    WHERE staff_id=%s
    ORDER BY deadline DESC
    """

    cursor.execute(query,(staff_id,))
    return cursor.fetchall()