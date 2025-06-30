from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

# 📦 Load students from file
def load_students():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# 💾 Save students to file
def save_students(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# 🔄 In-memory data
students = load_students()

# ✅ Get students (optional class filter)
@app.route("/students", methods=["GET"])
def get_students():
    class_filter = request.args.get("class")
    if class_filter:
        filtered = [s for s in students if s["class"] == class_filter]
        return jsonify(filtered)
    return jsonify(students)

# ✅ Add new student
@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    required = {"name", "father", "roll", "section", "class"}
    if not required.issubset(data):
        return jsonify({"error": "Missing fields"}), 400

    students.append(data)
    save_students(students)
    return jsonify({"message": "Student added", "student": data})

# 🔍 Search student by name
@app.route("/search", methods=["POST"])
def search_students():
    keyword = request.json.get("name", "").lower()
    results = [s for s in students if keyword in s["name"].lower()]
    return jsonify(results)

# 🏁 Run
if __name__ == "__main__":
    app.run(debug=True, port=5000)
