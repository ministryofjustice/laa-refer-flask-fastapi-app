# backend/fast_api_refer.py
#  https://codingnomads.com/blog/python-fastapi-tutorial
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from . import models, database

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "This is FastAPIRefer.py returning something"}

# https://fastapi.tiangolo.com/advanced/middleware/
# middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust based on your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the SQLAlchemy Session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add a GET endpoint
@app.get("/test")
def test_endpoint():
    return {"message": "This is a test endpoint"}

class UserInput(BaseModel):
    user_input: str


# API endpoint to save the name to the database
@app.post("/save_input")
def save_input(user_input: UserInput, db: Session = Depends(database.get_db)):
    # Create a new record in the database
    db_user = models.User(name=user_input.user_input)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"user_id": db_user.id, "message": "WooHoo!! - Name saved successfully"}

#  this is to display the data so I can see that it did actually come across from flask
@app.get("/get_data/{user_id}")
def get_data(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user.id, "name": user.name}
