from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL

# Azure SQL DB connection string
import pyodbc


connection_string = URL.create(
    "mssql+pyodbc",
    username="admin1@shopserv1",
    password="anumitha@123",
    host="shopserv1.database.windows.net",
    port=1433,
    database="shopdb1",
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "encrypt": "yes",
        "trustServerCertificate": "no",
        "connection timeout": "30"
    }
)

engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
