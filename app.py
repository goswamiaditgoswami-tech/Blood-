from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import json
from datetime import datetime
from analysis import analyze_report

app = Flask(__name__)
app.secret_key = "blood-report-secret-key"



DATABASE = "database.db"


# ---------------- DATABASE CONNECTION ----------------

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- CREATE REPORT TABLE ----------------

def create_report_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS blood_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            report_date TEXT NOT NULL,
            total_count INTEGER,
            normal_count INTEGER,
            low_count INTEGER,
            high_count INTEGER,
            results TEXT,
            patient_data TEXT
        )
    """)

    conn.commit()
    conn.close()


# Create table when application starts
create_report_table()


# ---------------- HOME PAGE ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()

        try:
            conn.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )

            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return "Email already registered. Please use another email."

        conn.close()

        # Show the welcome message on the login page after successful registration.
        flash("Welcome! Your account has been created successfully.", "success")

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        ).fetchone()

        conn.close()

        if user:

            session["user_id"] = user["id"]
            session["name"] = user["name"]
            session["email"] = user["email"]

            return redirect(url_for("dashboard"))

        flash("Invalid email or password!")
        return redirect(url_for("login"))

    return render_template("login.html")


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = get_db_connection()

    # Count total reports
    report_count = conn.execute(
        "SELECT COUNT(*) FROM blood_reports WHERE user_id = ?",
        (user_id,)
    ).fetchone()[0]

    # Get latest report
    latest_report = conn.execute("""
        SELECT
            id,
            report_date,
            total_count,
            normal_count,
            low_count,
            high_count
        FROM blood_reports
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (user_id,)).fetchone()

    # Get report history
    history = conn.execute("""
        SELECT
            id,
            report_date,
            total_count,
            normal_count,
            low_count,
            high_count
        FROM blood_reports
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 10
    """, (user_id,)).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        name=session.get("name"),
        email=session.get("email"),
        report_count=report_count,
        latest_report=latest_report,
        history=history
    )


# ---------------- MANUAL REPORT ----------------

@app.route("/manual-report", methods=["GET", "POST"])
def manual_report():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        # Patient information
        name = request.form.get("name", session.get("name", "Patient"))
        email = request.form.get("email", session.get("email", ""))
        age = request.form.get("age", "Not Provided")
        gender = request.form.get("gender", "male")

        # Blood report values
        hemoglobin = request.form.get("hemoglobin")
        wbc = request.form.get("wbc")
        rbc = request.form.get("rbc")
        platelets = request.form.get("platelets")
        glucose = request.form.get("glucose")
        cholesterol = request.form.get("cholesterol")
        creatinine = request.form.get("creatinine")

        try:

            data = {
                "name": name,
                "email": email,
                "age": age,
                "gender": gender,
                "hemoglobin": float(hemoglobin),
                "wbc": float(wbc),
                "rbc": float(rbc),
                "platelets": float(platelets),
                "glucose": float(glucose),
                "cholesterol": float(cholesterol),
                "creatinine": float(creatinine)
            }

        except (ValueError, TypeError):

            return """
            <h2>Invalid Input</h2>
            <p>Please enter valid numbers for all blood test values.</p>
            <a href="/manual-report">Go Back</a>
            """

        # Analyze report
        results, summary, overall_message = analyze_report(data)

        # ---------------- SAVE REPORT ----------------

        conn = get_db_connection()

        report_date = datetime.now().strftime("%d-%m-%Y %H:%M")

        cursor = conn.execute("""
            INSERT INTO blood_reports
            (
                user_id,
                report_date,
                total_count,
                normal_count,
                low_count,
                high_count,
                results,
                patient_data
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            report_date,
            summary["total"],
            summary["normal"],
            summary["low"],
            summary["high"],
            json.dumps(results),
            json.dumps(data)
        ))

        conn.commit()

        # Get newly created report ID
        report_id = cursor.lastrowid

        conn.close()

        # Show result page
        return render_template(
            "results.html",
            results=results,
            summary=summary,
            overall_message=overall_message,
            data=data,
            report_id=report_id
        )

    return render_template("manual_report.html")


# ---------------- VIEW OLD REPORT ----------------

@app.route("/report/<int:report_id>")
def view_report(report_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    report = conn.execute("""
        SELECT *
        FROM blood_reports
        WHERE id = ? AND user_id = ?
    """, (report_id, session["user_id"])).fetchone()

    conn.close()

    if report is None:
        return "Report not found."

    # Convert saved JSON back to Python objects
    results = json.loads(report["results"])
    data = json.loads(report["patient_data"])

    summary = {
        "total": report["total_count"],
        "normal": report["normal_count"],
        "low": report["low_count"],
        "high": report["high_count"]
    }

    # Create overall message
    if summary["high"] == 0 and summary["low"] == 0:
        overall_message = "All analyzed values are within the selected reference ranges."

    elif summary["high"] > 0 and summary["low"] > 0:
        overall_message = "Some values are outside the selected reference ranges. Please review the detailed results."

    elif summary["high"] > 0:
        overall_message = "Some values are above the selected reference ranges. Please review the detailed results."

    else:
        overall_message = "Some values are below the selected reference ranges. Please review the detailed results."

    return render_template(
        "results.html",
        results=results,
        summary=summary,
        overall_message=overall_message,
        data=data,
        report_id=report["id"]
    )


# ---------------- UPLOAD REPORT ----------------

@app.route("/upload-report")
def upload_report():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("upload_report.html")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    app.run(debug=True)