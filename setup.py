from subprocess import check_call, CalledProcessError
from sys import executable, exit
from os.path import exists

REQUIREMENTS_FILE = "requirements.txt"
ENV_FILE = ".env"
ENV_EXAMPLE_FILE = ".env.example"
COPY_ENV_COMMAND = f"cp {ENV_EXAMPLE_FILE} {ENV_FILE}"
REFRESH_DB_COMMAND = "python manage.py refresh-db"
RUN_SERVER_COMMAND = "python run.py"

def install_requirements():
    print("🔄 Installing required packages from requirements.txt...")
    
    try:
        check_call([executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE])
        print("✅ All packages installed successfully!")
        
        # Check if .env exists
        if not exists(ENV_FILE):
            print("⚠️  .env file not found!")
            print(f"📋 Please copy {ENV_EXAMPLE_FILE} to {ENV_FILE} and fill in your configuration")
            print(f"   {COPY_ENV_COMMAND}")
        
        print("🚀 Setup complete! You can now run:")
        print(f"   {REFRESH_DB_COMMAND}  # Setup database")
        print(f"   {RUN_SERVER_COMMAND}                # Start the server")
        
    except CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        exit(1)

if __name__ == "__main__":
    install_requirements()