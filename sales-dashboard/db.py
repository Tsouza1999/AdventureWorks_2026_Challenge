import pyodbc
import pandas as pd

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=AdventureWorks2019;"
        "Trusted_Connection=yes;"
    )
    return conn


def load_sales_data(query_path: str) -> pd.DataFrame:
    conn = get_connection()

    with open(query_path, "r", encoding="utf-8") as file:
        query = file.read()

    df = pd.read_sql(query, conn)
    conn.close()

    return df
