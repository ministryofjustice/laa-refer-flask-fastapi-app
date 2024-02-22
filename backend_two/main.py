from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Boolean, Column, Float, String, Integer
from pydantic import constr, ValidationError, validator

app1 = FastAPI()

#SqlAlchemy Setup
SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:///./db.sqlite3:'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DBUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    account_number = Column(String(6))
    nino = Column(String(9))
    description = Column(String, nullable=True)
    appointment_booked = Column(Boolean)
    user_contacted = Column(Boolean)
    postcode = Column(String(8))
    case_costs = Column(Integer)
    billable_units = Column(Float)

Base.metadata.create_all(bind=engine)

# A Pydantic User
class User(BaseModel):
    name: str
    account_number: str
    nino: str # replaced by line below with stricter validation
    # nino: constr(min_length=8)  # sometimes a NINO can not include the final letter in the string format LLNNNNNNL
    description: Optional[str] = None
    appointment_booked: bool
    user_contacted: bool
    postcode: str
    case_costs: float
    billable_units: int

    class Config:
        orm_mode = True

    @validator("nino")
    def validate_nino_length_and_pattern(cls, value):
        if len(value) not in (8,9):
            raise ValueError("NINO must be 8 or 9 characters long")
        import re
        pattern = re.compile(r"^[A-CEGHJ-PR-TW-Z]{1}[A-CEGHJ-NPR-TW-Z]{1}[0-9]{6}[A-DFM]{0,1}$")
        if not pattern.match(value):
            raise ValueError("NINO must match the specified pattern LLNNNNNN(L)")
        if not value.isalnum():
            raise ValueError("NINO must contain only alphanumeric characters")
        return value

def get_user(db: Session, user_id: int):
    return db.query(DBUser).where(DBUser.id == user_id).first()

def get_users(db: Session):
    return db.query(DBUser).all()

def create_user(db: Session, user: User):
    # db_user = DBUser(**user.model_dump())
    db_user = DBUser(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app1.get('/')  # this is a route
async def root(): # run this method when the route is called
    return {'message': 'Hello William, how can I serve?'}

# V1 of users before I had a DB
# @app.post('/users/')
# async def create_user_view(user: User):
#     return user

# V2 of /users
@app1.post('/users/', response_model=User)
def create_users_view(user: User, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user

@app1.get('/users/', response_model=List[User])
def get_users_view(db: Session = Depends(get_db)):
    return get_users(db)

@app1.get('/users/{user_id}')
def get_user_view(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)

