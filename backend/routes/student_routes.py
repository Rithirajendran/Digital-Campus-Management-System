from flask import Blueprint, render_template, request, redirect
from db_config import cursor
import os
from datetime import datetime, date
from models.video_model import get_videos
from models.marks_model import get_marks
from models.attendance_model import get_subject_attendance, get_overall_attendance
from models.staff_model import get_mentor
from models.material_model import get_materials
from models.assignment_model import get_assignments, submit_assignment
from models.prediction_model import predict_result
from models.notification_model import get_notifications
from models.chat_model import send_message, get_messages
from werkzeug.utils import secure_filename
student_bp = Blueprint("student", __name__)
# ==============================
# Student Dashboard (FIXED ✅)
# ==============================
@student_bp.route("/student_dashboard/<int:student_id>")
def student_dashboard(student_id):

    # STUDENT DETAILS
    cursor.execute(
        "SELECT student_name, email FROM students WHERE student_id=%s",
        (student_id,)
    )
    student = cursor.fetchone()
    student_name = student[0]
    student_email = student[1]
    # EXISTING FEATURES
    subjects = get_subject_attendance(student_id)
    marks = get_marks(student_id)
    mentor = get_mentor(student_id)
    videos = get_videos()
    notifications = get_notifications(student_id)

    # ✅ NEW FEATURES (EVENTS + ANNOUNCEMENTS)
    cursor.execute("SELECT * FROM events ORDER BY date DESC")
    events = cursor.fetchall()
    cursor.execute("SELECT * FROM announcements ORDER BY created_at DESC")
    announcements = cursor.fetchall()
    return render_template(
        "student_dashboard.html",
        student_id=student_id,
        student_name=student_name,
        student_email=student_email,
        subjects=subjects,
        marks=marks,
        mentor=mentor,
        videos=videos,
        notifications=notifications,
        events=events,              # ✅ added
        announcements=announcements # ✅ added
    )

# ==============================
# VIDEOS
# ==============================
@student_bp.route("/videos/<int:student_id>")
def videos_page(student_id):
    videos = get_videos()
    return render_template(
        "videos.html",
        videos=videos,
        student_id=student_id
    )
@student_bp.route("/materials/<int:student_id>")
def view_materials(student_id):

    materials = get_materials()

    return render_template(
        "materials.html",
        materials=materials,
        student_id=student_id
    )
@student_bp.route("/assignments/<int:student_id>")
def student_assignments(student_id):
    assignments = get_assignments()
    return render_template(
        "assignments.html",
        assignments=assignments,
        student_id=student_id
    )


# ==============================
# CHAT (STUDENT)
# ==============================
@student_bp.route("/chat/<int:student_id>/<int:staff_id>")
def chat_page(student_id, staff_id):

    messages = get_messages(student_id, staff_id)

    return render_template(
        "chat.html",
        messages=messages,
        student_id=student_id,
        staff_id=staff_id
    )


@student_bp.route("/send_message", methods=["POST"])
def send_msg():

    student_id = request.form["student_id"]
    staff_id = request.form["staff_id"]
    message = request.form["message"]

    send_message(student_id, staff_id, "student", message)

    return redirect(f"/chat/{student_id}/{staff_id}")


# ==============================
# ATTENDANCE
# ==============================
@student_bp.route("/student_attendance/<int:student_id>")
def student_attendance(student_id):

    overall = get_overall_attendance(student_id)
    subjects = get_subject_attendance(student_id)

    return render_template(
        "student_attendance.html",
        student_id=student_id,
        present=overall[0],
        onduty=overall[1],
        absent=overall[2],
        subjects=subjects
    )


# ==============================
# MARKS
# ==============================
@student_bp.route("/student_marks/<int:student_id>")
def student_marks(student_id):

    marks = get_marks(student_id)

    return render_template(
        "student_marks.html",
        marks=marks,
        student_id=student_id
    )


# ==============================
# PREDICTION
# ==============================
@student_bp.route("/prediction/<int:student_id>")
def prediction(student_id):

    overall = get_overall_attendance(student_id)
    attendance = (overall[0] or 0) + (overall[1] or 0)

    marks = get_marks(student_id)

    total = sum(int(m[1]) for m in marks if str(m[1]).isdigit())
    avg_marks = total / len(marks) if marks else 0

    result = predict_result(attendance, avg_marks)

    return render_template(
        "prediction.html",
        attendance=attendance,
        marks=round(avg_marks, 2),
        result=result
    )

@student_bp.route("/announcements/<int:student_id>")
def student_announcements(student_id):

    cursor.execute("SELECT * FROM announcements ORDER BY created_at DESC")
    announcements = cursor.fetchall()

    return render_template(
        "announcements.html",
        announcements=announcements,
        student_id=student_id
    )
# ==============================
# EVENTS
# ==============================
@student_bp.route("/events/<int:student_id>")
def student_events(student_id):

    cursor.execute("SELECT * FROM events ORDER BY date DESC")
    events = cursor.fetchall()

    updated_events = []

    for e in events:
        e = list(e)

        # ✅ FIXED INDEX (date = e[3])
        if isinstance(e[3], str):
            e[3] = datetime.strptime(e[3], "%Y-%m-%d").date()

        updated_events.append(e)

    return render_template(
        "events.html",
        events=updated_events,
        student_id=student_id,
        current_date=date.today()
    )
