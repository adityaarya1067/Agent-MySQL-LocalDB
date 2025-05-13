import sqlite3

connection = sqlite3.connect("student.db")

cursor = connection.cursor()

table_info="""
create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT)

"""

cursor.execute(table_info)

cursor.execute('''INSERT INTO STUDENT VALUES('Aditya','Data Science','A',98)'''),
cursor.execute("INSERT INTO STUDENT VALUES('Sneha', 'Machine Learning', 'B', 91)"),
cursor.execute("INSERT INTO STUDENT VALUES('Rohan', 'Artificial Intelligence', 'A', 85)"),
cursor.execute("INSERT INTO STUDENT VALUES('Meera', 'Data Science', 'C', 78)"),
cursor.execute("INSERT INTO STUDENT VALUES('Karan', 'Cyber Security', 'B', 88)"),
cursor.execute("INSERT INTO STUDENT VALUES('Isha', 'Computer Vision', 'A', 95)"),
cursor.execute("INSERT INTO STUDENT VALUES('Yash', 'Natural Language Processing', 'C', 82)"),
cursor.execute("INSERT INTO STUDENT VALUES('Priya', 'Deep Learning', 'B', 89)"),
cursor.execute("INSERT INTO STUDENT VALUES('Amit', 'Data Engineering', 'A', 76)"),
cursor.execute("INSERT INTO STUDENT VALUES('Neha', 'Big Data', 'B', 93)"),
cursor.execute("INSERT INTO STUDENT VALUES('Arjun', 'Reinforcement Learning', 'C', 87)")

print("The inserted records are")
data=cursor.execute("Select * from Student")

for row in data:
  print(row)

connection.commit()
connection.close()
