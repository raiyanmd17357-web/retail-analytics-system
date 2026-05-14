import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Raiyan@4328",
    database="retail_analytics"
)

cursor = conn.cursor()

query = """
INSERT INTO visitors
(people_count, object_count, detected_objects, timestamp)
VALUES (%s, %s, %s, NOW())
"""

values = (
    5,
    3,
    "bottle, phone, chair"
)

cursor.execute(query, values)

conn.commit()

print("Data Inserted Successfully")