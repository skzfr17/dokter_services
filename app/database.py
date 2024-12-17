# doctor_services/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "mysql+mysqlconnector://root:@localhost/db_healthcare"


# Membuat engine dan sesi
engine = create_engine(DATABASE_URL, connect_args={"charset": "utf8mb4"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Mendeklarasikan Base untuk model
Base = declarative_base()

# Dependency untuk mendapatkan sesi (DB)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
