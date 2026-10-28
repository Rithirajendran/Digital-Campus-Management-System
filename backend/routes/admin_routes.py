from flask import Blueprint, render_template
from models.admin_model import (
    get_total_students,
    get_staff_count,
    get_average_attendance,
    get_low_attendance_students
)

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin_dashboard")
def admin_dashboard():

    total_students = get_total_students()
    total_staff = get_staff_count()
    avg_attendance = get_average_attendance()

    low_students = get_low_attendance_students()

    clean_students = []

    for s in low_students:
        clean_students.append((s[0], float(s[1])))

    low_attendance = len(clean_students)

    return render_template(
        "admin_dashboard.html",
        total_students=total_students,
        total_staff=total_staff,
        avg_attendance=avg_attendance,
        low_attendance=low_attendance,
        low_attendance_students=clean_students
    )