import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rithi@123",
    database="digital_campus"
)

cursor = db.cursor()

print("Connected to MySQL successfully")