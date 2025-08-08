# Build APIs with FastAPI

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Uvicorn](https://img.shields.io/badge/Uvicorn-009639?style=for-the-badge&logo=gunicorn&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FastApi
   ```

2. **Install dependencies** (choose one method)
   
   **Option A: Using setup script (recommended)**
   ```bash
   python setup.py
   ```

2. **Install and Setup PostgreSQL and pgAdmin**

   - **Install PostgreSQL**  
     Download and install PostgreSQL from the [official website](https://www.postgresql.org/download/).  
     Follow the installation steps and remember your database username and password.

   - **Install pgAdmin [official website](https://www.pgadmin.org/download/)**  

   - **Create a Database**  

   - **Configure Database Connection**  
     Update your `.env` file with the correct PostgreSQL connection details:
     ```
     DATABASE_URL=postgresql://<username>:<password>@localhost:5432/fastapi_auth_db
     ```

3. **Refresh the database**
   ```bash
   python manage.py refresh-db
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload or
   python run.py
   ```

5. **Access the application**
   - API: http://127.0.0.1:8000
   - Interactive Docs: http://127.0.0.1:8000/docs
   - Alternative Docs: http://127.0.0.1:8000/redoc

## 📁 Project Structure

```
API/
├── app/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py       
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── base_controller.py 
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth_middleware.py
│   │   ├── guest_middleware.py
│   │   └── middleware_registry.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py           
│   │   └── user.py           
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── base_repository.py 
│   ├── routers/
│   │    └── routes.py  
│   ├── schemas/
│   │   └── __init__.py            
│   ├── services/
│   │   ├── __init__.py
│   │   └── base_service.py    
│   ├── __init__.py
│   └── database.py         
├── .env                       
├── .env.example               
├── .gitignore                 
├── app.db                     
├── main.py                    
├── manage.py                  
├── refresh_db.py              
├── requirements.txt           
├── run.py                     
├── setup.py                   
└── README.md                  
```

## 🤝 Contributing
1. Clone the repository
2. Create a meaningful branch
3. Make your changes
4. Submit a pull request
