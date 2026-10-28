from flask import Blueprint, render_template, request, redirect
import os
from werkzeug.utils import secure_filename
from datetime import date
from db_config import cursor, db

from models.video_model import add_video, get_videos
from models.staff_model import get_assigned_students
from models.marks_model import add_marks
from models.attendance_model import add_attendance
from models.material_model import add_material
from models.assignment_model import (
    create_assignment,
    get_submissions,
    grade_submission,
    get_staff_assignments
)

from models.notification_model import add_notification, get_notifications
from models.chat_model import send_message, get_messages

staff_bp = Blueprint("staff", __name__)

# ==============================
# 🔥 GET PENDING STUDENT MESSAGES
# ==============================
def get_pending_messages(staff_id):
    query = """
    SELECT student_id, COUNT(*) as total
    FROM chat
    WHERE staff_id=%s AND sender='student' AND is_read=0
    GROUP BY student_id
    """
    cursor.execute(query, (staff_id,))
    return cursor.fetchall()
# ==============================
# 🔥 GET LAST MESSAGE PER STUDENT
# ==============================
def get_last_messages(staff_id, students):
    last_messages = {}
    for s in students:
        student_id = s[0]
        msgs = get_messages(student_id, staff_id)
        if msgs:
            last_messages[student_id] = msgs[-1][1]
        else:
            last_messages[student_id] = None
    return last_messages

# ==============================
# 🔥 GET CHAT LIST
# ==============================
def get_student_chat_list(staff_id):
    query = """
    SELECT 
        s.student_id,
        s.student_name,
        COUNT(*) AS unread_count,
        MAX(c.created_at) as last_time
    FROM students s
    INNER JOIN chat c
        ON s.student_id = c.student_id 
    WHERE s.mentor_id = %s 
    AND c.staff_id = %s
    AND c.sender = 'student'
    AND c.is_read = 0
    GROUP BY s.student_id, s.student_name
    ORDER BY last_time DESC
    """
    cursor.execute(query, (staff_id, staff_id))
    return cursor.fetchall()


# ==============================
# STAFF DASHBOARD
# ==============================
@staff_bp.route("/staff_dashboard/<int:staff_id>")
def staff_dashboard(staff_id):
    students = get_assigned_students(staff_id)
    assignments = get_staff_assignments(staff_id)
    videos = get_videos()
    today = date.today()
    cursor.execute("""
        SELECT staff_name, email, department
        FROM staff
        WHERE staff_id = %s
    """, (staff_id,))
    mentor = cursor.fetchone()
    mentor_name = mentor[0] if mentor else "Not Available"
    mentor_email = mentor[1] if mentor else "Not Available"
    mentor_dept = mentor[2] if mentor else "Not Available"
    notifications = get_notifications(staff_id)
    pending_chats = get_pending_messages(staff_id)
    last_messages = get_last_messages(staff_id, students)
    chat_list = get_student_chat_list(staff_id)
    return render_template(
        "staff_dashboard.html",
        staff_id=staff_id,students=students,
        assignments=assignments, videos=videos,
        current_date=today,
        mentor_name=mentor_name,mentor_email=mentor_email,
        mentor_dept=mentor_dept,notifications=notifications,
        pending_chats=pending_chats,last_messages=last_messages,
        chat_list=chat_list
    )


# ==============================
# MY STUDENTS
# ==============================
@staff_bp.route("/my_students/<int:staff_id>")
def my_students(staff_id):
    students = get_assigned_students(staff_id)
    return render_template("my_students.html", students=students, staff_id=staff_id)


# ==============================
# MARKS
# ==============================
@staff_bp.route("/marks/<int:staff_id>")
def marks_page(staff_id):
    students = get_assigned_students(staff_id)
    return render_template("marks.html", students=students, staff_id=staff_id)


@staff_bp.route("/marks")
def marks_redirect():
    return redirect("/marks/1")


@staff_bp.route("/add_marks", methods=["POST"])
def add_marks_route():
    subject = request.form.get("subject")
    exam_type = request.form.get("exam_type")
    total = request.form.get("total_marks")

    for key in request.form:
        if key.startswith("marks_"):
            student_id = key.split("_")[1]
            marks = request.form.get(key)

            if marks:
                add_marks(student_id, subject, exam_type, marks, total)

                if int(marks) < 40:
                    add_notification(student_id, f"⚠ Low marks in {subject}", "marks")

    return "<h3>✅ Marks Saved Successfully</h3>"


# ==============================
# ATTENDANCE
# ==============================
@staff_bp.route("/attendance/<int:staff_id>")
def attendance(staff_id):
    students = get_assigned_students(staff_id)
    return render_template("attendance.html", students=students, staff_id=staff_id)


@staff_bp.route("/mark_attendance", methods=["POST"])
def mark_attendance_route():
    staff_id = request.form.get("staff_id")
    subject = request.form.get("subject")

    for key in request.form:
        if key.startswith("status_"):
            student_id = key.split("_")[1]
            status = request.form[key]

            if not subject or subject == "None":
                continue

            add_attendance(student_id, subject, status)

    return redirect(f"/staff_dashboard/{staff_id}")


# ==============================
# MATERIAL UPLOAD
# ==============================
@staff_bp.route("/upload_material", methods=["POST"])
def upload_material():
    title = request.form["title"]
    subject = request.form["subject"]
    staff_id = request.form["staff_id"]

    file = request.files["file"]

    upload_folder = "frontend/static/uploads"
    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(file.filename)
    file.save(os.path.join(upload_folder, filename))

    path = "uploads/" + filename
    add_material(title, subject, path, staff_id)

    return redirect(f"/staff_dashboard/{staff_id}")


# ==============================
# VIDEO
# ==============================
@staff_bp.route("/add_video", methods=["POST"])
def upload_video():
    title = request.form["title"]
    subject = request.form["subject"]
    youtube_link = request.form["youtube_link"]
    staff_id = request.form["staff_id"]

    add_video(title, subject, youtube_link, staff_id)
    return redirect(f"/staff_dashboard/{staff_id}")


# ==============================
# ADD EVENT ✅ FULLY FIXED
# ==============================
@staff_bp.route("/add_event", methods=["POST"])
def add_event():

    type = request.form["type"]
    title = request.form["title"]
    description = request.form["description"]
    date = request.form["date"]
    organizer = request.form.get("organizer")

    image = request.files.get("image")
    filename = None

    # ✅ SAFE IMAGE UPLOAD
    if image and image.filename != "":
        upload_folder = "frontend/static/uploads"
        os.makedirs(upload_folder, exist_ok=True)

        filename = "uploads/" + secure_filename(image.filename)
        image.save(os.path.join(upload_folder, filename.split("/")[-1]))

    query = """
    INSERT INTO events (type, title, description, date, image, organizer)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (type, title, description, date, filename, organizer))
    db.commit()

    return redirect(request.referrer)


# ==============================
# ADD ANNOUNCEMENT ✅ FIXED
# ==============================
@staff_bp.route("/add_announcement", methods=["POST"])
def add_announcement():

    title = request.form["title"]
    message = request.form["content"]
    type = request.form["type"]

    image = request.files.get("image")
    filename = None  # default = no image

    # ✅ ONLY run if image exists
    if image and image.filename != "":
        upload_folder = "frontend/static/uploads"
        os.makedirs(upload_folder, exist_ok=True)

        filename = secure_filename(image.filename)
        image.save(os.path.join(upload_folder, filename))

        filename = "uploads/" + filename

    # ✅ insert even if filename is None
    query = """
    INSERT INTO announcements (title, message, type, image)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (title, message, type, filename))
    db.commit()

    return redirect(request.referrer)

# ==============================
# 💬 STAFF CHAT (FULLY FIXED)
# ==============================
@staff_bp.route("/staff_chat/<int:staff_id>/<int:student_id>", methods=["GET", "POST"])
def staff_chat(staff_id, student_id):

    # ✅ SEND MESSAGE
    if request.method == "POST":
        message = request.form.get("message")

        if message:
            send_message(student_id, staff_id, "staff", message)

        return redirect(f"/staff_chat/{staff_id}/{student_id}")

    # ✅ MARK AS READ
    cursor.execute("""
        UPDATE chat
        SET is_read = 1
        WHERE student_id=%s AND staff_id=%s AND sender='student'
    """, (student_id, staff_id))
    db.commit()

    # ✅ GET MESSAGES
    messages = get_messages(student_id, staff_id)

    return render_template(
        "chat.html",
        staff_id=staff_id,
        student_id=student_id,
        messages=messages
    )
