from flask import Flask, redirect, render_template, request, url_for
import mysql.connector

app = Flask(__name__, template_folder='Templates')

# MySQL database configuration
db_config = {
    'user': 'root',
    'password': 'ToughPassword1!',
    'host': 'localhost',
    'database': 'ToDoList'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM todo")
    todo_list = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("form.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todo (title, complete) VALUES (%s, %s)", (title, False))
    conn.commit()
    
    cursor.close()
    conn.close()
    return redirect(url_for("home"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE todo SET complete = NOT complete WHERE id = %s", (todo_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM todo WHERE id = %s", (todo_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
