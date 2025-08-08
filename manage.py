import sys
from app.database import engine
from app.models.base_model import Base
from app.models.user import User

def refresh_db():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Database refreshed successfully!")
    print(f"Tables created: {list(Base.metadata.tables.keys())}")

def show_help():
    print("Available commands:")
    print("  python manage.py refresh-db    - Drop and recreate all database tables")
    print("  python manage.py help          - Show this help message")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "refresh-db":
        refresh_db()
    elif command == "help":
        show_help()
    else:
        print(f"Unknown command: {command}")
        show_help()
        sys.exit(1)