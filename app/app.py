from flask import Flask, request, jsonify
import csv
import os


app = Flask(__name__)

# Шлях до файлу CSV
CSV_FILE = "students.csv"

# Функція для читання студентів з файлу CSV
def read_students():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)
# Функція для запису студентів до файлу CSV
def write_students(students):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["id", "first_name", "last_name", "age"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)

# Маршрут для отримання списку всіх студентів
@app.route("/students", methods=["GET"])
def get_students():
    students = read_students()
    return jsonify(students)

# Маршрут для отримання студента за ID
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student_by_id(student_id):
    students = read_students()
    student = next((s for s in students if int(s["id"]) == student_id), None)
    if not student:
        return jsonify({"error": "No student with this ID was found"}), 404
    return jsonify(student)


# Маршрут для отримання студентів за прізвищем
@app.route("/lastname/<string:last_name>", methods=["GET"])
def get_student_by_last_name(last_name):
    students = read_students()
    name_students = [s for s in students if s["last_name"] == last_name]
    if not name_students:
        return jsonify({"error": "No students with this last name were found"}), 404
    return jsonify(name_students)

# Маршрут для додавання нового студента
@app.route("/students/new", methods=["POST"])
def add_student():
    data = request.json
    if not all(key in data for key in ["first_name", "last_name", "age"]):
        return jsonify({"error": "All fields first_name, last_name, age must be filled"}), 400
    
    students = read_students()
    next_id = max([int(s["id"]) for s in students], default=0) + 1
    
    new_student = {
        "id": next_id,
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "age": data["age"]
    }
    students.append(new_student)
    write_students(students)
    return jsonify(new_student), 201

# Маршрут для оновлення студента за ID
@app.route("/students/update/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.json
    if not all(key in data for key in ["first_name", "last_name", "age"]):
        return jsonify({"error": "All fields first_name, last_name, age must be filled"}), 400
    
    students = read_students()
    student = next((s for s in students if int(s["id"]) == student_id), None)
    if not student:
        return jsonify({"error": "No student with this ID was found"}), 404
    
    student["first_name"] = data["first_name"]
    student["last_name"] = data["last_name"]
    student["age"] = data["age"]
    
    write_students(students)
    return jsonify(student)

# Маршрут для часткового оновлення студента за ID
@app.route("/students/ageupdate/<int:student_id>", methods=["PATCH"])
def update_student_age(student_id):
    data = request.json
    
    if "age" not in data:
        return jsonify({"error": "The age field must be specified"}), 400
    
    students = read_students()
    student = next((s for s in students if int(s["id"]) == student_id), None)
    if not student:
        return jsonify({"error": "No student with this ID was found"}), 404
    
    student["age"] = data["age"]
    
    write_students(students)
    return jsonify(student)

# Маршрут для видалення студента за ID
@app.route("/delete/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    students = read_students()
    student = next((s for s in students if int(s["id"]) == student_id), None)
    if not student:
        return jsonify({"error": "No student with this ID was found"}), 404
    
    students.remove(student)
    write_students(students)
    return jsonify({"message": "The student was successfully deleted"}), 200

# Обробник помилок для 404 (не знайдено)
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Page not found"}), 404

# Запуск Flask сервера
if __name__ == "__main__":
    app.run(debug=True)