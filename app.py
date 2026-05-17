from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)

# -----------------------------
# SECRET KEY CONFIG
# -----------------------------
# Local fallback is used only when SECRET_KEY is not set in environment variables.
app.secret_key = os.getenv("SECRET_KEY", "lnscarz_secret_key_change_later")


# -----------------------------
# APP CONFIG
# -----------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads", "cars")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


# -----------------------------
# DATABASE CONFIG
# -----------------------------
# Local default:
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=
# DB_NAME=lnscarz_db
# DB_PORT=3306
#
# Live Render/FreeSQLDatabase:
# Set these values in Render Environment Variables.
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "lnscarz_db"),
    "port": int(os.getenv("DB_PORT", "3306")),
}


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print("Database connection error:", e)
        raise


def admin_required():
    return "admin_id" in session


# -----------------------------
# PUBLIC PAGES
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/cars")
def cars():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    search = request.args.get("search", "").strip()
    brand = request.args.get("brand", "").strip()
    model = request.args.get("model", "").strip()
    body_type = request.args.get("body_type", "").strip()
    condition = request.args.get("condition", "").strip()
    transmission = request.args.get("transmission", "").strip()
    fuel_type = request.args.get("fuel_type", "").strip()
    colour = request.args.get("colour", "").strip()
    min_price = request.args.get("min_price", "").strip()
    max_price = request.args.get("max_price", "").strip()
    sort = request.args.get("sort", "latest").strip()

    query = "SELECT * FROM sell_requests WHERE status = 'Approved'"
    values = []

    if search:
        query += """
            AND (
                vehicle_brand LIKE %s OR
                vehicle_model LIKE %s OR
                manufacture_year LIKE %s OR
                fuel_type LIKE %s OR
                transmission LIKE %s
            )
        """
        values.extend([
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ])

    if brand:
        query += " AND vehicle_brand = %s"
        values.append(brand)

    if model:
        query += " AND vehicle_model = %s"
        values.append(model)

    if body_type:
        query += " AND body_type = %s"
        values.append(body_type)

    if condition:
        query += " AND vehicle_condition LIKE %s"
        values.append(f"%{condition}%")

    if transmission:
        query += " AND transmission = %s"
        values.append(transmission)

    if fuel_type:
        query += " AND fuel_type = %s"
        values.append(fuel_type)

    if colour:
        query += " AND vehicle_colour = %s"
        values.append(colour)

    if min_price:
        query += " AND expected_price_min >= %s"
        values.append(min_price)

    if max_price:
        query += " AND expected_price_max <= %s"
        values.append(max_price)

    if sort == "price_high":
        query += " ORDER BY expected_price_max DESC"
    elif sort == "price_low":
        query += " ORDER BY expected_price_min ASC"
    elif sort == "year_new":
        query += " ORDER BY manufacture_year DESC"
    else:
        query += " ORDER BY id DESC"

    cursor.execute(query, values)
    cars = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT vehicle_brand
        FROM sell_requests
        WHERE status = 'Approved'
        AND vehicle_brand IS NOT NULL
        AND vehicle_brand != ''
        ORDER BY vehicle_brand
    """)
    brands = [row["vehicle_brand"] for row in cursor.fetchall()]

    cursor.execute("""
        SELECT DISTINCT vehicle_model
        FROM sell_requests
        WHERE status = 'Approved'
        AND vehicle_model IS NOT NULL
        AND vehicle_model != ''
        ORDER BY vehicle_model
    """)
    models = [row["vehicle_model"] for row in cursor.fetchall()]

    cursor.execute("""
        SELECT DISTINCT body_type
        FROM sell_requests
        WHERE status = 'Approved'
        AND body_type IS NOT NULL
        AND body_type != ''
        ORDER BY body_type
    """)
    body_types = [row["body_type"] for row in cursor.fetchall()]

    cursor.execute("""
        SELECT DISTINCT transmission
        FROM sell_requests
        WHERE status = 'Approved'
        AND transmission IS NOT NULL
        AND transmission != ''
        ORDER BY transmission
    """)
    transmissions = [row["transmission"] for row in cursor.fetchall()]

    cursor.execute("""
        SELECT DISTINCT fuel_type
        FROM sell_requests
        WHERE status = 'Approved'
        AND fuel_type IS NOT NULL
        AND fuel_type != ''
        ORDER BY fuel_type
    """)
    fuel_types = [row["fuel_type"] for row in cursor.fetchall()]

    cursor.execute("""
        SELECT DISTINCT vehicle_colour
        FROM sell_requests
        WHERE status = 'Approved'
        AND vehicle_colour IS NOT NULL
        AND vehicle_colour != ''
        ORDER BY vehicle_colour
    """)
    colours = [row["vehicle_colour"] for row in cursor.fetchall()]

    cursor.close()
    db.close()

    filters = {
        "search": search,
        "brand": brand,
        "model": model,
        "body_type": body_type,
        "condition": condition,
        "transmission": transmission,
        "fuel_type": fuel_type,
        "colour": colour,
        "min_price": min_price,
        "max_price": max_price,
        "sort": sort,
    }

    return render_template(
        "car.html",
        cars=cars,
        brands=brands,
        models=models,
        body_types=body_types,
        transmissions=transmissions,
        fuel_types=fuel_types,
        colours=colours,
        filters=filters,
    )


@app.route("/car-view/<int:request_id>")
def public_car_view(request_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM sell_requests WHERE id = %s AND status = 'Approved'",
        (request_id,)
    )
    car = cursor.fetchone()

    cursor.close()
    db.close()

    if car is None:
        return render_template("404.html"), 404

    return render_template("car-view.html", car=car)


@app.route("/car-details/<int:vehicle_id>")
def car_details_dynamic(vehicle_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
    vehicle = cursor.fetchone()

    cursor.close()
    db.close()

    if vehicle is None:
        return render_template("404.html"), 404

    return render_template("car-details.html", vehicle=vehicle)


@app.route("/car-details")
def car_details():
    return render_template("car-details.html")


@app.route("/sell")
def sell():
    return render_template("sell.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/brokering")
def brokering():
    return render_template("brokering.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/blog-details")
def blog_details():
    return render_template("blog-details.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# -----------------------------
# SELL YOUR CAR FORM SAVE
# -----------------------------
@app.route("/sell-request", methods=["POST"])
def sell_request():
    full_name = request.form.get("full_name", "").strip()
    nic_passport = request.form.get("nic_passport", "").strip()
    mobile_number = request.form.get("mobile_number", "").strip()
    whatsapp_number = request.form.get("whatsapp_number", "").strip()
    email = request.form.get("email", "").strip()
    district = request.form.get("district", "").strip()

    vehicle_brand = request.form.get("vehicle_brand", "").strip()
    vehicle_model = request.form.get("vehicle_model", "").strip()
    manufacture_year = request.form.get("manufacture_year", "").strip()
    mileage = request.form.get("mileage", "").strip()
    fuel_type = request.form.get("fuel_type", "").strip()
    transmission = request.form.get("transmission", "").strip()
    body_type = request.form.get("body_type", "").strip()
    vehicle_colour = request.form.get("vehicle_colour", "").strip()
    vehicle_condition = request.form.get("vehicle_condition", "").strip()
    previous_owners = request.form.get("previous_owners", "").strip()
    registration_number = request.form.get("registration_number", "").strip()

    expected_price_min = request.form.get("expected_price_min", "").strip()
    expected_price_max = request.form.get("expected_price_max", "").strip()
    insurance_status = request.form.get("insurance_status", "").strip()
    revenue_license_valid_until = request.form.get("revenue_license_valid_until", "").strip()
    fault_status = request.form.get("fault_status", "").strip()
    preferred_contact_method = request.form.get("preferred_contact_method", "").strip()
    notes = request.form.get("notes", "").strip()

    if not full_name or not nic_passport or not mobile_number or not district:
        flash("Please fill all required personal details.", "error")
        return redirect(url_for("sell"))

    if not vehicle_brand or not vehicle_model or not manufacture_year or not mileage:
        flash("Please fill all required vehicle details.", "error")
        return redirect(url_for("sell"))

    if not fuel_type or not transmission or not vehicle_condition:
        flash("Please fill all required vehicle information.", "error")
        return redirect(url_for("sell"))

    vehicle_image = None

    if "vehicle_image" in request.files:
        file = request.files["vehicle_image"]

        if file and file.filename != "":
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = datetime.now().strftime("%Y%m%d%H%M%S_") + filename
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)

                file.save(file_path)

                vehicle_image = "uploads/cars/" + unique_filename
            else:
                flash("Invalid image type. Please upload JPG, JPEG, PNG, or WEBP image.", "error")
                return redirect(url_for("sell"))

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO sell_requests (
            full_name,
            nic_passport,
            mobile_number,
            whatsapp_number,
            email,
            district,
            vehicle_brand,
            vehicle_model,
            manufacture_year,
            mileage,
            fuel_type,
            transmission,
            body_type,
            vehicle_colour,
            vehicle_condition,
            previous_owners,
            registration_number,
            vehicle_image,
            expected_price_min,
            expected_price_max,
            insurance_status,
            revenue_license_valid_until,
            fault_status,
            preferred_contact_method,
            notes
        )
        VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s
        )
        """,
        (
            full_name,
            nic_passport,
            mobile_number,
            whatsapp_number,
            email,
            district,
            vehicle_brand,
            vehicle_model,
            manufacture_year,
            mileage,
            fuel_type,
            transmission,
            body_type,
            vehicle_colour,
            vehicle_condition,
            previous_owners,
            registration_number,
            vehicle_image,
            expected_price_min,
            expected_price_max,
            insurance_status,
            revenue_license_valid_until,
            fault_status,
            preferred_contact_method,
            notes,
        ),
    )

    db.commit()
    cursor.close()
    db.close()

    flash(
        "Your vehicle sale request has been submitted successfully. Our team will contact you within 24 hours.",
        "success"
    )
    return redirect(url_for("sell"))


# -----------------------------
# CUSTOMER INQUIRY
# -----------------------------
@app.route("/submit-inquiry", methods=["POST"])
def submit_inquiry():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    message = request.form.get("message", "").strip()
    vehicle_id = request.form.get("vehicle_id", "").strip()

    if not name or not email or not message:
        flash("Please fill all required fields.", "error")
        return redirect(url_for("contact"))

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO inquiries (vehicle_id, name, email, phone, message)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (vehicle_id if vehicle_id else None, name, email, phone, message)
    )

    db.commit()
    cursor.close()
    db.close()

    flash("Inquiry submitted successfully.", "success")
    return redirect(url_for("contact"))


# -----------------------------
# ADMIN LOGIN
# -----------------------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
        admin = cursor.fetchone()

        cursor.close()
        db.close()

        if admin and check_password_hash(admin["password"], password):
            session["admin_id"] = admin["id"]
            session["admin_username"] = admin["username"]
            flash("Login successful.", "success")
            return redirect(url_for("admin_dashboard"))

        flash("Invalid username or password.", "error")

    return render_template("admin-login.html")


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("admin_login"))


# -----------------------------
# ADMIN DASHBOARD
# -----------------------------
@app.route("/admin/dashboard")
def admin_dashboard():
    if not admin_required():
        return redirect(url_for("admin_login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM vehicles")
    total_vehicles = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM inquiries")
    total_inquiries = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM sell_requests")
    total_sell_requests = cursor.fetchone()["total"]

    cursor.execute("SELECT * FROM inquiries ORDER BY id DESC LIMIT 5")
    latest_inquiries = cursor.fetchall()

    cursor.execute("SELECT * FROM sell_requests ORDER BY id DESC LIMIT 5")
    latest_sell_requests = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "admin-dashboard.html",
        total_vehicles=total_vehicles,
        total_inquiries=total_inquiries,
        total_sell_requests=total_sell_requests,
        latest_inquiries=latest_inquiries,
        latest_sell_requests=latest_sell_requests
    )


# -----------------------------
# ADMIN REPORTS
# -----------------------------
@app.route("/admin/reports")
def admin_reports():
    if not admin_required():
        return redirect(url_for("admin_login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM sell_requests")
    total_sell_requests = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM sell_requests WHERE status = 'Approved'")
    approved_cars = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM sell_requests WHERE status = 'Pending'")
    pending_requests = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM sell_requests WHERE status = 'Rejected'")
    rejected_requests = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM sell_requests WHERE status = 'Contacted'")
    contacted_requests = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM sell_requests WHERE status = 'Completed'")
    completed_requests = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM inquiries")
    total_inquiries = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT status, COUNT(*) AS total
        FROM sell_requests
        GROUP BY status
        ORDER BY total DESC
    """)
    status_summary = cursor.fetchall()

    cursor.execute("""
        SELECT vehicle_brand, COUNT(*) AS total
        FROM sell_requests
        WHERE vehicle_brand IS NOT NULL AND vehicle_brand != ''
        GROUP BY vehicle_brand
        ORDER BY total DESC
        LIMIT 10
    """)
    brand_summary = cursor.fetchall()

    cursor.execute("""
        SELECT DATE(created_at) AS request_date, COUNT(*) AS total
        FROM sell_requests
        GROUP BY DATE(created_at)
        ORDER BY request_date DESC
        LIMIT 10
    """)
    daily_summary = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "admin-reports.html",
        total_sell_requests=total_sell_requests,
        approved_cars=approved_cars,
        pending_requests=pending_requests,
        rejected_requests=rejected_requests,
        contacted_requests=contacted_requests,
        completed_requests=completed_requests,
        total_inquiries=total_inquiries,
        status_summary=status_summary,
        brand_summary=brand_summary,
        daily_summary=daily_summary
    )


# -----------------------------
# ADMIN VEHICLE CRUD
# -----------------------------
@app.route("/admin/vehicles")
def admin_vehicles():
    if not admin_required():
        return redirect(url_for("admin_login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM vehicles ORDER BY id DESC")
    vehicles = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("admin-vehicles.html", vehicles=vehicles)


@app.route("/admin/vehicles/add", methods=["POST"])
def add_vehicle():
    if not admin_required():
        return redirect(url_for("admin_login"))

    make = request.form.get("make", "").strip()
    model = request.form.get("model", "").strip()
    year = request.form.get("year", "").strip()
    mileage = request.form.get("mileage", "").strip()
    transmission = request.form.get("transmission", "").strip()
    fuel_type = request.form.get("fuel_type", "").strip()
    colour = request.form.get("colour", "").strip()
    price = request.form.get("price", "").strip()
    description = request.form.get("description", "").strip()
    image = request.form.get("image", "").strip()
    status = request.form.get("status", "").strip()

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO vehicles
        (make, model, year, mileage, transmission, fuel_type, colour, price, description, image, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (make, model, year, mileage, transmission, fuel_type, colour, price, description, image, status)
    )

    db.commit()
    cursor.close()
    db.close()

    flash("Vehicle added successfully.", "success")
    return redirect(url_for("admin_vehicles"))


@app.route("/admin/vehicles/update/<int:vehicle_id>", methods=["POST"])
def update_vehicle(vehicle_id):
    if not admin_required():
        return redirect(url_for("admin_login"))

    make = request.form.get("make", "").strip()
    model = request.form.get("model", "").strip()
    year = request.form.get("year", "").strip()
    mileage = request.form.get("mileage", "").strip()
    transmission = request.form.get("transmission", "").strip()
    fuel_type = request.form.get("fuel_type", "").strip()
    colour = request.form.get("colour", "").strip()
    price = request.form.get("price", "").strip()
    description = request.form.get("description", "").strip()
    image = request.form.get("image", "").strip()
    status = request.form.get("status", "").strip()

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE vehicles
        SET make = %s,
            model = %s,
            year = %s,
            mileage = %s,
            transmission = %s,
            fuel_type = %s,
            colour = %s,
            price = %s,
            description = %s,
            image = %s,
            status = %s
        WHERE id = %s
        """,
        (make, model, year, mileage, transmission, fuel_type, colour, price, description, image, status, vehicle_id)
    )

    db.commit()
    cursor.close()
    db.close()

    flash("Vehicle updated successfully.", "success")
    return redirect(url_for("admin_vehicles"))


@app.route("/admin/vehicles/delete/<int:vehicle_id>", methods=["POST"])
def delete_vehicle(vehicle_id):
    if not admin_required():
        return redirect(url_for("admin_login"))

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("DELETE FROM vehicles WHERE id = %s", (vehicle_id,))

    db.commit()
    cursor.close()
    db.close()

    flash("Vehicle deleted successfully.", "success")
    return redirect(url_for("admin_vehicles"))


# -----------------------------
# ADMIN INQUIRIES
# -----------------------------
@app.route("/admin/inquiries")
def admin_inquiries():
    if not admin_required():
        return redirect(url_for("admin_login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT inquiries.*, vehicles.make, vehicles.model
        FROM inquiries
        LEFT JOIN vehicles ON inquiries.vehicle_id = vehicles.id
        ORDER BY inquiries.id DESC
        """
    )

    inquiries = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("admin-inquiries.html", inquiries=inquiries)


# -----------------------------
# ADMIN SELL REQUESTS
# -----------------------------
@app.route("/admin/sell-requests")
def admin_sell_requests():
    if not admin_required():
        return redirect(url_for("admin_login"))

    search = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()
    brand = request.args.get("brand", "").strip()

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    query = "SELECT * FROM sell_requests WHERE 1=1"
    values = []

    if search:
        query += """
            AND (
                full_name LIKE %s OR
                mobile_number LIKE %s OR
                whatsapp_number LIKE %s OR
                email LIKE %s OR
                district LIKE %s OR
                vehicle_brand LIKE %s OR
                vehicle_model LIKE %s OR
                registration_number LIKE %s
            )
        """
        search_value = f"%{search}%"
        values.extend([
            search_value,
            search_value,
            search_value,
            search_value,
            search_value,
            search_value,
            search_value,
            search_value
        ])

    if status:
        query += " AND status = %s"
        values.append(status)

    if brand:
        query += " AND vehicle_brand = %s"
        values.append(brand)

    query += " ORDER BY id DESC"

    cursor.execute(query, values)
    sell_requests = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT vehicle_brand
        FROM sell_requests
        WHERE vehicle_brand IS NOT NULL AND vehicle_brand != ''
        ORDER BY vehicle_brand
    """)
    brands = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "admin-sell-requests.html",
        sell_requests=sell_requests,
        brands=brands,
        filters={
            "search": search,
            "status": status,
            "brand": brand
        }
    )


@app.route("/admin/sell-requests/view/<int:request_id>")
def view_sell_request(request_id):
    if not admin_required():
        return redirect(url_for("admin_login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sell_requests WHERE id = %s", (request_id,))
    sell_request = cursor.fetchone()

    cursor.close()
    db.close()

    if sell_request is None:
        return render_template("404.html"), 404

    return render_template("admin-sell-request-view.html", sell_request=sell_request)


@app.route("/admin/sell-requests/status/<int:request_id>", methods=["POST"])
def update_sell_request_status(request_id):
    if not admin_required():
        return redirect(url_for("admin_login"))

    status = request.form.get("status", "").strip()

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE sell_requests SET status = %s WHERE id = %s",
        (status, request_id)
    )

    db.commit()
    cursor.close()
    db.close()

    flash("Sell request status updated successfully.", "success")
    return redirect(url_for("admin_sell_requests"))


@app.route("/admin/sell-requests/delete/<int:request_id>", methods=["POST"])
def delete_sell_request(request_id):
    if not admin_required():
        return redirect(url_for("admin_login"))

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("DELETE FROM sell_requests WHERE id = %s", (request_id,))

    db.commit()
    cursor.close()
    db.close()

    flash("Sell request deleted successfully.", "success")
    return redirect(url_for("admin_sell_requests"))


# -----------------------------
# ERROR HANDLERS
# -----------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("404.html"), 500


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "False").lower() == "true"
    )