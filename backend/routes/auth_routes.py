from flask import Blueprint, render_template, request, redirect
from models.admin_model import admin_login
from models.staff_model import staff_login
from models.student_model import student_login

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def login_page():
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login():

    role = request.form["role"]
    email = request.form["email"]
    password = request.form["password"]

    # ADMIN LOGIN
    if role == "admin":
        admin = admin_login(email, password)

        if admin:
            return redirect("/admin_dashboard")


    # STAFF LOGIN
    elif role == "staff":
        staff = staff_login(email, password)

        if staff:
            staff_id = staff[0]
            return redirect(f"/staff_dashboard/{staff_id}")


    # STUDENT LOGIN
    elif role == "student":
        student = student_login(email, password)

        if student:
            student_id = student[0]
            return redirect(f"/student_dashboard/{student_id}")


    return "Invalid Login"
