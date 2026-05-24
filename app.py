from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
from functools import wraps

app = Flask(__name__)
app.secret_key = 'Traffic_case_Tracker_secret_2026'   



def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Karthick@357",
        database="traffic_db"
    )



def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'officer_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        badge    = request.form['badge'].strip()
        password = request.form['password'].strip()
        try:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM Officers WHERE badge_number = %s AND password = %s",
                (badge, password)
            )
            officer = cursor.fetchone()
            cursor.close()
            db.close()

            if officer:
                session['officer_id']   = officer['officer_id']
                session['officer_name'] = officer['officer_name']
                session['station']      = officer['station']
                session['badge']        = officer['badge_number']
                return redirect(url_for('index'))
            else:
                error = "Invalid badge number or password."
        except Error as e:
            print(f"[DB ERROR] {e}")
            error = "Database connection error. Please try again."

    return render_template('login.html', error=error)



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    stats = {'total_violations': 0, 'total_vehicles': 0, 'my_records': 0}
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM Records")
        stats['total_violations'] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Vehicles")
        stats['total_vehicles'] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Records WHERE officer_id = %s", (session['officer_id'],))
        stats['my_records'] = cursor.fetchone()[0]
        cursor.close()
        db.close()
    except Error as e:
        print(f"[DB ERROR] {e}")

    return render_template('index.html', stats=stats)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    success = False
    if request.method == 'POST':
        vehicle   = request.form['vehicle'].strip().upper()
        owner     = request.form.get('owner', '').strip()
        phone     = request.form.get('phone', '').strip()
        violation = request.form['violation'].strip()
        fine      = request.form['fine'].strip()
        location  = request.form.get('location', '').strip()

        try:
            db = get_db()
            cursor = db.cursor()

            cursor.execute("SELECT vehicle_id FROM Vehicles WHERE vehicle_number = %s", (vehicle,))
            v = cursor.fetchone()
            vehicle_id = v[0] if v else None
            if not vehicle_id:
                cursor.execute(
                    "INSERT INTO Vehicles (vehicle_number, owner_name, owner_phone) VALUES (%s, %s, %s)",
                    (vehicle, owner, phone)
                )
                db.commit()
                vehicle_id = cursor.lastrowid

            cursor.execute("SELECT violation_id FROM Violations WHERE violation_type = %s", (violation,))
            v2 = cursor.fetchone()
            violation_id = v2[0] if v2 else None
            if not violation_id:
                cursor.execute(
                    "INSERT INTO Violations (violation_type, fine_amount) VALUES (%s, %s)",
                    (violation, fine)
                )
                db.commit()
                violation_id = cursor.lastrowid

            cursor.execute(
                """INSERT INTO Records (vehicle_id, violation_id, officer_id, violation_date, location)
                   VALUES (%s, %s, %s, NOW(), %s)""",
                (vehicle_id, violation_id, session['officer_id'], location)
            )
            db.commit()
            cursor.close()
            db.close()
            success = True

        except Error as e:
            print(f"[DB ERROR] {e}")

    return render_template('add_violation.html', success=success)



@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    data = None
    searched_vehicle = ''
    if request.method == 'POST':
        searched_vehicle = request.form['vehicle'].strip().upper()
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                """SELECT v.vehicle_number, v.owner_name, vi.violation_type,
                          vi.fine_amount, r.violation_date, r.location,
                          o.officer_name, o.station
                   FROM Records r
                   JOIN Vehicles   v  ON r.vehicle_id  = v.vehicle_id
                   JOIN Violations vi ON r.violation_id = vi.violation_id
                   JOIN Officers   o  ON r.officer_id  = o.officer_id
                   WHERE v.vehicle_number = %s
                   ORDER BY r.violation_date DESC""",
                (searched_vehicle,)
            )
            data = cursor.fetchall()
            cursor.close()
            db.close()
        except Error as e:
            print(f"[DB ERROR] {e}")
            data = []

    return render_template('search.html', data=data, searched_vehicle=searched_vehicle)



if __name__ == '__main__':
    app.run(debug=True)
