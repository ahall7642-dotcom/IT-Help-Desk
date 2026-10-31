
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# Connect to the database
def get_db_connection():
    connection = sqlite3.connect("tickets.db")
    connection.row_factory = sqlite3.Row
    return connection


# Create the tickets table
def create_table():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            issue TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'Open'
        )
    """)

    connection.commit()
    connection.close()


# Homepage
@app.route("/")
def home():
    return render_template("index.html")


# Submit a ticket
@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        name = request.form["name"]
        issue = request.form["issue"]
        description = request.form["description"]

        connection = get_db_connection()

        connection.execute(
            "INSERT INTO tickets (name, issue, description) VALUES (?, ?, ?)",
            (name, issue, description)
        )

        connection.commit()
        connection.close()

        return redirect("/tickets")

    return render_template("submit.html")


# View all tickets
@app.route("/tickets")
def tickets():
    connection = get_db_connection()

    all_tickets = connection.execute(
        "SELECT * FROM tickets"
    ).fetchall()

    connection.close()

    return render_template(
        "tickets.html",
        tickets=all_tickets
    )


# Update ticket status
@app.route("/update_status/<int:ticket_id>", methods=["POST"])
def update_status(ticket_id):
    new_status = request.form["status"]

    if new_status not in ["Open", "In Progress", "Resolved"]:
        return "Invalid ticket status", 400

    connection = get_db_connection()

    connection.execute(
        "UPDATE tickets SET status = ? WHERE id = ?",
        (new_status, ticket_id)
    )

    connection.commit()
    connection.close()

    return redirect("/tickets")


# Start the application
if __name__ == "__main__":
    create_table()
    app.run(debug=True)

