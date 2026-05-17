import os
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash


# -----------------------------
# DATABASE CONFIG
# -----------------------------
# Local default values:
# host     = localhost
# user     = root
# password = empty
# database = lnscarz_db
#
# For FreeSQLDatabase / Render, set these as environment variables:
# DB_HOST
# DB_USER
# DB_PASSWORD
# DB_NAME
# DB_PORT

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "lnscarz_db"),
    "port": int(os.getenv("DB_PORT", "3306")),
}


def create_admin_user():
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()

        username = "admin"
        password = "admin123"

        hashed_password = generate_password_hash(password)

        cursor.execute("DELETE FROM admins WHERE username = %s", (username,))

        cursor.execute(
            """
            INSERT INTO admins (username, password)
            VALUES (%s, %s)
            """,
            (username, hashed_password)
        )

        db.commit()

        cursor.close()
        db.close()

        print("Admin user created successfully.")
        print("Username: admin")
        print("Password: admin123")

    except Error as e:
        print("Database error:")
        print(e)


if __name__ == "__main__":
    create_admin_user()