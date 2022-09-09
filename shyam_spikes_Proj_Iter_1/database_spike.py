import sqlite3

# Create/Connect to a database
connect_db = sqlite3.connect('tasks.db')

# Create cusror
cursor = connect_db.cursor()

# Create Table
# cursor.execute(""" CREATE TABLE tasks (
#             task_name text,
#             task_description text,
#             stroy_points text,
#             priority text,
#             status text,
#             assigned_to text, 
#             tag text
#             )""")

def create():
    # Create/Connect to a database
    connect_db = sqlite3.connect('tasks.db')
    # Create cusror
    cursor = connect_db.cursor()

    connect_db.execute("INSERT INTO tasks VALUES (:task_name, :task_description, :stroy_points, :priority, :status, :assigned_to, :tag)", 
                    {
                        'task_name'
                    }
    )


# Commit changes
connect_db.commit()

# Close Connnection
connect_db.close()

