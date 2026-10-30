import sqlite3

emails = input("Enter emails separated by commas: ").split(",")

emails = [email.strip() for email in emails if email.strip()]

conn = sqlite3.connect("database.db")

for email in emails:
    user = conn.execute(
        "SELECT id, name FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    if user:
        user_id = user[0]
        name = user[1]

        conn.execute(
            "DELETE FROM blood_reports WHERE user_id = ?",
            (user_id,)
        )

        conn.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )

        print(f"Deleted: {name} ({email})")

    else:
        print(f"Not found: {email}")

conn.commit()
conn.close()

print("Finished.")