import subprocess
import sys
import os

def install_requirements():
    print("🔄 Installing required packages from requirements.txt...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        
        # Check if .env exists
        if not os.path.exists(".env"):
            print("⚠️  .env file not found!")
            print("📋 Please copy .env.example to .env and fill in your configuration")
            print("   cp .env.example .env")
        
        print("🚀 Setup complete! You can now run:")
        print("   python manage.py refresh-db  # Setup database")
        print("   python run.py                # Start the server")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()