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

tables = ["Grades", "Assessments", "Consultations", "Groups", "Specializations", "Studies", "Subjects", "Surveys", "Teachers", "Teachings"] 

data_dir = "/data/time1"

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


for table in tables:
    file_name = table.lower() + ".csv"
    file_path = os.path.join(data_dir, file_name)
    bulk_insert(file_path, table)

conn.close()

