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

tables = ["Grades", "Assessments", "Consultations", "Groups", "Specializations", "Studies", "Subjects", "Surveys", "Teachers", "Teachings", "Students"]
times = ["time1", "time2"]

data_dir = "/data"
def bulk_insert(file_path, table_name):
    query = f"""
    BULK INSERT {table_name}
    FROM '{file_path}'
    WITH (
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\\n',
        FIRSTROW = 2
    );
    """
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.commit()
    print(f"Data from {file_path} inserted into {table_name}")

for time in times:
    for table in tables:
        file_name = table.lower() + ".csv"
        file_path = os.path.join(data_dir, time, file_name)
        bulk_insert(file_path, table)
    print(f"Data for {time} loaded successfully")

conn.close()

