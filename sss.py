from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./health.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    region = Column(String)

class Medication(Base):
    __tablename__ = "medications"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    salt = Column(String)
    price = Column(Float)
    description = Column(String)

class AyurvedicMedicine(Base):
    __tablename__ = "ayurveda"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    dosha_type = Column(String)
    benefits = Column(String)

class DietLog(Base):
    __tablename__ = "diet_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    food_item = Column(String)
    calories = Column(Float)

class Insurance(Base):
    __tablename__ = "insurance"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    provider = Column(String)
    policy_number = Column(String)

import requests

class OneMGService:
    BASE_URL = "https://api.1mg.com"  # placeholder

    def search_medicine(self, name: str):
        # Replace with real API key integration
        return {
            "name": name,
            "source": "1mg",
            "available": True,
            "note": "Stub response - integrate official API"
        }

class PractoService:

    def find_doctors(self, city: str, speciality: str):
        # Practo API is restricted → placeholder
        return [
            {
                "name": "Dr. Sample",
                "speciality": speciality,
                "city": city,
                "rating": 4.5
            }
        ]

class AyurvedaService:

    def get_recommendation(self, dosha: str):
        data = {
            "vata": "Warm food, sesame oil, avoid cold drinks",
            "pitta": "Cooling foods like cucumber, coconut water",
            "kapha": "Light food, spices, avoid dairy excess"
        }
        return data.get(dosha.lower(), "No recommendation found")

def indian_diet_recommendation(region: str):
    diets = {
        "north": ["roti", "dal", "rice", "paneer"],
        "south": ["idli", "dosa", "sambar", "rice"],
        "west": ["bhakri", "vegetables", "dal"],
        "east": ["rice", "fish curry", "lentils"]
    }
    return diets.get(region.lower(), ["balanced diet recommended"])

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models

from services.ayurveda_service import AyurvedaService
from services.practo_service import PractoService
from services.onemg_service import OneMGService
from utils.diet import indian_diet_recommendation

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Indian Health Platform")

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# MEDICINE SEARCH (1mg)
# -------------------------
@app.get("/medicine/search/")
def search_medicine(name: str):
    service = OneMGService()
    return service.search_medicine(name)

# -------------------------
# AYURVEDA
# -------------------------
@app.get("/ayurveda/")
def ayurveda(dosha: str):
    service = AyurvedaService()
    return {"recommendation": service.get_recommendation(dosha)}

# -------------------------
# DIET RECOMMENDATION
# -------------------------
@app.get("/diet/")
def diet(region: str):
    return {"foods": indian_diet_recommendation(region)}

# -------------------------
# DOCTORS (Practo stub)
# -------------------------
@app.get("/doctors/")
def doctors(city: str, speciality: str):
    service = PractoService()
    return service.find_doctors(city, speciality)