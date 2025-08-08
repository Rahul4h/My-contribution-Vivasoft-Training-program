import uvicorn
from app.config.settings import get_settings

settings = get_settings()

if __name__ == "__main__":
    print(f"Starting server on {settings.HOST}:{settings.PORT_NUMBER}...")
    print(f"Application: {settings.APP_NAME}")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT_NUMBER,
        reload=True,
        log_level="info"
    )
    
    print("Server has shut down")
