import os
import pyodbc

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=localhost,1433;'
    'DATABASE=SCHOOL;'
    'UID=sa;'
    'PWD=testpass123$;'
    'TrustServerCertificate=yes;'
)

tables = ["Teachers", "Students", "Consultations", "Specializations", "Groups", "Studies", "Subjects", "Teachings", "Grades", "Surveys", "Assessments"]
times = ["time1", "time2"]

data_dir = "/data"

def bulk_insert(file_path, table_name):
    cursor = conn.cursor()

    cursor.execute(f"EXEC xp_fileexist '{file_path}'")
    file_exists = cursor.fetchone()[0]
    if not file_exists:
        print(f"File {file_path} not found, skip...")
        return

    query = f"""
    BULK INSERT {table_name}
    FROM '{file_path}'
    WITH (
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\\n',
        FIRSTROW = 2
    );
    """
    cursor.execute(query)
    cursor.commit()

for time in times:
    for table in tables:
        file_name = table.lower() + ".csv"
        file_path = os.path.join(data_dir, time, file_name)
        bulk_insert(file_path, table)
    print(f"Data for {time} loaded successfully")

conn.close()
