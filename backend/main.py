# # backend/main.py
# #  https://codingnomads.com/blog/python-fastapi-tutorial
# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# from . import database, models

# app = FastAPI()

# #  https://fastapi.tiangolo.com/advanced/middleware/
# # middleware to allow requests from the frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust based on your frontend's origin
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Dependency to get the SQLAlchemy Session
# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Add a GET endpoint
# @app.get("/test")
# def test_endpoint():
#     return {"message": "This is a test endpoint"}

# # API endpoint to save the name to the database
# @app.post("/save_input")
# def save_input(user_input: str, db: Session = Depends(get_db)):
#     # Create a new record in the database
#     db_user = models.User(name=user_input)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return {"message": "WooHoo!! - Name saved successfully"}
