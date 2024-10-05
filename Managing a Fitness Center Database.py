#Task 1 Setting Up the Flask Environment and Database Connection
# Using the terminal, prepare the fallowing
#mkdir fitness_center
#cd fitness_center

#python -m venv venv
#venv\Scripts\activate

#pip install Flask Flask-Marshmallow mysql-connector-python

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Fitness Center API'

if __name__ == '__main__':
    app.run(debug=True)

import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="kyletrey",
        database="fitness_center_db"
    )

#Task 2 Implementing CRUD Operations for Members
from flask import request, jsonify
from config import connect_db

#Add Member
@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    connection = connect_db()
    cursor = connection.cursor()
    query = "INSERT INTO Members (name, email, phone) VALUES (%s, %s, %s)"
    cursor.execute(query, (data['name'], data['email'], data['phone']))
    connection.commit()
    cursor.close()
    return jsonify({'message': 'Member added successfully'}), 201

#Retrieve Member
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Members WHERE id = %s", (id,))
    member = cursor.fetchone()
    cursor.close()
    if member:
        return jsonify(member)
    else:
        return jsonify({'message': 'Member not found'}), 404

#Update Member
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()
    connection = connect_db()
    cursor = connection.cursor()
    query = "UPDATE Members SET name = %s, email = %s, phone = %s WHERE id = %s"
    cursor.execute(query, (data['name'], data['email'], data['phone'], id))
    connection.commit()
    cursor.close()
    return jsonify({'message': 'Member updated successfully'})

#Delete Member
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Members WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    return jsonify({'message': 'Member deleted successfully'})

#Task 3 Managing Workout Sessions
#Schedule Workout Session
@app.route('/sessions', methods=['POST'])
def schedule_session():
    data = request.get_json()
    connection = connect_db()
    cursor = connection.cursor()
    query = "INSERT INTO WorkoutSessions (member_id, session_date, duration) VALUES (%s, %s, %s)"
    cursor.execute(query, (data['member_id'], data['session_date'], data['duration']))
    connection.commit()
    cursor.close()
    return jsonify({'message': 'Session scheduled successfully'}), 201

#Update Workout Session
@app.route('/sessions/<int:id>', methods=['PUT'])
def update_session(id):
    data = request.get_json()
    connection = connect_db()
    cursor = connection.cursor()
    query = "UPDATE WorkoutSessions SET session_date = %s, duration = %s WHERE id = %s"
    cursor.execute(query, (data['session_date'], data['duration'], id))
    connection.commit()
    cursor.close()
    return jsonify({'message': 'Session updated successfully'})

#View Workout Sessions for Member
@app.route('/members/<int:id>/sessions', methods=['GET'])
def get_member_sessions(id):
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM WorkoutSessions WHERE member_id = %s", (id,))
    sessions = cursor.fetchall()
    cursor.close()
    return jsonify(sessions)


