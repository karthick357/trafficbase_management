# 🛡 TrafficBase Management

A web-based **Traffic Violation Case Tracker** built for law enforcement officers. Officers can log in with their badge credentials, record traffic violations against vehicle numbers, and search the full enforcement history of any registered vehicle — all through a clean, role-aware dashboard.

## 🚀 Features

- **Officer Authentication** — Secure badge-number and password login; sessions are tracked per officer
- **Live Command Dashboard** — At-a-glance stats: total violations logged, vehicles registered, and your personal session records
- **Log Violations** — Record vehicle details, owner info, violation type, fine amount, and incident location in one form
- **Search Records** — Look up the complete violation history of any vehicle by registration number
- **Role Attribution** — Every record is permanently linked to the logging officer's badge and station
- **Responsive UI** — Dark-themed enforcement-grade interface with status bar, scrolling ticker, and clear data tables

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Database | MySQL (via `mysql-connector-python`) |
| Frontend | HTML5, CSS3 (Jinja2 templates) |
| Auth | Flask Sessions |

---

## 📁 Project Structure

```
trafficbase_management/
├── app.py                 # Flask application — routes, DB logic, session handling
├── style.css              # Global stylesheet (dark enforcement theme)
├── index.html             # Dashboard / Command Center
├── login.html             # Officer login page
├── add_violation.html     # Log new violation form
└── search.html            # Vehicle violation history lookup

## 🗄 Database Schema

The app expects a MySQL database named `traffic_db` with the following tables:

```sql
-- Officers (authenticated users)
CREATE TABLE Officers (
    officer_id    INT AUTO_INCREMENT PRIMARY KEY,
    officer_name  VARCHAR(100),
    badge_number  VARCHAR(20) UNIQUE,
    password      VARCHAR(255),
    station       VARCHAR(100)
);

-- Vehicles
CREATE TABLE Vehicles (
    vehicle_id     INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(20) UNIQUE,
    owner_name     VARCHAR(100),
    owner_phone    VARCHAR(20)
);

-- Violation Types
CREATE TABLE Violations (
    violation_id   INT AUTO_INCREMENT PRIMARY KEY,
    violation_type VARCHAR(100),
    fine_amount    DECIMAL(10,2)
);

-- Records (links everything together)
CREATE TABLE Records (
    record_id      INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id     INT,
    violation_id   INT,
    officer_id     INT,
    violation_date DATETIME,
    location       VARCHAR(255),
    FOREIGN KEY (vehicle_id)   REFERENCES Vehicles(vehicle_id),
    FOREIGN KEY (violation_id) REFERENCES Violations(violation_id),
    FOREIGN KEY (officer_id)   REFERENCES Officers(officer_id)
);
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/karthick357/trafficbase_management.git
cd trafficbase_management
```

### 2. Install dependencies
```bash
pip install flask mysql-connector-python
```

### 3. Configure the database

Update the `get_db()` function in `app.py` with your MySQL credentials:
```python
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_mysql_user",
        password="your_password",
        database="traffic_db"
    )
```

Then create the `traffic_db` database and run the schema above.

### 4. Set up the Flask template folder

Move the HTML files into a `templates/` folder (Flask convention):
```bash
mkdir templates
mv *.html templates/
```

Move `style.css` into the static folder:
```bash
mkdir -p static
mv style.css static/
```

### 5. Run the app
```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## 🔐 Default Login

Add officer records directly to the `Officers` table in MySQL to create accounts:
```sql
INSERT INTO Officers (officer_name, badge_number, password, station)
VALUES ('Officer Name', 'TF-001', 'yourpassword', 'Central Station');
```

---

## 📌 Supported Violation Types

Speeding · Signal Jump · No Helmet · No Seatbelt · DUI / Drunk Driving · Wrong Lane · No Parking Zone · Wrong-Way Driving · Mobile Phone Use · Overloading · Other

---

## 📄 License

For authorized enforcement use only. Unauthorized access is prohibited.

---

> Built with Flask & MySQL · © 2025 traffic_case_tracker
