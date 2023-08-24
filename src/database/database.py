import sqlite3
import json
from data import USER_DATA, DATAFRAME
from utilities.utils import *
# Create a SQLite3 database and tables

def connectDatabase(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    return cursor, conn


def create_tables(database):
    try:
        cursor , conn = connectDatabase(database)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student TEXT ,
                project TEXT,
                scenario TEXT,
                createdDate DATE,
                user_data TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dataframe (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                reference_df BLOB,
                student_df BLOB,
                status_df BLOB,
                FOREIGN KEY (student_id) REFERENCES student (student_id)
            )
        ''')
        conn.commit()
        
    finally:
        conn.close()

def insertHistory(database):
    project = USER_DATA["headingData"]["project_name"]
    scenario = USER_DATA["visualizationData"]["scenario"]
    student = USER_DATA["informationData"]["student_name"]
    reference_df_list = serializeDataframeList(DATAFRAME["reference_df"])
    student_df_list = serializeDataframeList(DATAFRAME["student_df"])
    status_df_list = serializeDataframeList(DATAFRAME["status_df"])
    userData = serialize(USER_DATA)
    createdDate = current_date()

    cursor , conn = connectDatabase(database)  
    selectedStudent_id = selectStudentID(cursor, project, scenario, student)
    if selectedStudent_id != None :
        selectedStudent_id = selectedStudent_id[0]
        updateStudent(cursor, project, scenario, createdDate, userData, selectedStudent_id )
        updateDataframe(cursor, reference_df_list, student_df_list, status_df_list , selectedStudent_id)

    else:
        insertStudent(cursor, student, project, scenario, createdDate, userData)
        student_id = selectStudentID(cursor, project, scenario, student)
        student_id = student_id[0]
        insertDataframe(cursor, student_id, reference_df_list, student_df_list, status_df_list )
    conn.commit()     
    conn.close()
    return True

def insertStudent(cursor, student, project, scenario, createdDate, userData):
    cursor.execute('''
        INSERT INTO student (student, project, scenario, createdDate, user_data)
        VALUES (?, ?, ?, ?, ?)
    ''', (student, project, scenario, createdDate, userData))
    print("Inserted Student")
    return None

def insertDataframe(cursor, student_id, reference_df_list, student_df_list, status_df_list):
    for i in range(len(reference_df_list)):
        cursor.execute('''
            INSERT INTO dataframe (student_id, reference_df, student_df, status_df)
            VALUES (?, ? ,?, ?)
        ''', (student_id, reference_df_list[i], student_df_list[i], status_df_list[i]))
    print("Inserted Dataframe")
    return None

def selectStudentID(cursor, project, scenario, student):
    cursor.execute('''
        SELECT student_id 
        FROM student
        WHERE project = ? AND
        scenario = ? AND
        student = ?
    ''', (project, scenario, student))
    selectedStudent_id = cursor.fetchone()
    return selectedStudent_id

def updateStudent(cursor, project, scenario, createdDate, userData, student_id):
    cursor.execute("UPDATE student SET project = ?, scenario = ? , createdDate = ?, user_data = ? WHERE student_id = ?", (project, scenario, createdDate, userData, student_id))
    print("Updated Student")
    return None

def updateDataframe(cursor, reference_df_list, student_df_list, status_df_list, student_id):
    for i in range(len(reference_df_list)):
        cursor.execute("UPDATE dataframe SET reference_df = ?, student_df = ? , status_df = ? WHERE student_id = ?", (reference_df_list[i], student_df_list[i], status_df_list[i], student_id))
        print("Updated Dateframe")
    return None

def selectAllProject(database):
    cursor , conn = connectDatabase(database)   
    cursor.execute('''
        SELECT DISTINCT project
        FROM student;
    ''')
    projects = cursor.fetchall()
    conn.commit()     
    conn.close()
    return projects

def retreiveHistory(database):
    cursor , conn = connectDatabase(database)   
    cursor.execute('''
        SELECT student_id, project, scenario, student, createdDate
        FROM student
    ''')
    histories = cursor.fetchall()
    conn.commit()     
    conn.close()
    return histories 
    # except Exception as e:
    #     print(e)
    #     return False

def retreiveSelectedHistory(database, selectedProject):
    cursor , conn = connectDatabase(database)   
    cursor.execute('''
        SELECT student_id, project, scenario, student, createdDate
        FROM student
        WHERE project = ?
    ''', (selectedProject,))
    histories = cursor.fetchall()
    conn.commit()     
    conn.close()
    return histories 
    # except Exception as e:
    #     print(e)
    #     return False

def deleteHistory(database, student_id):
    cursor , conn = connectDatabase(database)
    cursor.execute('''
        DELETE FROM student WHERE student_id = ?
    ''', (student_id,))
    cursor.execute("UPDATE student SET student_id = student_id - 1 WHERE student_id > ?", (student_id,))

    conn.commit()     
    conn.close()

def retrieveSelectedDataframeList(database, student_id):
    cursor , conn = connectDatabase(database)
    cursor.execute('SELECT reference_df, student_df, status_df  FROM dataframe WHERE student_id = ?', (student_id,))
    rows = cursor.fetchall()
    reference_df = [ deserializeDataframe(row[0]) for row in rows]
    student_df = [deserializeDataframe(row[1]) for row in rows]
    status_df = [deserializeDataframe(row[2]) for row in rows]

    conn.commit()     
    conn.close()
    return reference_df, student_df, status_df
