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

def get_columns(cursor, table_name):
    cursor.execute(f"""
    SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = '{table_name}'
    """)
    columns = [row[0] for row in cursor.fetchall()]

    cursor.execute(f"""
    SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    WHERE TABLE_NAME = '{table_name}' AND CONSTRAINT_NAME LIKE 'PK_%'
    """)
    primary_key = cursor.fetchone()[0]

    return columns, primary_key

def bulk_insert(file_path, table_name):
    temp_table = f"#{table_name}Temp"
    cursor = conn.cursor()

    columns, primary_key = get_columns(cursor, table_name)
    non_key_columns = [col for col in columns if col != primary_key]

    cursor.execute(f"EXEC xp_fileexist '{file_path}'")
    file_exists = cursor.fetchone()[0]
    if not file_exists:
        print(f"File {file_path} not found, skip...")
        return

    cursor.execute(f"SELECT TOP 0 * INTO {temp_table} FROM {table_name}")
    conn.commit()

    query = f"""
    BULK INSERT {temp_table}
    FROM '{file_path}'
    WITH (
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\\n',
        FIRSTROW = 2
    );
    """
    cursor.execute(query)
    cursor.commit()

    update_set = ", ".join([f"target.{col} = source.{col}" for col in non_key_columns])
    insert_columns = ", ".join(columns)
    insert_values = ", ".join([f"source.{col}" for col in columns])

    merge_query = f"""
    MERGE {table_name} AS target
    USING {temp_table} AS source
    ON target.{primary_key} = source.{primary_key}
    WHEN MATCHED THEN 
        UPDATE SET {update_set}
    WHEN NOT MATCHED THEN 
        INSERT ({insert_columns})
        VALUES ({insert_values});
    """
    cursor.execute(merge_query)
    cursor.commit()

    cursor.execute(f"DROP TABLE {temp_table}")
    cursor.commit()

for time in times:
    for table in tables:
        file_name = table.lower() + ".csv"
        file_path = os.path.join(data_dir, time, file_name)
        bulk_insert(file_path, table)
    print(f"Data for {time} loaded successfully")

conn.close()
