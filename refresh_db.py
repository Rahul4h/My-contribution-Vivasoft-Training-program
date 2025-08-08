from app.database import engine
from app.models.base_model import Base

def refresh_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Database refreshed successfully!")
    print(f"Tables created: {list(Base.metadata.tables.keys())}")

if __name__ == "__main__":
    refresh_database()